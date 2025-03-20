import json
import sys
import os

# Define required files
REQUIRED_FILES = ["glyphs.json", "modes.json", "phrases.json", "rules.json"]

def validate_json(filename, data):
    """ Validate JSON structure based on filename """
    if filename == "glyphs.json" and not isinstance(data, dict):
        raise ValueError("glyphs.json should be a dictionary.")

    if filename == "modes.json" and not isinstance(data, dict):
        raise ValueError("modes.json should be a dictionary.")

    if filename == "phrases.json" and not isinstance(data, dict):
        raise ValueError("phrases.json should be a dictionary.")

    if filename == "rules.json":
        if not isinstance(data, list):
            raise ValueError("rules.json should be a list.")
        for rule in data:
            if not all(k in rule for k in ["name", "regex", "replacement"]):
                raise ValueError(f"rules.json contains an invalid rule: {rule}")

# Validate uploaded files
uploaded_files = os.listdir("json_files")
missing_files = set(REQUIRED_FILES) - set(uploaded_files)

if missing_files:
    print(f"❌ Missing required files: {missing_files}")
    sys.exit(1)

for file in REQUIRED_FILES:
    with open(f"json_files/{file}", "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
            validate_json(file, data)
            print(f"✅ {file} is valid.")
        except Exception as e:
            print(f"❌ {file} validation failed: {e}")
            sys.exit(1)

print("🎉 All JSON files are valid!")