import csv
import os
from fractions import Fraction
from testing import *
  
def read_from_csv(path):
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

def separate_tuplets(raw_tuplet):
  separated_tupltes = []
  for event in raw_tuplet[3]:
    if 'Chord' in event[0]:
      info = [raw_tuplet[0], raw_tuplet[1]+' - '+event[0]+' ='+str(len(event[2])), raw_tuplet[2], event[1], event[2], event[3]]
    else:
      info = [raw_tuplet[0], raw_tuplet[1]+' - '+event[0], raw_tuplet[2], event[1], event[2], event[3]]
    separated_tupltes.append(info)
  return separated_tupltes

def separate_chords(raw_chord):
  separated_chord = []
  for note in raw_chord[4]:
    info = [raw_chord[0], raw_chord[1], raw_chord[2], raw_chord[3], note, raw_chord[5]]
    separated_chord.append(info)
  return separated_chord

def remove_fractions(no_chords_list):
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

def rebuild_fractions(no_fractions_list):
  no_chords_list = []

  header = 'Tempo', 'Tonalidade', 'Formula de Compasso'
  
  for event in no_fractions_list:
    if event[1] == 1:
      offset = int(event[0])
    else:
      offset = Fraction(event[0],event[1])

    if any(keyword in event[2] for keyword in header):
      info = [offset, event[2], event[3]]
    else:
      if event[5] == 1:
        duration = int(event[4])
      else:
        duration = Fraction(event[4],event[5])
      info = [offset, event[2], event[3], duration, event[6], event[7]]
    no_chords_list.append(info)

  return no_chords_list

def rejoin_chords(whole_piece):
  flag_tuplet_chord = 1
  chord_list = []
  for index, event in enumerate(whole_piece):
    notes = []
    if event[2] == 'Chord':
      count = 0
      if event[0] == whole_piece[index-1][0] and event[2] == whole_piece[index-1][2] and event[3] == whole_piece[index-1][3]:
        continue
      else:
        # respeitar o tamanho + próximo ser chord também + próximo ser mesma Part + próximo ter mesmo offset
        while index+count+1 < len(whole_piece) and event[2] == whole_piece[index+count+1][2] and event[3] == whole_piece[index+count+1][3] and event[0] == whole_piece[index+count+1][0] and event[1] == whole_piece[index+count+1][1]:
          whole_piece[index+count].append('flagged')
          notes.append(whole_piece[index+count][5])
          count = count + 1
        notes.append(whole_piece[index+count][5])
        whole_piece[index+count][5] = notes

    elif 'Chord' in event[2]:
      
      tuplet_info = event[2].split()
      total = int(tuplet_info[4][1])

      if flag_tuplet_chord == total:
        event[2] = 'Tuplet '+ tuplet_info[1] +' - Chord'
        chord_list.append(event[5])
        event[5] = chord_list

        chord_list = []
        flag_tuplet_chord = 1
      else:
        chord_list.append(event[5])
        event.append('flagged')
        flag_tuplet_chord = flag_tuplet_chord + 1

  for event in whole_piece.copy():
    if 'flagged' in event:
      whole_piece.remove(event)

  return whole_piece

def rejoin_tuplets(whole_piece):
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

def write_to_csv(lista):

  if not os.path.isdir('csv_new_approach'):
    os.mkdir('csv_new_approach')
  csv_path = os.path.join('csv_new_approach', 'outcome.csv')


  with open(csv_path, 'w', newline='') as f:
    write = csv.writer(f)
    write.writerows(lista)

def prepare_for_learning(whole_list):
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
      separated_tuplets = separate_tuplets(event)
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
      separated_chords = separate_chords(event)
      for element in separated_chords:
        no_chords_list.append(element)
    else:
      no_chords_list.append(event)

  #print('This is the sonate with all the tuplets and chords separated')
  #print(no_chords_list)
  #print()

  no_fractions_list = remove_fractions(no_chords_list)

  #print('This is the sonate with the time information split into num and denom')
  #print(no_fractions_list)
  #print()

  converted_no_ties_list = []
  for event in no_fractions_list:
    new_event = [event[0], event[1], event[2], event[3], event[4], event[5], event[6]]
    converted_no_ties_list.append(new_event)
  
  #print('This is the sonate without tie info converted to string')
  #print(converted_no_ties_list)
  #print()

  return converted_no_ties_list

def prepare_for_rebuilding(no_fractions_list):

  no_chords_list = rebuild_fractions(no_fractions_list)

  #print('This is the sonate with the offset and duration rebuilt')
  #print(no_chords_list)
  #print()

  chords_list = rejoin_chords(no_chords_list)

  #print('This is the sonate with all the chords rebuilt')
  #print(chords_list)
  #print()

  rebuilt_list = rejoin_tuplets(chords_list)
  
  #print('This is the sonate with all the chords and tuplets rebuilt')
  #print(rebuilt_list)
  #print()

  return rebuilt_list

def rearrange_received_data():

    xml_path = os.path.join("pieces")

    list_of_every_piece = []


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

        sonate = read_from_csv(path_to_read)
        #print('This is the sonate that was read from the CSV:')
        #print(sonate)
        #print()
        outcome = prepare_for_learning(sonate)

        list_of_every_piece.append(outcome)

    flatten_list = []
    count = 0
    for sonate in list_of_every_piece:
      count = count + 1
      for event in sonate:
        for element in event:
          flatten_list.append(element)

    #print('This is the flatten list:')
    #print(flatten_list)
    #print()

    print('\nAll the', count, 'pieces have been correctly collected.')
    n_vocab = len(set(flatten_list))
    print('The size of the vocabulary is of', n_vocab, 'elements.\n')
    return flatten_list, n_vocab


def rearrange_outcome_sonata(sonata):
    #print('This is the sonata:')
    #print(sonata)
    #print()

    no_chord_no_tuplet_output = []

    second_positions_4_pos = 'Tempo', 'Tonalidade', 'Formula de Compasso'
    second_positions_8_pos = 'Note', 'Rest', 'Chord'

    for index, element in enumerate(sonata):
      if isinstance(element, str):
          if any(keyword in element for keyword in second_positions_4_pos):
              info = [sonata[index-2], sonata[index-1], element, sonata[index+1]]
              no_chord_no_tuplet_output.append(info)
          elif 'Tuplet' in element:
              info = [sonata[index-2], sonata[index-1], element, sonata[index+1],sonata[index+2],sonata[index+3],sonata[index+4],sonata[index+5]]
              no_chord_no_tuplet_output.append(info)
          elif any(keyword in element for keyword in second_positions_8_pos):
              info = [sonata[index-2], sonata[index-1], element, sonata[index+1],sonata[index+2],sonata[index+3],sonata[index+4],sonata[index+5]]
              no_chord_no_tuplet_output.append(info)

    print('This is the unflattened list:')
    print(no_chord_no_tuplet_output)
    print()

    outcome = prepare_for_rebuilding(no_chord_no_tuplet_output)

    print('This is the outcome:')
    print(outcome)
    print()

    with open('outcome_TBConverted.txt', 'w') as f:
      for item in outcome:
        f.write(str(item))
        f.write('\n')

def create_piece(outcome):
  #score = create_piece(outcome)
  #show_new_piece(score)
  return