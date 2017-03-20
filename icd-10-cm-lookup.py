# Program to look up ICD-10-CM information
# Author: Jonathan Castellanos-Gomez

import os
import csv
import re

from tkinter import *

codes = []
descriptions = [] 
code_key_dict = {}
desc_key_dict = {}

def create_data_store():
    global codes, descriptions 
    global code_key_dict, desc_key_dict

    print("\nCreating ICD10-CM data store...")
    with open('icd10cm.txt', 'r') as fin:
        reader = csv.reader(fin, delimiter='\t')
        for entry in reader:
            code = entry[0]
            description = entry[1]
            codes.append(code)
            descriptions.append(description)
            code_key_dict[code] = description
            desc_key_dict[description] = code

def find_match_candidates(term, storage):
    candidates = []
    for entry in storage:
        if term.upper() in entry.upper():
            candidates.append(entry)

    return candidates

def parse_code(code):
    result = ""
    candidates = find_match_candidates(code, codes)
    if candidates:
        result += "\nThe descriptions that match your code are: \n"
        for c in candidates:
            desc = code_key_dict.get(c)
            entry = c + ": " + desc + "\n"
            result += entry
    else:
        result = "\nNo matches were found for the code: " + code

    return result

def parse_description(desc):
    result = ""
    candidates = find_match_candidates(desc, descriptions)
    if candidates:
        result = "\nThe codes that match your description are: \n"
        for c in candidates:
            code = desc_key_dict.get(c)
            entry = code + ": " + c + "\n"
            result += entry
    else:
        result = "\nNo matches were found for your description."

    return result

def search():
    search_term = input_entry.get()
    match = re.search(r'^[a-zA-Z]\d\d(\.\d{1,3})?$', search_term)
    if match:
        resultfield.delete(1.0, END)
        resultfield.insert(END, parse_code(match.group()))
    else:
        resultfield.delete(1.0, END)
        resultfield.insert(END, parse_description(search_term))

def clear_entries():
    resultfield.delete(1.0, END)
    input_entry.delete(0, END)

create_data_store()
print("Data store has been created.")

root = Tk()
root.title("Simple ICD-10-CM Lookup")

Label(root, text="Enter an ICD-10-CM code or description:").pack()
input_entry = Entry(root)
input_entry.pack()
    
Button(root, text="Search", command=search).pack()
Button(root, text="Clear", command=clear_entries).pack()

resultfield = Text(root)
resultfield.pack()

Button(root, text="Quit", command=root.destroy).pack()

root.mainloop()



