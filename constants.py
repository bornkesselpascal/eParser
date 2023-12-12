import os

# FOLDER NAMES
output_folder = 'results/performance/output'
raw_folder = 'results/performance/raw'

# LOG NAMES
test_description_file = 'test_description.xml'
test_results_file = 'test_results.xml'

# XML OUTPUT OPTIONS
create_timediff_xml = False

# EXECUTION OPTIONS
def os_name():
    if os.name == 'nt':
        return 'Windows'
    elif os.name == 'posix':
        if os.uname().sysname == 'Darwin':
            return 'macOS'
        else:
            return 'Linux'
        
    return 'unknown'

def concurrent_execution():
    if os_name() == 'Linux':
        return True
    else:
        return False

max_worker = 5
