import json
from os import stat
import tkinter, time
from turtle import title
import pandas as pd
from tkinter import *
from tkinter import filedialog, ttk

file_options = ["xlsx", "csv"]
pfad_liste = []
user = {}

def get_list(pfad_liste1, list_dict, parent=""):
    for i in list_dict:
        w = type(i)
        if type(i) == list:
            get_list(pfad_liste1, i, parent='{}:{}'.format(parent, i))
        elif type(i) == dict:
            get_keys(i, parent=parent)
        else:
            pass
def get_keys(some_dictionary, parent=""):
    global pfad_liste
    if "schemaVersion" in some_dictionary:
        pfad_liste = []
    for key, value in some_dictionary.items():
        if "{" not in str(value):
            pfad_liste.append('{}:{}/{}'.format(parent, key, value))
        if isinstance(value, dict):
            get_keys(value, parent='{}:{}'.format(parent, key))
        elif isinstance(value, list):
            get_list(pfad_liste, value, parent='{}:{}'.format(parent, key))
        else:
            pass
    return pfad_liste


# ----------- Upload File ------------ #
def upload_file():
    filename = filedialog.askopenfilenames()
    tkinter.messagebox.showinfo(title="Import file", message=str(len(filename)) + " File(s) are successfully imported!")
    return filename

def start_progress(progress):
    progress.start(20)

def stop_progress(progress):
    progress.stop()

def myfunction(*args):
    x = filetype_entry.get()
    y = filename_entry.get()
    if x and y:
        read_button.config(state='normal')
    else:
        read_button.config(state='disabled')
# ----------- Read and Extraxt JSON ------------ #
def write():
    filetype = filetype_entry.get()
    savename = filename_entry.get()
    if savename != "":
        files = upload_file()
    start_time = time.time()
    for file in files:
        with open(file, encoding="utf-8") as json_file:
            data = json.load(json_file)
            if "/" in file:
                file_partition = file.split("/")
                file = file_partition[len(file_partition) - 1]
            user[file] = get_keys(data)

    try:
        df = pd.DataFrame({ key1:pd.Series(value1) for key1, value1 in user.items()})
        if filetype == ".xlsx (empfohlen)":
            df.to_excel(savename+".xlsx", engine="xlsxwriter", index=False)
            time_needed = time.time() - start_time
            tkinter.messagebox.showinfo(title="Import file", message=str(len(files)) + " File(s) are successfully read and written to " +savename+".xlsx" + "\n" + "Time needed is " + str("{:.2f}".format(time_needed)) + " Sekunden")
        elif filetype == ".csv":
            df.to_csv(savename+".csv", index=False)
            time_needed = time.time() - start_time
            tkinter.messagebox.showinfo(title="Import file", message=str(len(files)) + " File(s) are successfully read and written to " + savename +".csv" + "\n" + "Time needed is " + str("{:.2f}".format(time_needed)) + " Sekunden")
        else:
            tkinter.messagebox.showerror(title="Warning!", message="Please choose the correct file type from the dropdown!!")
        filetype_entry.delete(0, END)
        filename_entry.delete(0, END)
        
        window.destroy()
    except:
        tkinter.messagebox.showerror(title="Warning!", message="The progress has failed!")
        window.destroy()

# ----------- GUI ------------- #

window = Tk()
window.title("JSON Pfade-Auslesen")
window.config(padx=25, pady=25)


#Labels
filetype_label = Label(text="Save file as .xlsx/.csv:")
filetype_label.grid(row=1, column=0)

filename_label = Label(text="Save the .xlsx/.csv with name*:")
filename_label.grid(row=2, column=0)

place_maker_label = Label(text="")
place_maker_label.grid(row=3, column=0, columnspan=2)

file_label = Label(text="Import the JSON files here")
file_label.grid(row=4,column=0)

#Eingabe
filetype_entry = ttk.Combobox(window, values=[".xlsx (empfohlen)", ".csv"], state="readonly")
filetype_entry.current(0)
filetype_entry.grid(row=1, column=1, columnspan=2)

filename_entry = Entry(width=15)
filename_entry.grid(row=2, column=1, columnspan=2)


read_button = Button(text="Choose JSON files", command=write)
read_button.grid(row=4, column=1, columnspan=2)

window.mainloop()
