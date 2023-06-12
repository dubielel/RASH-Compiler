from copy import deepcopy
from enum import Enum

from containers.function_container import FunctionContainer
from containers.variable_container import VariableContainer
from enums.scope import Scope


class AccessRestriction(Enum):
    RESTRICTED_PROTECTED = 1
    RESTRICTED_PRIVATE = 2
    GRANTED = 3


class ClassContainer:
    has_init: bool
    name: str
    methods: dict[str, FunctionContainer]
    attributes: dict[str, VariableContainer]

    static_methods: dict[str, FunctionContainer]
    static_attributes: dict[str, VariableContainer]

    library_dependencies: set[str]
    subclasses: set["ClassContainer"]
    superclasses: set["ClassContainer"]

    def __init__(self, name: str):
        self.name = name
        self.methods = {}
        self.attributes = {}
        self.static_methods = {}
        self.static_attributes = {}
        self.has_init = False
        self.library_dependencies = set()
        self.subclasses = set()
        self.superclasses = set()

    def add_attribute(self, attribute: VariableContainer, is_static: bool = False):
        if is_static:
            self.static_attributes[attribute.identifier] = attribute
        else:
            self.attributes[attribute.identifier] = attribute

    def add_method(self, method: FunctionContainer, is_static: bool = False):
        if method.identifier == "__init__":
            self.has_init = True

        if is_static:
            self.static_methods[method.identifier] = method
        else:
            self.methods[method.identifier] = method

    def add_library_dependency(self, lib: str):
        self.library_dependencies.add(lib)

    def create_new_method(self) -> FunctionContainer:
        self.library_dependencies.add("stdlib.h")

        body = f"{{\n\t{self.name}* self = ({self.name}*)malloc(sizeof({self.name}));\n"

        for attribute in self.attributes.values():
            if attribute.value:
                body += f"\tself->{attribute.name} = {attribute.value};\n"

        for method in self.methods.values():
            body += f"\tself->{method.name} = {self.name}_{method.name};\n"

        if self.has_init:
            init_method = self.methods["__init__"]
            init_params = init_method.params[1:-1].split(", ")
            init_params = [p.split(" ")[1] for p in init_params][1:]
            final_init_params = ["self", *init_params]
            body += f"\tself->{init_method.name}({', '.join(final_init_params)});\n\treturn self;\n}}"
            return FunctionContainer(
                f"new__{self.name}",
                self.name + "*",
                f"({', '.join(init_method.params[1:-1].split(', ')[1:])})",    # Remove self
                init_method.scope,
                body,
                self.name,
                is_new=True,
            )

        body += "\treturn self;\n}"

        return FunctionContainer(
            f"new__{self.name}",
            self.name + "*",
            "()",
            Scope.PRIVATE,
            body,
            self.name,
            is_new=True,
        )

    def save_class(self, dir: str):
        header_path = f"{dir}/{self.name}.h"
        source_path = f"{dir}/{self.name}.c"

        new_method = self.create_new_method()

        with open(header_path, "w+") as f:
            # Preamble and library dependencies

            f.write(f"#ifndef {self.name.upper()}_H\n")
            f.write(f"#define {self.name.upper()}_H\n\n")

            for lib in self.library_dependencies:
                f.write(f"#include<{lib}>\n")

            # Typedef

            f.write(f"\n")
            f.write(f"typedef struct s_{self.name} {self.name};\n\n")

            # Struct definition ------------------------------------------------------------------------------

            f.write(f"struct s_{self.name} {{\n")

            # Attributes in struct

            for attribute in self.attributes.values():
                f.write(f"\t{attribute.get_declaration()}\n")

            # Methods in struct

            for method in self.methods.values():
                f.write(f"\t{method.get_in_struct_declaration()}\n")
            f.write(f"}};\n\n")

            # End of struct ---------------------------------------------------------------------------------

            # Methods prototypes and static attributes and methods declaration ------------------------------

            for method in self.methods.values():
                f.write(f"{method.get_global_declaration()}\n")

            for method in self.static_methods.values():
                f.write(f"{method.get_global_declaration()}\n")

            for attribute in self.static_attributes.values():
                f.write(f"{attribute.get_static_declaration()}\n")

            f.write(f"{new_method.get_global_declaration()}\n")

            # End of prototypes ------------------------------------------------------------------------------

            f.write(f"\n#endif\n")

        with open(source_path, "w+") as f:
            f.write(f"#include \"{self.name}.h\"\n\n")

            for method in self.methods.values():
                f.write(f"{method.get_definition()}\n\n")

            for attribute in self.static_attributes.values():
                f.write(f"{attribute.get_static_definition()}\n\n")

            for method in self.static_methods.values():
                f.write(f"{method.get_definition()}\n\n")

            f.write(f"{new_method.get_definition()}\n\n")

    def add_subclass(self, subclass: "ClassContainer"):
        self.subclasses.add(subclass)

    def add_superclass(self, superclass: "ClassContainer"):
        self.superclasses.add(superclass)

        for attribute in superclass.attributes.values():
            # Enable overriding attributes
            if attribute.identifier not in self.attributes:
                self.attributes[attribute.identifier] = deepcopy(attribute)
                self.attributes[attribute.identifier].class_name = self.name

        for method in superclass.methods.values():
            # Enable overriding methods
            if method.identifier == "__init__":
                self.methods["super"] = deepcopy(method)
                self.methods["super"].class_name = self.name
                self.methods["super"].params = self.methods["super"].params.replace(superclass.name, self.name)
                self.methods["super"].identifier = "super"
                continue
            if method.identifier not in self.methods:
                self.methods[method.identifier] = deepcopy(method)
                old_class_name = self.methods[method.identifier].class_name
                self.methods[method.identifier].class_name = self.name
                self.methods[method.identifier].params = self.methods[method.identifier].params.replace(old_class_name, self.name)

        for static_attribute in superclass.static_attributes.values():
            # Enable overriding static attributes
            if static_attribute.identifier not in self.static_attributes:
                self.static_attributes[static_attribute.identifier] = deepcopy(static_attribute)
                self.static_attributes[static_attribute.identifier].class_name = self.name

        for static_method in superclass.static_methods.values():
            # Enable overriding static methods
            if static_method.identifier not in self.static_methods:
                self.static_methods[static_method.identifier] = deepcopy(static_method)
                old_class_name = self.static_methods[static_method.identifier].class_name
                self.static_methods[static_method.identifier].class_name = self.name



    def has_access(self, scope: Scope, accessor_name: str) -> AccessRestriction:
        if scope == Scope.PUBLIC:
            return AccessRestriction.GRANTED
        elif scope == Scope.PROTECTED:
            return AccessRestriction.GRANTED if accessor_name in list(map(lambda x: x.name, self.subclasses)) else AccessRestriction.RESTRICTED_PROTECTED
        elif scope == Scope.PRIVATE:
            return AccessRestriction.GRANTED if accessor_name == self.name else AccessRestriction.RESTRICTED_PRIVATE

