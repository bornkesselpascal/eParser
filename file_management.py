import os
from constants import test_description_file, test_results_file

def validate_test_folder(path: str) -> bool:
    '''
    Checks if the given path contains the test description and test result files.

            Parameters:
                    path (str): Path to the test scenario folder

            Returns:
                    result (bool): True if the folder contains the test description and test result
                                   files, False otherwise
    '''
    files_in_path = os.listdir(path)
    return test_results_file in files_in_path

def check_server_data(server_folder: str, test_folder: str) -> bool:
    '''
    Checks if server data exists for the given test scenario and that the test folder is valid.

            Parameters:
                    server_folder (str): Path the base folder containing the server data
                    test_folder (str): Name of the test scenario folder

            Returns:
                    result (bool): True if the server data exists and the test folder is valid,
                                   False otherwise
    '''
    test_folder_server = os.path.join(server_folder, test_folder)
    if not os.path.exists(test_folder_server):
        return False

    return validate_test_folder(test_folder_server)
    