# flow-log-parser

## About
This project is designed to parse flow log files to match the dstports and protocols to tags. The Flow Log Parser takes a text file of logs and a csv file with 3 columns: dstport, protocol, and tag. It then parses the logs and uses the lookup table to output tag counts and port/protocol combination counts to designated output file. 

## Setup
Download or clone project locally.
Navigate to project folder. 
Run FlowLogParser.py via command line: 

`python3 FlowLogParser.py [flow log text file] [lookup table css file] [output file]`

The project includes sample log and csv files, as well as an empty output.txt file for convenience.


Example usage: Navigate to main project folder. Run `python3 src/FlowLogParser.py resources/sample_flow_log_file.txt resources/sample_lookup.csv output.txt`

## Implementation Notes

### CSV Processing
The parser first processes the given csv file into a hashmap for easy lookups. This is designed for better performance when dealing with large log and csv files. For very small lookup tables or small log files, it might make sense to open and read the csv file and check line-by-line for a matching tag. If memory is a concern, the second approach might also work better for you, as the first approach trades off the additional memory for better performance for large files. 

### Testing
The parser includes 2 test files: `CSVProcessorTest.py` and `FileProcessorTest.py`. These include a few small tests for basic implementation details. With more time, I would create a more comprehensive test suite, making sure to test larger data files and malformed/invalid data files.


### Assumptions
- Supports only default log format.
- Supports only version 2.
- Supports only 30 common protocols included in socket module’s protocol constants (listed below)
- Assumes CSV column names to be “dstport”, “protocol”, and “tag” exactly
- Requires entire CSV file to be valid in order to use lookup table (in case of error, the behavior is as if the CSV lookup table is empty).
- Requires entire flow log file to be valid to process logs (in case of error, the behavior is as if the file is empty).

Supported protocols:

0: 'HOPOPTS',
 1: 'ICMP',
 2: 'IGMP',
 3: 'GGP',
 4: 'IPIP',
 6: 'TCP',
 8: 'EGP',
 12: 'PUP',
 17: 'UDP',
 22: 'IDP',
 29: 'TP',
 36: 'XTP',
 41: 'IPV6',
 43: 'ROUTING',
 44: 'FRAGMENT',
 46: 'RSVP',
 47: 'GRE',
 50: 'ESP',
 51: 'AH',
 58: 'ICMPV6',
 59: 'NONE',
 60: 'DSTOPTS',
 63: 'HELLO',
 77: 'ND',
 80: 'EON',
 103: 'PIM',
 108: 'IPCOMP',
 132: 'SCTP',
 255: 'RAW',
 256: 'MAX'
