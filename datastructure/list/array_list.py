import json

def new_list():
    new_list = {
        "size": 0,
        "elements": []
    }
    return new_list

def size(my_list):
    return my_list.get("size")

def load_list(my_list, filename):
    if (my_list is not None and filename is not None):
        with open(filename) as f:
            json_file = json.load(f)

        for element in json_file:
            add_last(my_list, element)
    return (my_list)
    
def add_last(my_list, element):
    my_list["elements"].append(element)
    my_list["size"] += 1