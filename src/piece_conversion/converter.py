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


def piece_to_csv(file_name):
  path = os.path.join("midi_pieces", file_name)
  piece = converter.parse(path)
  file = [x for x in piece.parts[0].flat.stripTies()]

  components = []

  for element in file:
      
      if type(element)==note.Note:
          info = [element.pitch.midi, fraction_to_string(element.offset), fraction_to_string(element.quarterLength)]
          components.append(info)
            
      elif type(element)==chord.Chord:
          chord_notes = element.notes
          for i in chord_notes:
              info = [i.pitch.midi, fraction_to_string(element.offset), fraction_to_string(element.quarterLength)]
              components.append(info)
          
      elif type(element)==note.Rest:     
          info = ['r', fraction_to_string(element.offset), fraction_to_string(element.quarterLength)]
          components.append(info)


  csv_name = file_name[:-4] +'.csv'
  if not os.path.isdir('csvs'):
      os.mkdir('csvs')
  csv_path = os.path.join('csvs', csv_name)
  with open(csv_path, 'w') as f:
      write = csv.writer(f)
      write.writerows(components)



path = os.path.join("midi_pieces")
pieces_list = []

# Iterate directory
for file in os.listdir(path):
    # check if current path is a file
    if os.path.isfile(os.path.join(path, file)) and '.mid' in file:
        pieces_list.append(file)
pieces_list.sort()

for file in pieces_list:
  piece_to_csv(file)