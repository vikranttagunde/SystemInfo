import sys
import json
import os

def process_text_file(file_path):
    json_output = {}
    with open(file_path, 'r') as txt_file:
        lines = txt_file.readlines()
        # Example processing logic; customize as needed
        for line in lines:
            if ":" in line:
                key, value = line.split(":", 1)
                json_output[key.strip()] = value.strip()
    
    json_file_path = os.path.splitext(file_path)[0] + '.json'
    with open(json_file_path, 'w') as json_file:
        json.dump(json_output, json_file, indent=2)
    print(f"Processed {file_path} -> {json_file_path}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python process_system_info.py <file_path>")
        sys.exit(1)
    process_text_file(sys.argv[1])