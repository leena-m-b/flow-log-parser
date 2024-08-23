import csv
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
import CSVProcessor

def test_process_csv():
    test_path = 'test_path.csv'
    with open(test_path, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['dstport', 'protocol', 'tag'])
        writer.writeheader()
        writer.writerow({'dstport': '80', 'protocol': 'TCP', 'tag': 'sv_p1'})
        writer.writerow({'dstport': '443', 'protocol': 'udp', 'tag': 'SV_p2'})
    
    csv_map = CSVProcessor.process_csv(test_path)

    os.remove(test_path)
    
    expected_csv_map = {
        ('80', 'tcp'): 'SV_P1',
        ('443', 'udp'): 'SV_P2'
    }
    
    assert csv_map == expected_csv_map, f"Expected csv_map to be {expected_csv_map}, but got {csv_map}."
    

test_process_csv()
print("Tests passed.")