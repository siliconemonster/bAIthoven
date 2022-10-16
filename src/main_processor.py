from test_new_approach import *
from testing import *
import os
import csv


# --------------- Parse sonates ---------------

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

    break

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

splitted_string = string_of_every_piece.split(',')

raw_entry = sorted(set(item for item in splitted_string))
event_into_int_dict = dict((note, number) for number, note in enumerate(raw_entry))

#print(event_into_int_dict)

translated_string = ''
for item in splitted_string:
    translated_string = translated_string + str(event_into_int_dict[item]) + ','

translated_string = translated_string[:-1]

#print(translated_string)


# --------------- Build outcome into musical piece ---------------

int_into_event_dict = {value: key for key, value in event_into_int_dict.items()}
#print(int_into_event_dict)

translated_flat_list = []

for item in translated_string.split(','):
    parsed_item = int(item)
    translated_flat_list.append(int_into_event_dict[parsed_item])

#print(translated_flat_list)

no_chord_no_tuplet_output = []

second_positions_3_pos = 'Tempo', 'Tonalidade', 'Formula de Compasso'
second_positions_6_pos = 'Note', 'Rest', 'Chord'

for index, element in enumerate(translated_flat_list):
    if any(keyword in element for keyword in second_positions_3_pos):
        info = [translated_flat_list[index-1], element, translated_flat_list[index+1]]
        no_chord_no_tuplet_output.append(info)
    elif 'Tuplet' in element:
        info = [translated_flat_list[index-1], element, translated_flat_list[index+1],translated_flat_list[index+2],translated_flat_list[index+3],translated_flat_list[index+4]]
        no_chord_no_tuplet_output.append(info)
    elif any(keyword in element for keyword in second_positions_6_pos):
        info = [translated_flat_list[index-1], element, translated_flat_list[index+1],translated_flat_list[index+2],translated_flat_list[index+3],translated_flat_list[index+4]]
        no_chord_no_tuplet_output.append(info)

#print(no_chord_no_tuplet_output)

outcome = prepare_for_rebuilding(no_chord_no_tuplet_output)

print(outcome)

