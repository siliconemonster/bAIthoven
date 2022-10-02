from fractions import Fraction
from music21 import *
import re
import csv
import os

def fraction_to_string(data):

  if isinstance(data, Fraction):
    result = str(data.numerator) + '/' + str(data.denominator)
  else: result = data
  return result

def string_to_fraction(data):
  if '/' in data:
    slash_position = data.find('/')
    
    result = Fraction(int(data[0:slash_position]), int(data[slash_position+1:]))
  else: result = data
  return result

def piece_to_csv(file_name):
  path = os.path.join("midi_pieces", file_name)
  piece = converter.parse(path)
  file = [x for x in piece.parts[0].flat.stripTies()]

  components = []

  for element in file:
      
      if type(element)==note.Note:
          info = [element.pitch.midi, fraction_to_string(element.quarterLength), fraction_to_string(element.offset)]
          components.append(info)
            
      elif type(element)==chord.Chord:
          chord_notes = element.notes
          for i in chord_notes:
              info = [i.pitch.midi, fraction_to_string(element.quarterLength), fraction_to_string(element.offset)]
              components.append(info)
          
      elif type(element)==note.Rest:     
          info = ['r', fraction_to_string(element.quarterLength), fraction_to_string(element.offset)]
          components.append(info)

  csv_name = file_name[:-4] +'.csv'
  if not os.path.isdir('csvs'):
      os.mkdir('csvs')
  csv_path = os.path.join('csvs', csv_name)
  
  with open(csv_path, 'w', newline='') as f:
      write = csv.writer(f)
      write.writerows(components)

def csv_to_string(csvs_list):
  all_sonatas_string = ''

  for a_csv_file in csvs_list:
    file_path = "csvs/" + a_csv_file
    with open(file_path) as csv_file:
      csv_reader = csv.reader(csv_file, delimiter=',')
      for row in csv_reader:
        for i in range(len(row)):
          all_sonatas_string += row[i]
          all_sonatas_string += ','
  
  all_sonatas_string = all_sonatas_string[:-1]
  return all_sonatas_string


def csv_to_piece():
  final_piece_csv = os.path.join("outcome_csv.csv")

  final_piece_score = stream.Score(id='mainScore')

  final_piece_score_part0 = stream.Part(id='part0')

  with open(final_piece_csv) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
      if row[0] == 'r':
        this_note = note.Rest()
      else:
        this_note = note.Note(int(row[0]))
      this_note.offset = float(string_to_fraction(row[1]))
      this_note.quarterLength = float(string_to_fraction(row[2]))

      final_piece_score_part0.append(this_note)

  final_piece_score.insert(0,final_piece_score_part0)

  final_piece_score.write('musicxml', 'outcome.mxl')


# ----- Creating CSV files -----
midi_path = os.path.join("midi_pieces")
pieces_list = []

# Iterate directory
for file in os.listdir(midi_path):
    # check if current path is a file
    if os.path.isfile(os.path.join(midi_path, file)) and '.mid' in file:
        pieces_list.append(file)
pieces_list.sort()

for file in pieces_list:
  piece_to_csv(file)

# ----- Converting CSV files into a long string -----
csvs_path = os.path.join("csvs")
csvs_list = []

# Iterate directory
for file in os.listdir(csvs_path):
    # check if current path is a file
    if os.path.isfile(os.path.join(csvs_path, file)) and '.csv' in file:
        csvs_list.append(file)
csvs_list.sort()

all_sonatas_string = csv_to_string(csvs_list)
print(all_sonatas_string)

# ----- Creating MXL file from prediction -----
csv_to_piece()