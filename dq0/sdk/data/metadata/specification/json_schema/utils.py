class Utils:
    @staticmethod
    def type_name_property(object_name, object_type, type_name):
        return f""""type_name": {{
  "description": "The '{object_name}' {object_type}'s type name is '{type_name}'",
  "type": "string",
  "const": "{type_name}"
}}"""
