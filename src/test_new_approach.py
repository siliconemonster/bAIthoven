import csv
import os
  
'''with open('csv_file', 'w', newline='') as f:
      
    # using csv.writer method from CSV package
    write = csv.writer(f)
    write.writerows(lista)'''

def read_from_csv(path):
  with open(path, newline='') as f:
    reader = csv.reader(f)
    data = list(reader)

    print(data)
    
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
          row.append(eval(element))
      whole_list.append(row)

    whole_list[0][2] = float(whole_list[0][2])
    return whole_list

def separate_tuplets(raw_tuplet):
  separated_tupltes = []
  for event in raw_tuplet[3]:
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
  for index, event in enumerate(whole_piece):
    notes = []
    if 'Chord' in event[1]:
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

  for event in whole_piece.copy():
    if 'flagged' in event:
      whole_piece.remove(event)

  return whole_piece

def rejoin_tuplets(whole_piece):
  rejoined_tupltes = []
  flag_tuplet = 1
  tuplet_list = []
  for event in whole_piece:
    if 'Tuplet' in event[1]:

      tuplet_info = event[1].split()
      info = [tuplet_info[3], event[3], event[4], event[5]]
      tuplet_list.append(info)

      if flag_tuplet == int(tuplet_info[1][0]):
        event[1] = 'Tuplet ' + tuplet_info[1]
        event[3] = tuplet_list

        event.pop()
        event.pop()

        tuplet_list = []
        flag_tuplet = 1
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

  print(no_tuplets_list)

  no_chords_list = []
  for event in no_tuplets_list:
    if 'Chord' in event[1]:
      separated_chords = separate_chords(event)
      for element in separated_chords:
        no_chords_list.append(element)
    else:
      no_chords_list.append(event)

  print(no_chords_list)

  return no_chords_list

def prepare_for_rebuilding(no_chords_list):
  chords_list = rejoin_chords(no_chords_list)
  print(chords_list)

  rebuilt_list = rejoin_tuplets(chords_list)
  print(rebuilt_list)

  return rebuilt_list

path_to_read = os.path.join('converted_sonates','csv_file.csv')

sonate = read_from_csv(path_to_read)
print(sonate)
outcome = prepare_for_learning(sonate)

prepare_for_rebuilding(outcome)
write_to_csv(outcome)