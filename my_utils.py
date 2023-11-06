import os

from swim_utils import *

def getNames(FOLDER): # List all names in the folder
    unique_names = set()
    for filename in os.listdir(FOLDER):
        result = get_swimmers_data(filename)
        name = result[0]
        if name not in unique_names:
            unique_names.add(name)

    return unique_names 

def list_swimmer_events(FOLDER, name): # get all events from a swimmer

    swimmers_event = set()
    for filename in os.listdir(FOLDER):
        result = get_swimmers_data(filename)
        event = result[2] + " " + result[3]
        if name in filename:
            swimmers_event.add(event) 
    
    return list(swimmers_event)