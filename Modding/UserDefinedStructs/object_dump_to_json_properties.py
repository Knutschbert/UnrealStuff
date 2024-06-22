#ai 

import re
import csv
import sys
from pathlib import Path

pattern = re.compile(r'STRUCT_METADATA (.*?);(.*?);(.*?);(.*?);(.*?);(.*?);(.*?)\n')

def parse_file(file_path):
    data = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            match = pattern.match(line)
            if match:
                data.append(match.groups())
    return data

def write_to_csv(data, output_csv_path):
    with open(output_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        # Write the header
        csvwriter.writerow(["---", "File", "Class_Name", "Property_Class_Name", "Friendly_Name", "Name_ID", "Name_GUID", "Dir"])
        # Write the data rows
        for i, row in enumerate(data):
            if i == 0:
                csvwriter.writerow(["Row"] + list(row))
            else:
                csvwriter.writerow([f"Row_{i-1}"] + list(row))

# Main function to handle file input and processing
def main(file_path):
    data = parse_file(file_path)
    output_csv_path = Path(file_path).with_suffix('.csv')
    write_to_csv(data, output_csv_path)
    print(f"CSV file created: {output_csv_path}")

if __name__ == "__main__":
    # Check if the script is run with an argument (file path)
    if len(sys.argv) > 1:
        input_file = Path(sys.argv[1])
    else:
        input_file = Path(r'I:\Epic Games\Chivalry2_c\TBL\Binaries\Win64\UE4SS_ObjectDump.txt')
        # print("Please drag and drop the file or pass the file path as an argument.")
        # sys.exit(1)
    
    # Check if the provided file exists
    if not input_file.exists():
        print(f"File not found: {input_file}")
        sys.exit(1)

    main(input_file)
