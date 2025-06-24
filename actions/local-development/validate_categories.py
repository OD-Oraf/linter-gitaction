import json
import sys
from jsonschema import Draft7Validator
from jsonschema.exceptions import ValidationError

def validate_categories(categories_path, schema_path, output_format="text"):
    try:
        # Load schema
        with open(schema_path) as f:
            schema = json.load(f)
        
        # Load categories data
        with open(categories_path) as f:
            data = json.load(f)
        
        # Validate against schema
        validator = Draft7Validator(schema)
        all_errors = list(validator.iter_errors(data))

        if not all_errors:
            if output_format == "json":
                result = {
                    "valid": True,
                    "errors": [],
                    "summary": "Validation successful"
                }
                print(json.dumps(result, indent=2))
            else:
                print("✅ Validation successful")
            return True

        # Track errors by tagKey to avoid duplicates
        errors_by_tag = {}
        
        # Extract enum values from schema definitions
        tag_enums = {}
        if "$defs" in schema:
            defs = schema["$defs"]
            # Map definition names to their enum values
            if "owningBusinessGroupValues" in defs:
                tag_enums["Owning Business Group"] = defs["owningBusinessGroupValues"]["enum"]
            if "dataClassificationValues" in defs:
                tag_enums["Data Classification"] = defs["dataClassificationValues"]["enum"]

        # Process validation errors
        for error in all_errors:
            # Find the item index and tagKey
            if error.absolute_path and len(error.absolute_path) > 0:
                item_index = list(error.absolute_path)[0]
                if isinstance(item_index, int) and item_index < len(data):
                    item = data[item_index]
                    tag_key = item.get("tagKey")
                    
                    if tag_key and tag_key not in errors_by_tag:
                        # Find invalid values in the item
                        invalid_values = []
                        if isinstance(item.get("value"), list):
                            for val in item["value"]:
                                if tag_key in tag_enums and val not in tag_enums[tag_key]:
                                    invalid_values.append(val)
                        elif isinstance(item.get("value"), str):
                            val = item["value"]
                            if tag_key in tag_enums and val not in tag_enums[tag_key]:
                                invalid_values.append(val)
                        
                        if invalid_values:
                            errors_by_tag[tag_key] = {
                                'invalid_values': invalid_values,
                                'allowed_values': tag_enums.get(tag_key, [])
                            }

        if output_format == "json":
            # JSON output format
            json_errors = []
            for tag_key, error_info in errors_by_tag.items():
                json_errors.append({
                    "tagKey": tag_key,
                    "invalidValues": error_info['invalid_values'],
                    "allowedValues": error_info['allowed_values']
                })
            
            # If no specific enum errors found, include generic errors
            if not errors_by_tag:
                for error in all_errors:
                    json_errors.append({
                        "message": error.message,
                        "path": '.'.join(map(str, error.absolute_path)) if error.absolute_path else "",
                        "invalidValue": str(error.instance) if hasattr(error, 'instance') else ""
                    })
            
            result = {
                "valid": False,
                "errors": json_errors,
                "summary": f"Found {len(json_errors)} validation error(s)"
            }
            print(json.dumps(result, indent=2))
        else:
            # Text output format (existing)
            for tag_key, error_info in errors_by_tag.items():
                print(f"❌ Validation error for tagKey: {tag_key}")
                print(f"Invalid value(s): {', '.join(map(str, error_info['invalid_values']))}")
                print("Allowed values:")
                for val in error_info['allowed_values']:
                    print(f"- {val}")
                print()

            # If no specific enum errors found, show generic errors
            if not errors_by_tag:
                for error in all_errors:
                    print(f"❌ {error.message}")
                    if error.absolute_path:
                        print(f"Path: {'.'.join(map(str, error.absolute_path))}")
                    print()

        return False
        
    except FileNotFoundError as e:
        if output_format == "json":
            result = {
                "valid": False,
                "errors": [{"message": f"File not found: {e.filename}"}],
                "summary": "File not found error"
            }
            print(json.dumps(result, indent=2))
        else:
            print(f"❌ File not found: {e.filename}")
        return False
    except json.JSONDecodeError as e:
        if output_format == "json":
            result = {
                "valid": False,
                "errors": [{"message": f"JSON parse error: {e.msg}"}],
                "summary": "JSON parsing error"
            }
            print(json.dumps(result, indent=2))
        else:
            print(f"❌ JSON parse error: {e.msg}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 3 or len(sys.argv) > 4:
        print("Usage: python validate_categories.py <categories.json> <schema.json> [--json]")
        sys.exit(1)
        
    categories_file = sys.argv[1]
    schema_file = sys.argv[2]
    output_format = "json" if len(sys.argv) == 4 and sys.argv[3] == "--json" else "text"
    
    if not validate_categories(categories_file, schema_file, output_format):
        sys.exit(1)
