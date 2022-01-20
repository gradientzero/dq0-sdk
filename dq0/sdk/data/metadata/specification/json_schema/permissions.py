class Permissions:
    @staticmethod
    def permissions_property(key, title, operation):
        return f""""{key}": {{
  "title": "{title}",
  "description": "List of user/role uuids allowed to perform '{operation}' operations.",
  "type": "object",
  "patternProperties": {{
    "^([0-9a-f]{{8}}-[0-9a-f]{{4}}-[0-9a-f]{{4}}-[0-9a-f]{{4}}-[0-9a-f]{{12}})+$": {{ "type": "null" }}
  }},
  "additionalProperties": false
}}"""

    @staticmethod
    def json_schema(owner, properties):
        permissions_properties = ''
        for index, property in enumerate(properties):
            if 0 < index:
                permissions_properties += "\n        "
            permissions_properties += property.replace("\n", "\n        ")
            if index < len(properties) - 1:
                permissions_properties += ','
        return f"""{{
  "title": "Permissions",
  "description": "Permissions, governing access to its '{owner}' owner object.",
  "oneOf": [
    {{
      "type": "null"
    }},
    {{
      "type": "object",
      "properties": {{
        {permissions_properties}
      }},
      "minProperties": 1,
      "additionalProperties": false
    }}
  ]
}}"""
