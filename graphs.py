import os
from multiprocessing import Process
from constants import concurrent_execution
from graphs_campaign import _prepare_and_create_campaign_graphs
from graphs_scenario import _prepare_and_create_scenario_graphs
from graphs_datagramsize import _prepare_and_create_datagramsize_graphs


def create_campaign_graphs(test_data: list, campaign_folder: str, processes: list = None) -> None:
    '''
    Creates the graphs for the campaign. This includes:
        - Packet loss per datagram size
        - Packet loss per cycle time

            Parameters:
                    test_data (list): List of parsed test scenarios
                    campaign_folder (str): Path to the folder where the table should be saved
                    processes (list): List of processes (optional, used for concurrent execution)

            Returns:
                    None
    '''
    campaign_path = os.path.join(campaign_folder, "campaign")
    if not os.path.exists(campaign_path):
        os.makedirs(campaign_path)

    if concurrent_execution():
        process = Process(target=_prepare_and_create_campaign_graphs, args=(test_data, campaign_path))
        process.start()
        processes.append(process)
    else:
        _prepare_and_create_campaign_graphs(test_data, campaign_path)


def create_scenario_graphs(test_data: list, campaign_folder: str, processes: list = None) -> None:
    '''
    Creates the graphs for each test scenario. This includes:
        - Histogram of packet losses
        - Packet losses over time
        - Sent and received packets over time
        - Packets per second over time / Packets per query over time

    Note that the diagrams are only created if the test scenario contains query messages. Otherwise
    the diagrams are skipped.

            Parameters:
                    test_data (list): List of parsed test scenarios
                    campaign_folder (str): Path to the folder where the table should be saved
                    processes (list): List of processes (optional, used for concurrent execution)

            Returns:
                    None
    '''
    scenario_path = os.path.join(campaign_folder, "scenario")
    if not os.path.exists(scenario_path):
        os.makedirs(scenario_path)

    for test_scenario in test_data:
        if (test_scenario[3] is not None) and (test_scenario[3] != []):
            scenario_subpath = os.path.join(scenario_path, f"{test_scenario[0]['metadata']['t_uid']}")
            if not os.path.exists(scenario_subpath):
                os.makedirs(scenario_subpath)

            if concurrent_execution():
                process = Process(target=_prepare_and_create_scenario_graphs, args=(test_scenario, scenario_subpath))
                process.start()
                processes.append(process)
            else:
                _prepare_and_create_scenario_graphs(test_scenario, scenario_subpath)


def create_datagramsize_graphs(test_data: list, campaign_folder: str, processes: list = None) -> None:
    '''
    Creates the graphs for the different datagram sizes. This includes:
        - Packet loss per cycle time

            Parameters:
                    test_data (list): List of parsed test scenarios
                    campaign_folder (str): Path to the folder where the table should be saved
                    processes (list): List of processes (optional, used for concurrent execution)

            Returns:
                    None
    '''
    datagramsizes = list(set(test_scenario[0]['connection']['datagram_size'] for test_scenario in test_data))
    datagramsize_path = os.path.join(campaign_folder, "datagram")
    if not os.path.exists(datagramsize_path):
        os.makedirs(datagramsize_path)
    
    for datagramsize in datagramsizes:

        if concurrent_execution():
            process = Process(target=_prepare_and_create_datagramsize_graphs, args=(test_data, datagramsize, datagramsize_path))
            process.start()
            processes.append(process)
        else:
            _prepare_and_create_datagramsize_graphs(test_data, datagramsize, datagramsize_path)