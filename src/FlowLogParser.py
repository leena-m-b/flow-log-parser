import argparse
import FileProcessor
import CSVProcessor

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('log_file', type=str, help="path to flow log file")
    parser.add_argument('csv_file', type=str, help="path to csv look up table")
    parser.add_argument('output_file', type=str, help="path to output file")
    args = parser.parse_args()

    csv_map = CSVProcessor.process_csv(args.csv_file)
    tag_counts, port_protocol_counts = FileProcessor.process_logs(args.log_file, csv_map)
    FileProcessor.write_to_output(args.output_file, tag_counts, port_protocol_counts)

if __name__ == "__main__":
    main()