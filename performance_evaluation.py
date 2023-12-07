import os
import xml.etree.ElementTree as ET

def evaluate_performance(test_data: list, output_folder: str) -> None:
    output_filename = os.path.join(output_folder, "performance.xml")
    output_filename2 = os.path.join(output_folder, "timediffs.xml")
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Get basic data
    basic_tuid = test_data[0]['metadata']['t_uid']
    basic_datagramsize = test_data[0]['connection']['datagram_size']
    basic_cycletime = test_data[0]['connection']['cycle_time']

    # Calculate numbers
    test_duration = test_data[1]['report']['duration']
    test_datagrams = test_data[1]['report']['total']
    test_bandwidth = (test_datagrams * basic_datagramsize * 8) / test_duration

    if len(test_data[3]) == 0 or len(test_data[4]) == 0:
        print("Error: Timestamps are not available!")
        return

    # Evaluate the timestamps
    paket_loss = True
    if(len(test_data[3]) == len(test_data[4])):
        paket_loss = False

    # Get the timestamp difference for each sequence number
    # Check if the sequence numbers are the same, a counter is not enough because numbers my be missing or they are not in order
    # Iterate the client timestamps and get a sequence number, then iterate the server timestamps and get the same sequence number
    # The Send and Receive timestamps are then compared and the difference is calculated
    # The timestamps are stored as tv_sec and tv_nsec, so they have to be converted to seconds first
    # The difference is then calculated by subtracting the Send timestamp from the Receive timestamp
    # The difference is then stored in a list with the corresponding sequence number
    # The list is then sorted by the sequence number

    # Get the sequence numbers from the client timestamps
    client_sequence_numbers = list()
    for timestamp in test_data[3]:
        client_sequence_numbers.append(int(timestamp['sequence']))

    # Get the sequence numbers from the server timestamps
    server_sequence_numbers = list()
    for timestamp in test_data[4]:
        server_sequence_numbers.append(int(timestamp['sequence']))

    # Check if client and server sequence numbers are the same and in the same order
    in_order = True
    sorted_server_sequence_numbers = sorted(server_sequence_numbers)
    if server_sequence_numbers != sorted_server_sequence_numbers:
        print("Error: Sequence numbers are not the same or not in the same order!")
        in_order = False

        # Print out only the sequence numbers that is in a different order
        for i in range(len(server_sequence_numbers)):
            if server_sequence_numbers[i] != sorted_server_sequence_numbers[i]:
                print(f"Server: {server_sequence_numbers[i]}")
                print(f"Sorted: {sorted_server_sequence_numbers[i]}")

    # Sort test data [3] and [4] by sequence number
    test_data[3].sort(key=lambda x: int(x['sequence']))
    test_data[4].sort(key=lambda x: int(x['sequence']))

    # Get the timestamps for each sequence number
    timestamps = list()
    for i in range(len(test_data[3])):
        # Calculate the difference between the timestamps
        diff_sec = int(test_data[4][i]['tv_sec']) - int(test_data[3][i]['tv_sec'])
        diff_nsec = int(test_data[4][i]['tv_nsec']) - int(test_data[3][i]['tv_nsec'])

        # Check if the nanoseconds are negative
        if diff_nsec < 0:
            diff_sec -= 1
            diff_nsec += 1000000000

        # Calculate the difference in seconds
        difference = diff_sec + (diff_nsec / 1000000000)

        timestamps.append({
            'sequence': int(test_data[3][i]['sequence']),
            'difference': difference
        })

    # Calculate the average difference
    average_difference = 0
    for timestamp in timestamps:
        average_difference += timestamp['difference']
    average_difference = average_difference / len(timestamps)

    # Calculate the standard deviation
    standard_deviation = 0
    for timestamp in timestamps:
        standard_deviation += (timestamp['difference'] - average_difference) ** 2
    standard_deviation = (standard_deviation / len(timestamps)) ** 0.5

    # Calculate the minimum and maximum difference
    minimum_difference = timestamps[0]['difference']
    maximum_difference = timestamps[0]['difference']
    for timestamp in timestamps:
        if timestamp['difference'] < minimum_difference:
            minimum_difference = timestamp['difference']
        if timestamp['difference'] > maximum_difference:
            maximum_difference = timestamp['difference']

    # Calculate the minimum and maximum difference more efficiently
    minimum_difference = min(timestamps, key=lambda x: x['difference'])['difference']
    maximum_difference = max(timestamps, key=lambda x: x['difference'])['difference']


    # Calculate the difference between the minimum and maximum difference
    difference_difference = maximum_difference - minimum_difference

    # Calculate the jitter
    jitter = 0
    for timestamp in timestamps:
        jitter += abs(timestamp['difference'] - average_difference)
    jitter = jitter / len(timestamps)


    # Create the XML file
    root = ET.Element('performance')

    # Basic data
    basic = ET.SubElement(root, 'basic')
    ET.SubElement(basic, 't_uid').text = basic_tuid
    ET.SubElement(basic, 'datagram_size').text = str(basic_datagramsize)
    ET.SubElement(basic, 'cycle_time').text = str(basic_cycletime)

    # Test data
    test = ET.SubElement(root, 'test')
    ET.SubElement(test, 'duration').text = str(test_duration)
    ET.SubElement(test, 'datagrams').text = str(test_datagrams)
    ET.SubElement(test, 'bandwidth').text = str(test_bandwidth)

    # Timestamps
    xml_timestamps = ET.SubElement(root, 'timestamps')
    ET.SubElement(xml_timestamps, 'packet_loss').text = str(paket_loss)
    ET.SubElement(xml_timestamps, 'in_order').text = str(in_order)
    ET.SubElement(xml_timestamps, 'average_difference').text = str(average_difference)
    ET.SubElement(xml_timestamps, 'standard_deviation').text = str(standard_deviation)
    ET.SubElement(xml_timestamps, 'minimum_difference').text = str(minimum_difference)
    ET.SubElement(xml_timestamps, 'maximum_difference').text = str(maximum_difference)
    ET.SubElement(xml_timestamps, 'difference_difference').text = str(difference_difference)
    ET.SubElement(xml_timestamps, 'jitter').text = str(jitter)

    # Write the formatted XML file to disk
    tree = ET.ElementTree(root)
    indent(tree.getroot()) # this I add
    tree.write(output_filename, encoding='utf-8', xml_declaration=True)

    # Delete the xml tree and structure from memory
    del tree
    del root

    #  Write timestamps to XML file
    #  Create the XML file only if output_folder contains the string 'ihwk_1', 'ihwk_2' or 'ihwk_3', otherwise the file is not needed
    if 'ihwk_1' in output_folder or 'ihwk_2' in output_folder or 'ihwk_3' in output_folder:
        root = ET.Element('timestamps')

        for timestamp in timestamps:
            record = ET.SubElement(root, 'record')
            ET.SubElement(record, 'sequence').text = str(timestamp['sequence'])
            ET.SubElement(record, 'difference').text = str(timestamp['difference'])

        # Write the formatted XML file to disk
        tree = ET.ElementTree(root)
        indent(tree.getroot()) # this I add
        tree.write(output_filename2, encoding='utf-8', xml_declaration=True)

        del tree
        del root


def indent(elem, level=0, more_sibs=False):
    i = "\n"
    if level:
        i += (level-1) * '  '
    num_kids = len(elem)
    if num_kids:
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
            if level:
                elem.text += '  '
        count = 0
        for kid in elem:
            indent(kid, level+1, count < num_kids - 1)
            count += 1
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
            if more_sibs:
                elem.tail += '  '
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i
            if more_sibs:
                elem.tail += '  '