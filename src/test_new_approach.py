import csv
import os
from fractions import Fraction
  
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

def rejoin_chords(whole_piece):
  flag_tuplet_chord = 1
  chord_list = []
  for index, event in enumerate(whole_piece):
    notes = []
    if event[1] == 'Chord':
      count = 0
      if event[0] == whole_piece[index-1][0] and event[2] == whole_piece[index-1][2]:
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
  no_tuplets_list = []
  for event in whole_list:
    if 'Tuplet' in event[1]:
      separated_tuplets = separate_tuplets(event)
      for element in separated_tuplets:
        no_tuplets_list.append(element)
    else:
      no_tuplets_list.append(event)

  # print('This is the sonate with all the tuplets separated')
  # print(no_tuplets_list)
  # print()

  no_chords_list = []
  for event in no_tuplets_list:
    if 'Chord' in event[1]:
      separated_chords = separate_chords(event)
      for element in separated_chords:
        no_chords_list.append(element)
    else:
      no_chords_list.append(event)

  # print('This is the sonate with all the tuplets and chords separated')
  # print(no_chords_list)
  # print()

  return no_chords_list

def prepare_for_rebuilding(no_chords_list):
  chords_list = rejoin_chords(no_chords_list)

  # print('This is the sonate with all the chords rebuilt')
  # print(chords_list)
  # print()

  rebuilt_list = rejoin_tuplets(chords_list)
  
  # print('This is the sonate with all the chords and tuplets rebuilt')
  # print(rebuilt_list)
  # print()

  return rebuilt_list

'''path_to_read = os.path.join('converted_sonates','csv_file.csv')

sonate = read_from_csv(path_to_read)
#print(sonate)
outcome = prepare_for_learning(sonate)

prepare_for_rebuilding(outcome)
write_to_csv(outcome)'''