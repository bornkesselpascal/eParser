import os
from datetime import datetime
from constants import tables, diagrams, output_folder, results_folder, os_name, concurrent_execution
from parsing import parse_description_file, parse_result_file, parse_query_messages
from file_management import validate_test_folder, check_server_data
from tablemaker import write_test_table, write_query_table
from graphs import create_campaign_graphs, create_scenario_graphs, create_datagramsize_graphs


parent_folder = os.path.dirname(os.path.dirname((os.path.abspath(__file__))))

# Output folder for the current execution
commit_hash   = os.popen('git rev-parse HEAD').read().strip()[:7]
timestamp     = datetime.now().strftime('%y%m%d_%H%M%S')
operating_sys = os_name()
output_folder = os.path.join(parent_folder, output_folder, f'{timestamp}_{commit_hash}_{operating_sys}')
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Results folder for the current execution
result_folder = os.path.join(parent_folder, results_folder)
if not os.path.exists(result_folder):
    exit(1)



def __parse_campaign(name: str) -> None:
    # Check if the results folder exists
    data_folder   = os.path.join(result_folder, name)
    if not os.path.isdir(data_folder):
        return

    client_folder = os.path.join(data_folder, 'client')
    server_folder = os.path.join(data_folder, 'server')

    if not os.path.exists(client_folder):
        # If no data is available, we stop here.
        return

    # Print start message
    print(f'Starting eParser for campaign {name}... (at {datetime.now().strftime("%Y-%m-%d %H:%M:%S")})')

    # Create campaign folder for the output
    campaign_folder = os.path.join(output_folder, name)
    if not os.path.exists(campaign_folder):
        os.makedirs(campaign_folder)


    # List of tuples containing the following data for each test scenario:
    #   - description:    dict
    #   - client_results: dict
    #   - server_results: dict or None
    #   - query_messages: list (of dicts) or None
    test_data = list()
    processes = list()

    # Parse all test scenarios and store the data in the list
    for test_folder in os.listdir(client_folder):
        test_folder_client = os.path.join(client_folder, test_folder)
        if not os.path.isdir(test_folder_client):
            continue

        # Check if test folder is valid (contains test_description.xml and test_results.xml)
        if not validate_test_folder(test_folder_client):
            continue
        print(f'Processing test scenario {test_folder}...')

        # Check if server data exists
        server_data = check_server_data(server_folder, test_folder)
        if server_data:
            test_folder_server = os.path.join(server_folder, test_folder)

        # Parse the test description file
        description = parse_description_file(test_folder_client)

        # Parse the test results files
        client_results = parse_result_file(test_folder_client)
        if server_data:
            server_results = parse_result_file(test_folder_server)
        else:
            server_results = None

        # Parse the query messages
        query_messages = parse_query_messages(test_folder_client)

        test_data.append((description, client_results, server_results, query_messages))


    # Sort the list after 'cycle_time' and then after 'datagram_size' (both in description)
    test_data.sort(key=lambda x: (x[0]['connection']['datagram_size'], x[0]['connection']['cycle_time']))

    # Write the test data to a csv file and create query overview if possible
    if tables['generate']:
        write_test_table(test_data, name, campaign_folder, processes)
        write_query_table(test_data, campaign_folder, processes)

    # Create diagrams:
    #   - campaign
    #   - scenario (only if query messages are available)
    #   - datagram size
    if diagrams['generate']:
        create_campaign_graphs(test_data, campaign_folder, processes)
        create_scenario_graphs(test_data, campaign_folder, processes)
        create_datagramsize_graphs(test_data, campaign_folder, processes)


    # End the execution of eParser
    if concurrent_execution():
        for process in processes:
            process.join()

    print(f'Finished eParser for campaign {name}... (at {datetime.now().strftime("%Y-%m-%d %H:%M:%S")})')



# Process all campaigns in the results folder
campaign_list = list()
for test_campaign in os.listdir(result_folder):
    if test_campaign.endswith('_N') or test_campaign.startswith('.'):
        continue

    print(f'Process campaign {test_campaign}? (y/n)')
    answer = input().lower()

    if 'y' in answer:
        campaign_list.append(test_campaign)
    if 'a' in answer:
        break

for test_campaign in campaign_list:
    __parse_campaign(test_campaign)
