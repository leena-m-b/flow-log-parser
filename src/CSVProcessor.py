import csv

"""
Reads through csv lookup table and creates a dictionary mapping pairs
(dstport, protocol) to tag. Returns empty in case of error.
Case insensitivity is handled by having protocols be in lowercase and tags
in uppercase.
"""
def process_csv(file_path):
    try:
        csv_map = {}
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                csv_map[(row['dstport'], row['protocol'].lower())] = (row['tag']).upper()

            return csv_map
    
    except FileNotFoundError:
        print(f"File {file_path} does not exist.")
        return {}
    except KeyError as e:
        print(f"Missing expected column in CSV file {e}")
        return {}
    except Exception as e:
        print(f"An error occurred while processing the file: {e}")
        return {}