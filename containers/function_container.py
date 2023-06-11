from dataclasses import dataclass

from enums.scope import Scope


@dataclass
class FunctionContainer:
    identifier: str
    return_type: str
    params: str
    scope: Scope
    body: str
    class_name: str
    is_new: bool = False

    @property
    def name(self):
        scope_map = {Scope.PUBLIC: "", Scope.PROTECTED: "pr_", Scope.PRIVATE: "pv_"}
        return f"{scope_map[self.scope]}{self.identifier}"

    @name.setter
    def name(self, value):
        raise AttributeError("Cannot set name of FunctionContainer")

    def get_in_struct_declaration(self):
        return f"{self.return_type} (*{self.name}){self.params};"

    def get_global_declaration(self):
        if self.is_new:
            return f"{self.return_type} new__{self.class_name}{self.params};"
        return f"{self.return_type} {self.class_name}_{self.name}{self.params};"

    def get_definition(self):
        if self.is_new:
            return f"{self.return_type} new__{self.class_name}{self.params} {self.body}"
        return f"{self.return_type} {self.class_name}_{self.name}{self.params} {self.body}"

    def get_entry_point_definition(self):
        return f"{self.return_type} {self.name}{self.params} {self.body}"

