from test_new_approach import *
from testing import *
import os
import csv

xml_path = os.path.join("pieces")

list_of_every_piece = []


for file in os.listdir(xml_path):

    filename = os.path.join(xml_path, file)

    txt_name = file[:-4]
    if not os.path.isdir('outcome_txts'):
        os.mkdir('outcome_txts')
    path_and_name = os.path.join("outcome_txts", txt_name)

    final_list = extract_data(filename, new_filename=path_and_name)

    print(file + ' correctly transformed')

    txt_path = os.path.join("outcome_txts", txt_name + '.txt')

    txt_list = []

    with open(txt_path, 'r') as f:
        for line in f:
            txt_list.append(eval(line.strip()))
    
    if not os.path.isdir('csvs'):
        os.mkdir('csvs')
    csv_path = os.path.join("csvs", txt_name + '.csv')

    with open(csv_path, 'w', newline='') as f:
        write = csv.writer(f)
        write.writerows(txt_list)


    path_to_read = os.path.join(csv_path)

    sonate = read_from_csv(path_to_read)
    outcome = prepare_for_learning(sonate)

    list_of_every_piece.append(outcome)

flatten_list = []
string_of_every_piece = ''
for sonate in list_of_every_piece:
    for event in sonate:
        for element in event:
            flatten_list.append(element)
            string_of_every_piece = string_of_every_piece + str(element) + ','

string_of_every_piece = string_of_every_piece[:-1]

#print(flatten_list)
#print(string_of_every_piece)

raw_entry = sorted(set(item for item in string_of_every_piece.split(',')))
event_into_int = dict((note, number) for number, note in enumerate(raw_entry))

print(event_into_int)


