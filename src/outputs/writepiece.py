import music21 as m21
from fractions import Fraction
from output1E import output
from collections import defaultdict

def find_indicators(master_list):
    result = []
    for element in master_list:
        if len(element) == 3:
            result.append(element)
    return result

def normalize_tuplets(master_list):
    for element in master_list:
        if len(element) == 4:
            written_duration = sum([x[1] for x in element[3]])
            ratio_number = element[1].split(" ")[1]
            ratio = Fraction(f"{ratio_number.split(':')[0]}/{ratio_number.split(':')[1]}")
            duration = written_duration / ratio
            element.insert(3, duration)
            element.append(None)




def count_parts(master_list):
    part_names = []
    for element in master_list:
        if len(element) == 6:
            part_name = element[2]
            if part_name not in part_names:
                part_names.append(part_name)

    return sorted(part_names)

def separate_parts(master_list):
    names = count_parts(master_list)
    result = defaultdict(list)
    for element in master_list:
        result[element[2]].append(element)
        result[element[2]].sort(key=lambda x: x[0])
    return result

def first_and_last(master_list):
    names = count_parts(master_list)
    parts = separate_parts(master_list)
    offs = []
    for name in names:
        for part in parts[name]:
            offs.append(part[0])

    return min(offs), max(offs)

def fill_parts(master_list):
    names = count_parts(master_list)
    min_max = first_and_last(master_list)
    parts = separate_parts(master_list)

    for name in names:
        offs = [x[0] for x in parts[name]]
        offs.sort()
        if min_max[0] not in offs:
            parts[name].append([min_max[0], "Rest", name, offs[0]-min_max[0], 0, None])
        if min_max[1] not in offs:
            parts[name].append([min_max[1], "Rest", name, min_max[1]-offs[-1], 0, None])

        i = 0
        while i < len(parts[name]):
            cur_off = parts[name][i][0]
            correct_off = parts[name][i-1][0] + parts[name][i-1][3]
            if cur_off > correct_off:
                new_el = [correct_off, "Rest", name, cur_off-correct_off, 0, None]
                parts[name].insert(i-1, new_el)
                parts[name].sort()
                i += 1
            else:
                pass
            i += 1

    return parts

def process_element(element):
    # [offset, elemento, (indicador ou nota)]
    result = [element[0]]
    if element[1] == "Rest":
        el = m21.note.Rest()
        el.quarterLength = element[3]
        result.append(el)
        result.append("elemento")
    elif element[1] == "Note":
        el = m21.note.Note()
        el.pitch.midi = element[4]
        el.quarterLength = element[3]
        result.append(el)
        result.append("elemento")
    elif element[1] == "Chord":
        el = m21.chord.Chord()
        el.pitches = element[4]
        el.quarterLength = element[3]
        result.append(el)
        result.append("elemento")
    elif "Tuplet" in element[1]:
        result = []
        basic_ratio = element[1].split(" ")[1]
        numbers = basic_ratio.split(":")
        ratio = Fraction(f"{numbers[0]}/{numbers[1]}")
        cur_off = element[0]
        for el2 in element[4]:
            new_el = [cur_off, el2[0], element[2], (el2[1] / ratio), el2[2], el2[3]]
            new_processed = process_element(new_el)
            pair = new_processed[0:2]
            cur_off += new_el[3]
            result.append(pair)
        result.append("tuplet") 
    
    return result



def create_piece(master_list):
    
    names = count_parts(master_list)
    indicators = find_indicators(master_list)
    normalize_tuplets(master_list)
    parts = fill_parts(master_list)

    m21parts = []

    for name in names:
        new_part = m21.stream.Part()
        elements = parts[name]
        elements.sort(key=lambda x:x[0])
        for element in elements:
            element = process_element(element)
            #print(element)
            if element[-1] == "elemento":
                nota = element[1]
                new_part.append(nota)
                nota.offset = element[0]
            elif element[-1] == "tuplet":
                for x in element[0:-1]:
                    nota = x[1]
                    new_part.append(nota)
                    nota.offset = x[0]
        m21parts.append(new_part)

    """for ind in indicators:
        if ind[1] == "Tempo":
            indobj = m21.tempo.MetronomeMark(number=ind[2])
        elif ind[1] == "Formula de Compasso":
            indobj = m21.meter.TimeSignature(ind[2])
        m21parts[0].insert(0, indobj)"""

    m21.stream.makeNotation.makeRests(m21parts[0], fillGaps=True, inPlace=True)
    m21.stream.makeNotation.makeMeasures(m21parts[0], inPlace=True)
    for part in m21parts[1:]:
        m21.stream.makeNotation.makeRests(part, fillGaps=True, inPlace=True)
        m21.stream.makeNotation.makeMeasures(part,refStreamOrTimeRange=m21parts[0],inPlace=True)
    piece = m21.stream.Stream(m21parts)
    return piece

p = create_piece(output)
p.write('musicxml', 'output.xml')
