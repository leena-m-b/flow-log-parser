import io
import sys
import os
from collections import defaultdict

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import FileProcessor

def test_process_logs():
    test_file_path = 'test_path.txt'
    with open(test_file_path, 'w') as file:
        file.write("2 123456789012 eni-9k10l11m 192.168.1.5 51.15.99.115 49321 25 6 20 10000 1620140661 1620140721 ACCEPT OK\n")
        file.write("2 123456789012 eni-5f6g7h8i 10.0.2.103 52.26.198.183 56000 23 6 15 7500 1620140661 1620140721 REJECT OK\n")
    
    csv_map = {
        ('25', 'tcp'): 'SV_P1',
        ('23', 'tcp'): 'SV_P2',
    }
    
    tag_counts, port_protocol_counts = FileProcessor.process_logs(test_file_path, csv_map)
    os.remove(test_file_path)
    
    expected_tag_counts = defaultdict(int, {"SV_P1": 1, "SV_P2": 1})
    expected_port_protocol_counts = defaultdict(int, {('25', 'tcp'): 1, ('23', 'tcp'): 1})
    
    assert tag_counts == expected_tag_counts, f"Expected {expected_tag_counts}, but got {tag_counts}"
    assert port_protocol_counts == expected_port_protocol_counts, f"Expected {expected_port_protocol_counts}, but got {port_protocol_counts}"
    

def test_process_logs_untagged():
    test_file_path = 'test_path.txt'
    with open(test_file_path, 'w') as file:
        file.write("2 123456789012 eni-0a1b2c3d 10.0.1.201 198.51.100.2 443 49153 6 25 20000 1620140761 1620140821 ACCEPT OK\n")
        file.write("2 123456789012 eni-0a1b2c3d 10.0.1.201 198.51.100.2 443 23 6 25 20000 1620140761 1620140821 ACCEPT OK\n")
    
    csv_map = {
        ('25', 'tcp'): 'SV_P1',
        ('23', 'udp'): 'SV_P2',
    }
    
    tag_counts, port_protocol_counts = FileProcessor.process_logs(test_file_path, csv_map)
    os.remove(test_file_path)
    
    expected_tag_counts = defaultdict(int, {'No match found.': 2})
    expected_port_protocol_counts = defaultdict(int, {('49153', 'tcp'): 1, ('23', 'tcp'): 1})
    
    assert tag_counts == expected_tag_counts, f"Expected {expected_tag_counts}, but got {tag_counts}"
    assert port_protocol_counts == expected_port_protocol_counts, f"Expected {expected_port_protocol_counts}, but got {port_protocol_counts}"
    
def test_process_logs_ignores_bad_lines():
    test_file_path = 'test_path.txt'
    with open(test_file_path, 'w') as file:
        file.write("2 123456789012 eni-9k10l11m 192.168.1.5 51.15.99.115 49321 25 6 20 10000 1620140661 1620140721 ACCEPT OK\n")
        file.write("123456789012")
        file.write("2 123456789012 eni-5f6g7h8i 10.0.2.103 52.26.198.183 56000 23 6 15 7500 1620140661 1620140721 REJECT OK\n")
    
    csv_map = {
        ('25', 'tcp'): 'SV_P1',
        ('23', 'tcp'): 'SV_P2',
    }
    
    tag_counts, port_protocol_counts = FileProcessor.process_logs(test_file_path, csv_map)
    os.remove(test_file_path)
    
    expected_tag_counts = defaultdict(int, {"SV_P1": 1, "SV_P2": 1})
    expected_port_protocol_counts = defaultdict(int, {('25', 'tcp'): 1, ('23', 'tcp'): 1})
    
    assert tag_counts == expected_tag_counts, f"Expected {expected_tag_counts}, but got {tag_counts}"
    assert port_protocol_counts == expected_port_protocol_counts, f"Expected {expected_port_protocol_counts}, but got {port_protocol_counts}"
    

test_process_logs()
test_process_logs_untagged()
test_process_logs_ignores_bad_lines()
# test_read_file_file_not_found()

print("Tests passed.")



# def test_read_file():
#     test_file_path = 'test_path.txt'
#     with open(test_file_path, 'w') as file:
#         file.write("2 123456789012 eni-0a1b2c3d 10.0.1.201 198.51.100.2 443 49153 6 25 20000 1620140761 1620140821 ACCEPT OK\n")
#         file.write("2 123456789012 eni-0a1b2c3d 10.0.1.201 198.51.100.2 443 49153 6 25 20000 1620140761 1620140821 ACCEPT OK\n")
#         file.write("2 123456789012 eni-9k10l11m 192.168.1.5 51.15.99.115 49321 25 6 20 10000 1620140661 1620140721 ACCEPT OK\n")
#         file.write("2 123456789012 eni-5f6g7h8i 10.0.2.103 52.26.198.183 56000 23 6 15 7500 1620140661 1620140721 REJECT OK\n")
#         file.write("2 123456789012 eni-4h5i6j7k 172.16.0.2 192.0.2.146 49154 143 6 9 4500 1620140661 1620140721 ACCEPT OK\n")
    
#     csv_map = {
#         ('25', 'tcp'): 'sv_P1',
#         ('23', 'tcp'): 'SV_p2',
#         ('143', 'tcp'): 'sv_p1'
#     }
    
#     tag_counts, port_protocol_counts = FileProcessor.read_file(test_file_path, csv_map)
#     os.remove(test_file_path)
    
#     expected_tag_counts = defaultdict(int, {'No match found.': 2, "SV_P1": 2, "SV_P2": 1})
#     expected_port_protocol_counts = defaultdict(int, {('49153', 'tcp'): 2, ('25', 'tcp'): 1, ('23', 'tcp'): 1, ('143', 'tcp'): 1})
    
#     assert tag_counts == expected_tag_counts, f"Expected {expected_tag_counts}, but got {tag_counts}"
#     assert port_protocol_counts == expected_port_protocol_counts, f"Expected {expected_port_protocol_counts}, but got {port_protocol_counts}"
    