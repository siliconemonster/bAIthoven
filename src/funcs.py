import math
from fractions import Fraction
import music21 as m21
from music21.common.numberTools import opFrac
import abjad
from collections import defaultdict

def find_other_components(filename):
  piece = m21.converter.parse(filename).voicesToParts()
  result = []
  flat_piece = piece.flat
  wanted_types = (m21.meter.TimeSignature, m21.key.Key, m21.tempo.MetronomeMark)
  for x in flat_piece:
    if type(x) not in wanted_types:
      pass
    else:
      if type(x) == m21.meter.TimeSignature:
        el = [Fraction(opFrac(x.offset)), "Formula de Compasso", x.ratioString]
      elif type(x) == m21.key.Key:
        el = [Fraction(opFrac(x.offset)), "Tonalidade", x.tonic.name + " " + x.mode]
      elif type(x) == m21.tempo.MetronomeMark: 
        el = [Fraction(opFrac(x.offset)), "Tempo", x.number]
      if el not in result:
        result.append(el)
  return result


def extract_parts(filename):
  piece = m21.converter.parse(filename).voicesToParts()
  for part in piece.parts:
    part.makeRests(fillGaps=True, inPlace=True)
  all_parts_raw = [x.flat for x in piece.parts]
  parts = []
  for raw_part in all_parts_raw:
      part_list = [x for x in raw_part if type(x) in (m21.note.Note,m21.note.Rest,m21.chord.Chord)]
      parts.append(m21.stream.Stream(part_list))
  return parts


def parse_element(el, noTups=False):
  if noTups == False:
    dur = Fraction(opFrac(el.duration.quarterLength))
  else:
    dur = Fraction(opFrac(el.duration.quarterLengthNoTuplets))
  off = Fraction(opFrac(el.offset))
  tie_type = el.tie
  if tie_type != None:
    tie_type = tie_type.type
  if type(el) == m21.note.Note:
    type_name = "Note"
    type_pitch = el.pitch.midi
  elif type(el) == m21.note.Rest:
    type_name = "Rest"
    type_pitch = 0
  elif type(el) == m21.chord.Chord:
    type_name = "Chord"
    type_pitch = [y.midi for y in el.pitches]
  return [off,type_name,dur,type_pitch, tie_type]


def group_tuplets(parte):
    tup_fix = m21.duration.TupletFixer(parte)
    tupletGroups = tup_fix.findTupletGroups(incorporateGroupings=True)
    if len(tupletGroups) == 0:
      return [x for x in parte]

    start_end_indexes = []
    start_indexes = []
    end_indexes = []

    for x in tupletGroups:
        start_indexes.append(parte.index(x[0]))
        end_indexes.append(parte.index(x[-1]))


    new_part = []
    i = 0
    while i < len(parte):
        if i not in start_indexes:
            new_part.append(parte[i])
            i += 1
        else:
            start_ind = i
            end_ind = end_indexes[start_indexes.index(i)]
            group = [parte[k] for k in range(start_ind, end_ind+1)]
            new_part.append(group)
            i += len(group)
    return new_part


def parse_with_tuplets(parte):
  group = group_tuplets(parte)
  result = []
  for x in group:
    if type(x) != list:
      el = parse_element(x)
      result.append(el)
    else:
      parsed_el = [parse_element(y,noTups=True) for y in x]
      off = parsed_el[0][0]
      dur_mult = Fraction(x[0].duration.tuplets[0].tupletMultiplier())
      num = dur_mult.numerator
      den = dur_mult.denominator
      ratio_string = str(den) + ":" + str(num)
      name_string = "Tuplet " + ratio_string
      result.append([off, name_string, [y[1:] for y in parsed_el]])
  return result


def create_parts_dict(raw_parts):
  parsed_parts = [parse_with_tuplets(x) for x in raw_parts]
  parts = dict()
  for i, part in enumerate(parsed_parts):
    part_dict = {el[0]:el[1:] for el in part}
    parts[f"part_{i+1}"] = part_dict
  return parts

def find_all_offsets(parts):
  all_offsets = []
  for p in parts:
    all_offsets += list(parts[p].keys())
  all_offsets = sorted(list(set(all_offsets)))
  return all_offsets

def create_offset_dict(all_offsets, parts):
  parts_dict = defaultdict(list)
  for off in all_offsets:
    for p in parts:
        if off in parts[p].keys():
            parts_dict[off].append(parts[p][off])
        else:
            parts_dict[off].append("X")
  return parts_dict

def add_components(components, offset_dict):
  for off in components:
      offset_dict[off].append(components[off])
  return

def m21toabjad(x):

  result = []
  type_el = x[1]
  dur = x[3] / 4
  if type_el == "Note":
    nota = abjad.Note()
    nota.written_duration = dur
    pitch = abjad.NamedPitch(x[4] - 60)
    nota.written_pitch = pitch
  elif type_el == "Rest":
    nota = abjad.Rest(dur)
  elif type_el == "Chord":
    nota = abjad.Chord()
    nota.written_duration = dur
    pitches = [abjad.NamedPitch(y-60) for y in x[4]]
    nota.written_pitches = pitches
  if x[5] in ("start", "continue"):
    abjad.attach(abjad.Tie(),nota)
  result.append(nota)
  return result

def m21toabjadtuplet(comp):
  indvididual_notes = comp[3]
  for group in indvididual_notes:
    group.insert(0, "x")
    group.insert(2, "x")
  new_notas = [m21toabjad(y) for y in indvididual_notes]
  cont = abjad.Container(new_notas)
  ratio_string = comp[1].split(" ")[1]
  num, den = int(ratio_string.split(":")[0]),int(ratio_string.split(":")[1])
  leaves = abjad.select.leaves(cont)
  tup = abjad.Tuplet((den,num), [])
  tuplet = abjad.mutate.wrap(leaves, tup)
  return cont

def create_indicator(el):
  if el[1] == "Tempo":
    ind = abjad.MetronomeMark((1,4),int(el[2]))
  elif el[1] == "Formula de Compasso":
    num, den = int(el[2].split("/")[0]), int(el[2].split("/")[1])
    ind = abjad.TimeSignature((num,den))
  elif el[1] == "Tonalidade":
    fullname_pitch = el[2].split(" ")[0]
    if len(fullname_pitch) == 2:
      new_name = fullname_pitch[0].lower()
      if fullname_pitch[1] == "-":
        new_name += "f"
      elif fullname_pitch[1] == "=":
        new_name += "#"
    else:
      new_name = fullname_pitch.lower()
    mode = el[2].split(" ")[1]
    ind = abjad.KeySignature(
    abjad.NamedPitchClass(new_name), abjad.Mode(mode)
    )

  return ind


def find_indicators(master_list):
  indicators = [x for x in master_list if x[1] in ("Tempo", "Formula de Compasso", "Tonalidade", "Volta")]
  return indicators

def find_components(master_list, indicators):
  comps = [x for x in master_list if x not in indicators]
  return comps


def make_parts_lists(components):
  result = defaultdict(list)
  for comp in components:
    result[comp[2]].append(comp)
  return result 


def merge_comps_inds(components, indicators):
  res_list = defaultdict(list)
  for c in components:
    res_list[c[0]].append(c)
  for i in indicators:
    res_list[i[0]].append(i)
  return res_list