import json

def update_config():
    try:
        # Read the example config
        try:
            with open("config.json.example", "r") as example_file:
                example_config = json.load(example_file)
        except json.JSONDecodeError as e:
            print(f"Error reading config.json.example: Invalid JSON format")
            print(f"Details: {str(e)}")
            return
        except FileNotFoundError:
            print("config.json.example not found")
            return
        
        # Read the current config
        try:
            with open("config.json", "r") as config_file:
                current_config = json.load(config_file)
        except FileNotFoundError:
            current_config = {}
        except json.JSONDecodeError:
            print("Warning: Invalid config.json, creating new one")
            current_config = {}
        
        # Merge new options while preserving existing values
        updated = False
        for key, value in example_config.items():
            if key not in current_config:
                current_config[key] = value
                print(f"Added new option: {key} = {value}")
                updated = True
        
        # Save the updated config
        if updated:
            with open("config.json", "w") as config_file:
                json.dump(current_config, config_file, indent=4)
            print("Configuration updated successfully!")
        else:
            print("Configuration is already up to date!")
            
    except Exception as e:
        print(f"Error updating configuration: {str(e)}")

if __name__ == "__main__":
    update_config()