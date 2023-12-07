import xml.etree.ElementTree as ET

def parse_performance_report(file_path) -> dict:
    # Parse the XML file
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Initialize an empty dictionary to store the data
    data_dict = {}

    # Iterate through each child of the root
    for child in root:
        section = child.tag
        data_dict[section] = {}

        # Iterate through each element of the child
        for element in child:
            data_dict[section][element.tag] = element.text

    return data_dict

def parse_timestamp_messages(path: str) -> list:
    '''
    Parses the timestamp messages from the test results file and returns them as a list of dictionaries.
    Each dictionary contains the following keys: 'sequence', 'tv_sec', 'tv_nsec'. The list is sorted by
    sequence.

            Parameters:
                    path (str): Path to the test results file

            Returns:
                    reports (list): List of dictionaries containing the query messages
    '''
    tree = ET.parse(path)
    root = tree.getroot()

    records = list()

    for record in root.findall('record'):
        sequence = record.find('sequence').text
        difference = float(record.find('difference').text)

        records.append({
            'sequence': sequence,
            'difference': difference,
        })

    return records