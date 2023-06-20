import csv
import os
import shutil
from fractions import Fraction
from testing import *
import math as m
import pickle

# ###### Input Arranging ######
  
def _read_from_csv(path):
  with open(path, newline='') as f:
    reader = csv.reader(f)
    data = list(reader)
    
    whole_list = []

    for event in data:
      row = []
      for index, element in enumerate(event):
        if index == 1 or index == 2:
          row.append(element)
        elif index == 5 and element != '':
          row.append(element)
        elif element == '':
          row.append(None)
        else:
          if '/' in element:
            slash_position = element.find('/')
            row.append(Fraction(int(element[0:slash_position]), int(element[slash_position+1:])))
          else: row.append(eval(element))
      whole_list.append(row)

    return whole_list

def _separate_tuplets(raw_tuplet):
  separated_tupltes = []
  for event in raw_tuplet[3]:
    if 'Chord' in event[0]:
      info = [raw_tuplet[0], raw_tuplet[1]+' - '+event[0]+' ='+str(len(event[2])), raw_tuplet[2], event[1], event[2], event[3]]
    else:
      info = [raw_tuplet[0], raw_tuplet[1]+' - '+event[0], raw_tuplet[2], event[1], event[2], event[3]]
    separated_tupltes.append(info)
  return separated_tupltes

def _separate_chords(raw_chord):
  separated_chord = []
  for note in raw_chord[4]:
    info = [raw_chord[0], raw_chord[1], raw_chord[2], raw_chord[3], note, raw_chord[5]]
    separated_chord.append(info)
  return separated_chord

def _remove_fractions(no_chords_list):
  no_fractions_list = []

  for event in no_chords_list:
    info = []
    for idx, element in enumerate(event):
      if isinstance(element, Fraction) == True:
        info.append(element.numerator)
        info.append(element.denominator)
      elif idx == 0 or idx == 3:
        info.append(int(element))
        info.append(1)
      else: info.append(element)
    no_fractions_list.append(info)


  return no_fractions_list

def _convert_none_to_str(no_fractions_list):
  converted_none_list = []
  for event in no_fractions_list:
    if event[7] == None:
      new_event = [event[0], event[1], event[2], event[3], event[4], event[5], event[6], 'None']
      converted_none_list.append(new_event)
    else:
      converted_none_list.append(event)

  #print('This is the sonate with None entries converted to string')
  #print(converted_none_list)
  #print()

  return converted_none_list

def _prepare_for_learning(whole_list):
  no_header_list = []
  for event in whole_list:
    if 'Tempo' in event[1] or 'Formula de Compasso' in event[1]:
      continue
    else: no_header_list.append(event)

  # print('This is the sonate without a header')
  # print(no_header_list)
  # print()

  no_tuplets_list = []
  for event in no_header_list:
    if 'Tuplet' in event[1]:
      separated_tuplets = _separate_tuplets(event)
      for element in separated_tuplets:
        no_tuplets_list.append(element)
    else:
      no_tuplets_list.append(event)

  #print('This is the sonate with all the tuplets separated')
  #print(no_tuplets_list)
  #print()

  no_chords_list = []
  for event in no_tuplets_list:
    if 'Chord' in event[1]:
      separated_chords = _separate_chords(event)
      for element in separated_chords:
        no_chords_list.append(element)
    else:
      no_chords_list.append(event)

  #print('This is the sonate with all the tuplets and chords separated')
  #print(no_chords_list)
  #print()

  no_fractions_list = _remove_fractions(no_chords_list)

  #print('This is the sonate with the time information split into num and denom')
  #print(no_fractions_list)
  #print()

  converted_none_list = _convert_none_to_str(no_fractions_list)


  return converted_none_list

def _delete_temp_folders():
  shutil.rmtree('csvs')
  shutil.rmtree('outcome_txts')  

def _save_list_to_file(real_list, file_name):
  with open(file_name, 'w') as fp:
    for item in real_list:
      # write each item on a new line
      fp.write("%s\n" % item)

def _remove_denom(all_sonates_list):
  offset_denom = set()
  duration_denom = set()
  for sonate in all_sonates_list:
    for event in sonate:
      offset_denom.add(event[1])
      duration_denom.add(event[5])

  offset_lcm = m.lcm(*offset_denom)
  duration_lcm = m.lcm(*duration_denom)

  lcm_dict = {'offset_lcm': offset_lcm, 'duration_lcm': duration_lcm}
  with open('offsets.pkl', 'wb') as fp:
    pickle.dump(lcm_dict, fp)


  non_linear_no_denom_list = []
  for sonate in all_sonates_list:
    no_denom_sonate = []
    for event in sonate:
      offset_quot = offset_lcm / event[1]
      new_offset_num = int(event[0] * offset_quot)
      duration_quot = duration_lcm / event[5]
      new_duration_num = int(event[4] * duration_quot)

      temp = [new_offset_num, event[2], event[3], new_duration_num, event[6], event[7]]
      no_denom_sonate.append(temp)
    non_linear_no_denom_list.append(no_denom_sonate)

  return non_linear_no_denom_list

def _translate_to_int(no_denom_list):

  event_name_list = []
  part_list = []
  tie_list= []

  for sonate in no_denom_list:
    for event in sonate:
      event_name_list.append(event[1])
      part_list.append(event[2])
      tie_list.append(event[5])

  event_name_set = sorted(set(item for item in event_name_list))
  part_set = sorted(set(item for item in part_list))
  tie_set = sorted(set(item for item in tie_list))

  event_name_dict = dict((event, number) for number, event in enumerate(event_name_set))
  part_dict = dict((event, number) for number, event in enumerate(part_set))
  tie_dict = dict((event, number) for number, event in enumerate(tie_set))

  with open('event_name_dict.pkl', 'wb') as fp:
    pickle.dump(event_name_dict, fp)
  with open('part_dict.pkl', 'wb') as fp:
    pickle.dump(part_dict, fp)
  with open('tie_dict.pkl', 'wb') as fp:
    pickle.dump(tie_dict, fp)

  all_sonates_int_list = []
  for sonate in no_denom_list:
    sonate_int_list = []
    for event in sonate:
      temp_event_name = event_name_dict[event[1]]
      temp_part = part_dict[event[2]]
      temp_tie = tie_dict[event[5]]
      temp_full_event = [event[0], temp_event_name, temp_part, event[3], event[4]]
      sonate_int_list.append(temp_full_event)
    all_sonates_int_list.append(sonate_int_list)

  #print('This is the sonate only with integers')
  #print(all_sonates_int_list)
  #print()

  #_save_list_to_file(all_sonates_int_list, 'all_sonates_int_list.txt')

  return all_sonates_int_list

def _flatten_list(all_sonates_int_list):

  flattened_list = []
  count = 0
  for sonate in all_sonates_int_list:
    count = count + 1
    for event in sonate:
      for element in event:
        flattened_list.append(element)

  #print('This is the flatten list:')
  #print(flattened_list)
  #print()

  #_save_list_to_file(flattened_list, 'flattened_list.txt')

  return flattened_list, count

def rearrange_initial_data():

    xml_path = os.path.join("pieces")

    all_sonates_list = []


    for file in os.listdir(xml_path):

        filename = os.path.join(xml_path, file)

        txt_name = file[:-4]
        if not os.path.isdir('outcome_txts'):
            os.mkdir('outcome_txts')
        path_and_name = os.path.join("outcome_txts", txt_name)

        extract_data(filename, new_filename=path_and_name)

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

        sonate = _read_from_csv(path_to_read)
        #print('This is the sonate that was read from the CSV:')
        #print(sonate)
        #print()
        outcome = _prepare_for_learning(sonate)

        all_sonates_list.append(outcome)

    _delete_temp_folders()
    
    #_save_list_to_file(all_sonates_list, 'all_sonates_list.txt')
    no_denom_list = _remove_denom(all_sonates_list)
    all_sonates_int_list = _translate_to_int(no_denom_list)  
    flattened_list, count = _flatten_list(all_sonates_int_list) 

    print('\nAll the', count, 'pieces have been correctly collected.')
    n_vocab = len(set(flattened_list))
    print('The size of the vocabulary is of', n_vocab, 'elements.\n')
    
    return flattened_list, n_vocab



# ###### Output Arranging ######

def _reverse_translate(sonate):
  output = []

  with open('offsets.pkl', 'rb') as fp:
    offsets_dict = pickle.load(fp)
  with open('event_name_dict.pkl', 'rb') as fp:
    event_name_dict = pickle.load(fp)
  inv_event_name_dict = dict(zip(event_name_dict.values(), event_name_dict.keys()))
  with open('part_dict.pkl', 'rb') as fp:
    part_dict = pickle.load(fp)
  inv_part_dict = dict(zip(part_dict.values(), part_dict.keys()))
  with open('tie_dict.pkl', 'rb') as fp:
    tie_dict = pickle.load(fp)
  inv_tie_dict = dict(zip(tie_dict.values(), tie_dict.keys()))

  for event in sonate:
    offset = Fraction(event[0],offsets_dict['offset_lcm'])
    event_name = inv_event_name_dict[event[1]]
    part = inv_part_dict[event[2]]
    duration = Fraction(event[3],offsets_dict['duration_lcm'])

    output.append([offset, event_name, part, duration, event[4], None])

  return output

def _rejoin_chords(whole_piece):
  flag_tuplet_chord = 1
  chord_list = []
  for index, event in enumerate(whole_piece):
    notes = []
    if event[1] == 'Chord':
      count = 0
      if event[0] == whole_piece[index-1][0] and event[1] == whole_piece[index-1][1] and event[2] == whole_piece[index-1][2]:
        continue
      else:
        # respeitar o tamanho + próximo ser chord também + próximo ser mesma Part + próximo ter mesmo offset
        while index+count+1 < len(whole_piece) and event[1] == whole_piece[index+count+1][1] and event[2] == whole_piece[index+count+1][2] and event[0] == whole_piece[index+count+1][0]:
          whole_piece[index+count].append('flagged')
          notes.append(whole_piece[index+count][4])
          count = count + 1
        notes.append(whole_piece[index+count][4])
        whole_piece[index+count][4] = notes

    elif 'Chord' in event[1]:
      
      tuplet_info = event[1].split()
      total = int(tuplet_info[4][1])

      if flag_tuplet_chord == total:
        event[1] = 'Tuplet '+ tuplet_info[1] +' - Chord'
        chord_list.append(event[4])
        event[4] = chord_list

        chord_list = []
        flag_tuplet_chord = 1
      else:
        chord_list.append(event[4])
        event.append('flagged')
        flag_tuplet_chord = flag_tuplet_chord + 1

  for event in whole_piece.copy():
    if 'flagged' in event:
      whole_piece.remove(event)

  return whole_piece

def _rejoin_tuplets(whole_piece):
  flag_tuplet = 1
  tuplet_list = []
  total = 1
  count = 0
  for index, event in enumerate(whole_piece):
    if 'Tuplet' in event[1]:      
      tuplet_info = event[1].split()
      info = [tuplet_info[3], event[3], event[4], event[5]]
      tuplet_list.append(info)

      tuplet_comparer = tuplet_info[0] + ' ' + tuplet_info[1]

      while index+count+1 < len(whole_piece) and tuplet_comparer in whole_piece[index+count+1][1] and event[2] == whole_piece[index+count+1][2] and event[0] == whole_piece[index+count+1][0]:
        count = count + 1
        total = total + 1

      if flag_tuplet == total:
        event[1] = 'Tuplet ' + tuplet_info[1]
        event[3] = tuplet_list

        event.pop()
        event.pop()

        tuplet_list = []
        flag_tuplet = 1
        total = 1
        count = 0
      else:
        event.append('flagged')
        flag_tuplet = flag_tuplet + 1

  for event in whole_piece.copy():
    if 'flagged' in event:
      whole_piece.remove(event)

  return whole_piece

def _adjust_output(sonate):

  for event in sonate:
    if 'Tuplet' in event[1]:
      for tuplet in event[3]:
        if tuplet[2] == 0 and tuplet[0] != 'Rest':
          tuplet[0] = 'Rest'
        if tuplet[2] != 0 and tuplet[0] == 'Rest':
          tuplet[0] = 'Note'
        if tuplet[0] == 'Chord':
          tuplet[2] = list(sorted(set(tuplet[2])))
          if 0 in tuplet[2]:
            if tuplet[2] == [0]:
              tuplet[0] = 'Rest'
              tuplet[2] = 0
              continue
            else:
              tuplet[2].remove(0)
          if len(tuplet[2]) == 1:
            tuplet[0] = 'Note'
            tuplet[2] = tuplet[2][0]

      continue

    if event[4] == 0 and event[1] != 'Rest':
      event[1] = 'Rest'
    if event[4] != 0 and event[1] == 'Rest':
      event[1] = 'Note'
    if event[1] == 'Chord':
      event[4] = list(sorted(set(event[4])))
      if 0 in event[4]:
        if event[4] == [0]:
          event[1] = 'Rest'
          event[4] = 0
          continue
        else:
          event[4].remove(0)
      if len(event[4]) == 1:
        event[1] = 'Note'
        event[4] = event[4][0]

  return sonate

def _adjust_joined_tuplets(sonate):
  adjusted_sonate = []
  for event in sonate:
    if 'Tuplet' in event[1]:
      notes = event[1].split()[1]
      how_many_notes = int(notes.split(':')[0])

      if len(event[3]) < how_many_notes:
        while len(event[3]) < how_many_notes:
          event[3].append(event[3][-1])
        adjusted_sonate.append(event)
      elif len(event[3]) == how_many_notes:
        adjusted_sonate.append(event)
      elif len(event[3]) > how_many_notes:
        temp_tuplets = []

        for i in range(0,len(event[3]), how_many_notes):
          temp_tuplets.append(event[3][i:i+how_many_notes])

        temp_event = []
        for tup in temp_tuplets:
          if len(tup) < how_many_notes:
            while len(tup) < how_many_notes:
              tup.append(tup[-1])
            temp_event = [event[0], event[1], event[2], tup]
          elif len(tup) == how_many_notes:
            temp_event = [event[0], event[1], event[2], tup]
                  
          adjusted_sonate.append(temp_event)

    else:
      adjusted_sonate.append(event)

  return adjusted_sonate

def _order_offsets(sonate):
  parts_next_offset = ['empty', Fraction(0,1), Fraction(0,1), Fraction(0,1), Fraction(0,1), Fraction(0,1), Fraction(0,1)]
  parts_next_duration = ['empty', Fraction(0,1), Fraction(0,1), Fraction(0,1), Fraction(0,1), Fraction(0,1), Fraction(0,1)]
  full_measure = Fraction(4,1)
  increment = Fraction(1,100)
  previous_measure = -1
  current_measure = 1

  for event in sonate:
    current_measure = int(1 + (parts_next_offset[int(event[2][-1])]+ increment)/full_measure)

    if current_measure != previous_measure:
      index_to_skip = int(event[2][-1])
      for i in range(len(parts_next_offset)):
        if i != 0  and i != index_to_skip:
          if parts_next_offset[index_to_skip] > parts_next_offset[i]:
            parts_next_offset[i] = parts_next_offset[index_to_skip]
          else:
            parts_next_offset[i] = parts_next_offset[i]

    event[0] = parts_next_offset[int(event[2][-1])]
    
    if 'Tuplet' in event[1]:
      parts_next_duration[int(event[2][-1])] = event[3][0][1]

    else:
      parts_next_duration[int(event[2][-1])] = event[3]
    parts_next_offset[int(event[2][-1])] = event[0] + parts_next_duration[int(event[2][-1])]

    previous_measure = current_measure

  
    

  return sonate


def _add_generic_header(sonate):
  final_piece = []

  final_piece.append([Fraction(0,1), 'Tempo', '120.0'])
  final_piece.append([Fraction(0,1), 'Formula de Compasso', '4/4'])
  for event in sonate:
    final_piece.append(event)

  return final_piece

def rebuild_piece(sonate):

  split_chords_list = _reverse_translate(sonate)

  #print('This is the sonate translated from ints to musical terms')
  #print(split_chords_list)
  #print()

  split_tuplets_list = _rejoin_chords(split_chords_list)

  #print('This is the sonate with all the chords rebuilt')
  #print(split_tuplets_list)
  #print()

  no_header_list = _rejoin_tuplets(split_tuplets_list)

  #print('This is the sonate with all the chords and tuplets rebuilt')
  #print(no_header_list)
  #print()

  halfway_adjusted_list = _adjust_output(no_header_list)
  adjusted_list = _adjust_joined_tuplets(halfway_adjusted_list)
  ordered_adjusted_list = _order_offsets(adjusted_list)

  #print('This is the adjusted sonate ')
  #print(ordered_adjusted_list)
  #print()

  piece = _add_generic_header(ordered_adjusted_list)

  print('This is the produced sonate')
  print(piece)
  #print()

  return piece