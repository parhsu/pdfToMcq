from services.fileManagement.convert_pdf_to_csv import convert_pdf_to_csv

# if __name__ == '__main__':
#     convert_all_pdf_to_csv()

import tkinter as tk
from tkinter import filedialog


def open_file():
    # Open file dialog to select a file
    filepath = filedialog.askopenfilename()

    if filepath:
        # Read the contents of the selected file
        convert_pdf_to_csv(filepath)



# Create the GUI panel
window = tk.Tk()
window.title("File Selection")

# Create a button to open the file dialog
open_button = tk.Button(window, text="Open File", command=open_file)
open_button.pack()

# Start the GUI event loop
window.mainloop()

