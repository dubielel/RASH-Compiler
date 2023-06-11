from containers.function_container import FunctionContainer
from containers.variable_container import VariableContainer
from enums.scope import Scope


class ClassContainer:
    has_init: bool
    name: str
    methods: dict[str, FunctionContainer]
    attributes: dict[str, VariableContainer]

    static_methods: dict[str, FunctionContainer]
    static_attributes: dict[str, VariableContainer]

    library_dependencies: set[str]

    def __init__(self, name: str):
        self.name = name
        self.methods = {}
        self.attributes = {}
        self.static_methods = {}
        self.static_attributes = {}
        self.has_init = False
        self.library_dependencies = set()

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

        body = f"{{\n\t{self.name}* this = ({self.name}*)malloc(sizeof({self.name}));\n"

        for attribute in self.attributes.values():
            if attribute.value:
                body += f"\tthis->{attribute.name} = {attribute.value};\n"

        for method in self.methods.values():
            body += f"\tthis->{method.name} = {self.name}_{method.name};\n"

        if self.has_init:
            init_method = self.methods["__init__"]
            init_params = init_method.params[1:-1].split(", ")
            init_params = [p.split(" ")[1] for p in init_params][1:]
            final_init_params = ["this", *init_params]
            body += f"\tthis->{init_method.name}({', '.join(final_init_params)});\n\treturn this;\n}}"
            return FunctionContainer(
                f"new__{self.name}",
                self.name + "*",
                f"({', '.join(init_method.params[1:-1].split(', ')[1:])})",    # Remove self
                init_method.scope,
                body,
                self.name,
                is_new=True,
            )

        body += "\treturn this;\n}"

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
            f.write(f"#ifndef {self.name.upper()}_H\n")
            f.write(f"#define {self.name.upper()}_H\n\n")

            for lib in self.library_dependencies:
                f.write(f"#include<{lib}>\n")

            f.write(f"\n")
            f.write(f"typedef struct s_{self.name} {self.name};\n\n")

            f.write(f"struct s_{self.name} {{\n")
            for attribute in self.attributes.values():
                f.write(f"\t{attribute.get_declaration()}\n")
            for method in self.methods.values():
                f.write(f"\t{method.get_in_struct_declaration()}\n")
            f.write(f"}};\n\n")

            for method in self.methods.values():
                f.write(f"{method.get_global_declaration()}\n")

            for method in self.static_methods.values():
                f.write(f"{method.get_global_declaration()}\n")

            f.write(f"{new_method.get_global_declaration()}\n")
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
