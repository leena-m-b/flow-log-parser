import argparse
import socket
from collections import defaultdict

DSTPORT_INDEX = 6
PROTOCOL_INDEX = 7

"""
Returns map of protocol number to keyword (e.g. tcp).
Uses socket's protocol constants. Contains 30 common protocols. 
"""
def load_protocol_map():
    return {v:k[8:] for (k,v) in vars(socket).items() if k.startswith('IPPROTO')}


def find_matching_tag(csv_map, dstport, protocol):
    if (dstport, protocol) in csv_map:
        return (csv_map[(dstport, protocol)])
    
    return "No match found."


"""
Reads through file of flow logs to create and return 2 dictionaries,
tag_counts and port_protocol_counts, needed for output. Returns empty
dicts in case of error.
"""
def process_logs(file_path, csv_map):
    protocols = load_protocol_map()

    try:
        with open(file_path, 'r') as file:
            tag_counts = defaultdict(int)
            port_protocol_counts = defaultdict(int)
            
            for line in file:
                components = line.split()
                dstport = components[DSTPORT_INDEX]
                protocol = protocols[int(components[PROTOCOL_INDEX])].lower()
                
                tag = find_matching_tag(csv_map, dstport, protocol)
                
                tag_counts[tag] += 1
                port_protocol_counts[(dstport, protocol)] += 1

            return tag_counts, port_protocol_counts

    except FileNotFoundError:
        print(f"File {file_path} does not exist.")
        return defaultdict(int), defaultdict(int)

    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return defaultdict(int), defaultdict(int)


def write_tag_counts(file, counts):
    file.write("Tag Counts:\n")
    file.write("Tag,Count\n")
    for key, val in counts.items():
        if key == "No match found.":
            file.write("Untagged,")
        else:
            file.write(f"{key},")
        file.write(f"{val}\n")


def write_port_protocol(file, counts):
    file.write("Port/Protocol Combination Counts:\n")
    file.write("Port,Protocol,Count\n")
    for key, val in counts.items():
        file.write(f"{key[0]},{key[1]},{val}\n")


def write_to_output(file_path, tag_counts, port_protocol_counts):
    try:
        with open(file_path, 'w') as file:
            write_tag_counts(file, tag_counts)
            file.write("\n")
            write_port_protocol(file, port_protocol_counts)
        
    except FileNotFoundError:
        print(f"File {file_path} does not exist.")

    except Exception as e:
        print(f"An error occurred while writing to the file: {e}")

