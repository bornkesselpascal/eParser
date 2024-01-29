import tkinter as tk
from tkinter import filedialog
import xml.etree.ElementTree as ET

def select_file_and_process():
    # Set up the root tkinter window
    root = tk.Tk()
    root.withdraw()  # we don't want a full GUI, so keep the root window from appearing

    # Show an "Open" dialog box and return the path to the selected file
    file_path = filedialog.askopenfilename(filetypes=[("XML files", "*.xml")])
    if not file_path:
        return  # No file was selected

    try:
        # Parse the XML file
        tree = ET.parse(file_path)
        root_element = tree.getroot()

        # Extract difference values
        differences = [record.find('difference').text for record in root_element.findall('record')]

        # Write differences to a text file
        with open('differences.txt', 'w') as file:
            for diff in differences:
                file.write(diff + '\n')

        print("Differences written to differences.txt")

    except ET.ParseError:
        print("Error: Could not parse the XML file.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Run the function
select_file_and_process()
