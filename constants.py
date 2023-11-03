import os

# FOLDER NAMES
output_folder = 'output'
results_folder = 'results'

# LOG NAMES
test_description_file = 'test_description.xml'
test_results_file = 'test_results.xml'

# TABLE OPTIONS
tables = {
    'generate' : True,
    'excel' : {
        'generate' : True,
        'font_name' : 'Arial',
        'monospace_font_name' : 'Consolas',
    }
}

# DIAGRAM OPTIONS
diagrams = {
    'generate' : True,
    'histogram' : False,

    'colors' : {'datagramsize': {80: 'lightgray', 8900: 'steelblue', 65000: '#9fcc9f',},
                'location': {'CLIENT': 'lightgray', 'SERVER': 'steelblue', 'BOTH': '#9fcc9f',},
                'paket_type': {'sent': 'lightgray', 'received': 'steelblue',},},

    'output' : {
        'pdf': True,
        'latex' : False,
        'png' : True,
    },
}

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
