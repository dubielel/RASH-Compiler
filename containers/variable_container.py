from dataclasses import dataclass
from typing import Optional

from enums.scope import Scope


@dataclass
class VariableContainer:
    identifier: str
    type: str
    value: Optional[str]
    scope: Scope
    class_name: str

    @property
    def name(self):
        scope_map = {Scope.PUBLIC: "", Scope.PROTECTED: "pr_", Scope.PRIVATE: "pv_"}
        return f"{scope_map[self.scope]}{self.identifier}"

    @name.setter
    def name(self, value):
        raise AttributeError("Cannot set name of AttributeContainer")

    def get_static_declaration(self):
        return f"extern {self.type} {self.class_name}_{self.name};"

    def get_static_definition(self):
        if self.value is None:
            return f"{self.type} {self.class_name}_{self.name};"
        else:
            return f"{self.type} {self.class_name}_{self.name} = {self.value};"

    def get_declaration(self):
        return f"{self.type} {self.name};"

    def get_definition(self):
        if self.value is None:
            return f"{self.type} {self.name};"
        else:
            return f"{self.type} {self.name} = {self.value};"

