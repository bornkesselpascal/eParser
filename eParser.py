# NOTE: This is the eParser for performance tests. For the reliability tests, use an older commit.

import os
from datetime import datetime
from constants import output_folder, raw_folder, os_name, concurrent_execution
from parsing import parse_description_file, parse_result_file, parse_timestamp_messages
from file_management import validate_test_folder, check_server_data
from performance_evaluation import evaluate_performance
from multiprocessing import Process



parent_folder = os.path.dirname(os.path.dirname((os.path.abspath(__file__))))

# Output folder for the current execution
commit_hash   = os.popen('git rev-parse HEAD').read().strip()[:7]
timestamp     = datetime.now().strftime('%y%m%d_%H%M%S')
operating_sys = os_name()
output_folder = os.path.join(parent_folder, output_folder, f'{timestamp}_{commit_hash}_{operating_sys}')
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Raw folder for the current execution
result_folder = os.path.join(parent_folder, raw_folder)
if not os.path.exists(result_folder):
    exit(1)



def __handle_scenario(name :str, client_path: str, server_path: str, output_path: str) -> None:
    # Print start message
    print(f'Starting eParser for scenario {name}... (at {datetime.now().strftime("%Y-%m-%d %H:%M:%S")})')

    # Create campaign folder for the output
    campaign_folder = os.path.join(output_path, name)
    if not os.path.exists(campaign_folder):
        os.makedirs(campaign_folder)


    # List of tuples containing the following data for each test scenario:
    #   - description:    dict
    #   - client_results: dict
    #   - server_results: dict
    #   - client_timestamps: list (of dicts)
    #   - server_timestamps: list (of dicts)

    processes_test = list()

    # Parse all test scenarios and store the data in the list
    for test_folder in os.listdir(client_path):
        if concurrent_execution():
            process = Process(target=__handle_test, args=(test_folder, client_path, server_path, campaign_folder))
            process.start()
            processes_test.append(process)
        else:
            __handle_test(test_folder, client_path, server_path, campaign_folder)

    if concurrent_execution():
        for process in processes_test:
            process.join()

    print(f'Finished eParser for scenario {name}... (at {datetime.now().strftime("%Y-%m-%d %H:%M:%S")})')

def __handle_test(test_folder: str, client_path: str, server_path: str, output_path: str):
    test_folder_client = os.path.join(client_path, test_folder)
    if not os.path.isdir(test_folder_client):
        return

    # Check if test folder is valid (contains test_description.xml and test_results.xml)
    if not validate_test_folder(test_folder_client):
        return
    print(f'Processing test {test_folder}... (at {datetime.now().strftime("%Y-%m-%d %H:%M:%S")})')

    # Check if server data exists
    server_data = check_server_data(server_path, test_folder)
    if server_data:
        test_folder_server = os.path.join(server_path, test_folder)

    # Parse the test description file
    description = parse_description_file(test_folder_client)

    # Parse the test results files
    client_results = parse_result_file(test_folder_client)
    if server_data:
        server_results = parse_result_file(test_folder_server)
    else:
        server_results = None

    # Parse the query messages
    client_timestamps = parse_timestamp_messages(test_folder_client)
    if server_data:
        server_timestamps = parse_timestamp_messages(test_folder_server)
    else:
        server_timestamps = None

    test = (description, client_results, server_results, client_timestamps, server_timestamps)
    output_folder = os.path.join(output_path, test[0]['metadata']['t_uid'])
    evaluate_performance(test, output_folder)

    # Delete everything
    del description
    del client_results
    del server_results
    del client_timestamps
    del server_timestamps
    del test

# Ask for the campaigns to process
campaign_list = list()
for test_campaign in os.listdir(result_folder):
    if test_campaign.endswith('_N') or test_campaign.startswith('.') or test_campaign.endswith('.7z'):
        continue

    print(f'Process campaign {test_campaign}? (y/n)')
    answer = input().lower()

    if 'y' in answer:
        campaign_list.append(test_campaign)
    if 'a' in answer:
        break

# Process the selected campaigns
for test_campaign in campaign_list:
    # The folder is structured as follows:
    #   - raw_folder
    #       - campaign (e.g. 04_1_Base_A)
    #           - client
    #               - test_scenario (e.g. ihwk_A1_092400_111223)
    #                   - test (e.g. 092400_111223_1_80)
    #                       - test_description.xml
    #                       - test_results.xml
    #                   - ...
    #               - ...
    #           - server
    #               - test_scenario (e.g. ihwk_A1_092400_111223)
    #                   - test (e.g. 092400_111223_1_80)
    #                       - test_description.xml
    #                       - test_results.xml
    #                   - ...
    #               - ...
    #       - ...


    # Get the client and server folder for the current campaign
    test_campaign_client = os.path.join(result_folder, test_campaign, 'client')
    test_campaign_server = os.path.join(result_folder, test_campaign, 'server')

    # Get the output folder for the current campaign
    test_campaign_output = os.path.join(output_folder, test_campaign)
    
    processes_scenario = list()

    # Get the test scenarios for the current campaign
    for test_scenario in os.listdir(test_campaign_client):
        # Skip files
        if test_scenario.endswith('_N') or test_scenario.startswith('.') or test_scenario.endswith('.7z'):
            continue

        test_scenario_client = os.path.join(test_campaign_client, test_scenario)
        test_scenario_server = os.path.join(test_campaign_server, test_scenario)
        
        if concurrent_execution():
            process = Process(target=__handle_scenario, args=(test_scenario, test_scenario_client, test_scenario_server, test_campaign_output))
            process.start()
            processes_scenario.append(process)
        else:
            __handle_scenario(test_scenario, test_scenario_client, test_scenario_server, test_campaign_output)

    if concurrent_execution():
        for process in processes_scenario:
            process.join()
