import os
import xml.etree.ElementTree as ET
from constants import create_timediff_xml

def evaluate_performance(test_data: list, output_folder: str) -> None:
    output_summary_filename = os.path.join(output_folder, "performance.xml")
    output_timediff_filename = os.path.join(output_folder, "timediff.xml")
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


    # Check if there is packet loss (if the number of timestamps is not the same)
    paket_loss = True
    if(len(test_data[3]) == len(test_data[4])):
        paket_loss = False



    # Get the sequence numbers from the client and server timestamps
    client_sequence_numbers = list()
    for timestamp in test_data[3]:
        client_sequence_numbers.append(int(timestamp['sequence']))
    server_sequence_numbers = list()
    for timestamp in test_data[4]:
        server_sequence_numbers.append(int(timestamp['sequence']))

    # Check if server sequence numbers are in the same order (the client sequence numbers are always in order)
    in_order = True
    sorted_server_sequence_numbers = sorted(server_sequence_numbers)
    if server_sequence_numbers != sorted_server_sequence_numbers:
        in_order = False


    # Sort test data [3] and [4] by sequence number
    test_data[3].sort(key=lambda x: int(x['sequence']))
    test_data[4].sort(key=lambda x: int(x['sequence']))

    # Get the timestamps for each sequence number
    timestamps = list()
    server_records = {int(record['sequence']): record for record in test_data[4]}

    for record_client in test_data[3]:
        client_sequence = int(record_client['sequence'])
        record_server = server_records.get(client_sequence)

        # Check if the sequence numbers are equal (should always be the case, except if there is packet loss)
        if record_server is None:
            continue
        
        # Calculate the difference between the timestamps
        diff_sec = int(record_server['tv_sec']) - int(record_client['tv_sec'])
        diff_nsec = int(record_server['tv_nsec']) - int(record_client['tv_nsec'])

        # Check if the nanoseconds are negative
        if diff_nsec < 0:
            diff_sec -= 1
            diff_nsec += 1000000000

        # Calculate the difference in seconds
        difference = diff_sec + (diff_nsec / 1000000000)

        timestamps.append({
            'sequence': client_sequence,
            'difference': difference
        })


    # Calculate the Mean Latency
    mean_latency = 0
    for timestamp in timestamps:
        mean_latency += timestamp['difference']
    mean_latency = mean_latency / len(timestamps)

    # Calculate the standard deviation
    standard_deviation = 0
    for timestamp in timestamps:
        standard_deviation += (timestamp['difference'] - mean_latency) ** 2
    standard_deviation = (standard_deviation / len(timestamps)) ** 0.5

    # Calculate the minimum and maximum latency
    minimum_latency = min(timestamps, key=lambda x: x['difference'])['difference']
    maximum_latency = max(timestamps, key=lambda x: x['difference'])['difference']

    # Calculate the difference between the minimum and maximum latency
    difference_latency = maximum_latency - minimum_latency

    # Calculate the mean jitter
    mean_jitter = 0
    for timestamp in timestamps:
        mean_jitter += abs(timestamp['difference'] - mean_latency)
    mean_jitter = mean_jitter / len(timestamps)



    # Create the summary XML file
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
    ET.SubElement(xml_timestamps, 'mean_latency').text = str(mean_latency)
    ET.SubElement(xml_timestamps, 'standard_deviation').text = str(standard_deviation)
    ET.SubElement(xml_timestamps, 'minimum_latency').text = str(minimum_latency)
    ET.SubElement(xml_timestamps, 'maximum_latency').text = str(maximum_latency)
    ET.SubElement(xml_timestamps, 'difference_latency').text = str(difference_latency)
    ET.SubElement(xml_timestamps, 'mean_jitter').text = str(mean_jitter)

    # Write the formatted XML file to disk
    tree = ET.ElementTree(root)
    indent(tree.getroot()) # this I add
    tree.write(output_summary_filename, encoding='utf-8', xml_declaration=True)

    # Delete the xml tree and structure from memory
    del tree
    del root



    #  Create the timediff XML file
    if create_timediff_xml:
        root = ET.Element('timestamps')

        for timestamp in timestamps:
            record = ET.SubElement(root, 'record')
            ET.SubElement(record, 'sequence').text = str(timestamp['sequence'])
            ET.SubElement(record, 'difference').text = str(timestamp['difference'])

        # Write the formatted XML file to disk
        tree = ET.ElementTree(root)
        indent(tree.getroot()) # this I add
        tree.write(output_timediff_filename, encoding='utf-8', xml_declaration=True)

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