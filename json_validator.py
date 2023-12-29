import json

class JsonValidator:
    """
    Class for validating JSON against a given schema.
    """

    @staticmethod
    def validate_schema(json_file: str, schema_file: str) -> bool:
        """
        Validate JSON against a given schema.
        
        :param json_file: Path to the JSON file to be validated.
        :type json_file: str
        :param schema_file: Path to the schema file for validation rules.
        :type schema_file: str
        :return: True if validation succeeds, False otherwise.
        :return type: bool
        """
        try:
            with open(json_file, 'r') as jfile, open(schema_file, 'r') as sfile:
                json_data = json.load(jfile)
                schema = json.load(sfile)

                # Validate required fields
                if not JsonValidator.validate_required_fields(json_data, schema):
                    return False

                # Validate at least one of many fields
                if not JsonValidator.validate_at_least_one_of(json_data, schema):
                    return False

                # Validate either one field or another field
                if not JsonValidator.validate_either_one_or_another(json_data, schema):
                    return False

                # Validate mutually exclusive fields
                if not JsonValidator.validate_mutually_exclusive_fields(json_data, schema):
                    return False

                # Validate field value to be one of a set of values
                if not JsonValidator.validate_field_values(json_data, schema):
                    return False

            return True

        except FileNotFoundError as e:
            print(f"File not found: {e}")
            return False
        except json.JSONDecodeError as e:
            print(f"JSON decoding error: {e}")
            return False
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return False

    @staticmethod
    def validate_required_fields(json_data: dict, schema: dict) -> bool:
        """
        Validate required fields.
        
        :param json_data: JSON data to be validated.
        :type json_data: dict
        :param schema: Schema for validation rules.
        :type schema: dict
        :return: True if validation succeeds, False otherwise.
        :return type: bool
        """
        for field in schema.get("required_fields", []):
            if field not in json_data:
                print(f"Required field '{field}' is missing.")
                return False
        return True

    @staticmethod
    def validate_at_least_one_of(json_data: dict, schema: dict) -> bool:
        """
        Validate at least one of many fields.
        
        :param json_data: JSON data to be validated.
        :type json_data: dict
        :param schema: Schema for validation rules.
        :type schema: dict
        :return: True if validation succeeds, False otherwise.
        :return type: bool
        """
        field_group = schema.get("at_least_one_of", [])
        present_fields = [field for field in field_group if json_data.get(field)]
        if not present_fields:
            print(f"At least one of {field_group} should be present.")
            return False
        return True

    @staticmethod
    def validate_either_one_or_another(json_data: dict, schema: dict) -> bool:
        """
        Validate either one field or another field.
        
        :param json_data: JSON data to be validated.
        :type json_data: dict
        :param schema: Schema for validation rules.
        :type schema: dict
        :return: True if validation succeeds, False otherwise.
        :return type: bool
        """
        field_group = schema.get("either_one_or_another", [])
        present_fields = [field for field in field_group if json_data.get(field)]
        if len(present_fields) > 1:
            print(f"Either one of {field_group} should be present.")
            return False
        return True

    @staticmethod
    def validate_mutually_exclusive_fields(json_data: dict, schema: dict) -> bool:
        """
        Validate mutually exclusive fields.
        
        :param json_data: JSON data to be validated.
        :type json_data: dict
        :param schema: Schema for validation rules.
        :type schema: dict
        :return: True if validation succeeds, False otherwise.
        :return type: bool
        """
        field_group = schema.get("mutually_exclusive_fields", [])
        present_fields = [field for field in field_group if json_data.get(field)]
        if len(present_fields) != 1:
            print(f"Mutually exclusive fields {field_group} should not be present together.")
            return False
        return True

    @staticmethod
    def validate_field_values(json_data: dict, schema: dict) -> bool:
        """
        Validate field value to be one of a set of values.
        
        :param json_data: JSON data to be validated.
        :type json_data: dict
        :param schema: Schema for validation rules.
        :type schema: dict
        :return: True if validation succeeds, False otherwise.
        :return type: bool
        """
        for field, allowed_values in schema.get("field_values", {}).items():
            if json_data.get(field) not in allowed_values:
                print(f"Field '{field}' should have one of the values {allowed_values}.")
                return False
        return True

# Example usage:
json_validator = JsonValidator()

try:
    result = json_validator.validate_schema('json_data.json', 'schema.json')
    print(result)
except FileNotFoundError as e:
    print(f"File not found: {e}")
except json.JSONDecodeError as e:
    print(f"JSON decoding error: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
    """
    Create an instance of JsonValidator and call the validate_schema.

    :param json_data.json: JSON file to be validated.
    :type json_data.json: json module
    :param schema.json: Schema file for validation rules.
    :type schema.json: json module
    """
