import xml.etree.ElementTree as ET
import os

def parse_xml(file_path):
    # Parse the XML file
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Find the timestamp element
    timestamp = root.find('.//timestamp')

    # Extract data from each record and store in a list
    records = []
    for record in timestamp.findall('record'):
        sequence = record.find('sequence').text
        tv_sec = record.find('.//tv_sec').text
        tv_nsec = record.find('.//tv_nsec').text
        records.append({'sequence': sequence, 'tv_sec': tv_sec, 'tv_nsec': tv_nsec})

    return records

# Example usage
parent_folder = os.path.dirname(os.path.dirname((os.path.abspath(__file__))))
file_path = parent_folder + '/results/client/ihwk_1_103025_051223/103147_051223_1_65000/test_results.xml'
records = parse_xml(file_path)
print(records)