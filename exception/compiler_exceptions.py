class ClassReferencedBeforeDefinitionException(Exception):
    def __init__(self, class_name: str, line_number: int):
        super().__init__(f"Class '{class_name}' referenced before definition on line {line_number}")


class InvalidTypeException(Exception):
    def __init__(self, type: str, line_number: int):
        super().__init__(f"Invalid type '{type}' on line {line_number}")


class ProtectedAttributeAccessException(Exception):
    def __init__(self, attribute_name: str, line_number: int):
        super().__init__(f"Attempted to access protected attribute '{attribute_name}' on line {line_number}")


class PrivateAttributeAccessException(Exception):
    def __init__(self, attribute_name: str, line_number: int):
        super().__init__(f"Attempted to access private attribute '{attribute_name}' on line {line_number}")