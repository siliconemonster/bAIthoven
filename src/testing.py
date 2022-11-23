from funcs import *
import music21 as m21
import os
from fractions import Fraction
import pandas as pd

###-------------EXTRAIR OS DADOS DE UMA PEÇA-------------###

def extract_data(filename, new_filename=False):

    components = find_other_components(filename)
    raw_parts = extract_parts(filename)
    all_groups = [parse_with_tuplets(p) for p in raw_parts]

    for i, group in enumerate(all_groups):
        for el in group:
            el.insert(2, f"Parte_{i+1}")

    master_list = [x for x in components]
    for group in all_groups:
        master_list += group
    master_list = sorted(master_list, key=lambda x: x[0])


    final_list = []
    for x in master_list:
        if len(x) < 4:
            final_list.append(x)
        else:
            if x[3] != 0:
                final_list.append(x)
            else:
                pass

    if new_filename:
        with open(new_filename + ".txt", "w") as fp:
            for item in master_list:
                fp.write(str(item))
                fp.write('\n')

    return final_list



###-------------CRIAR UMA PEÇA A PARTIR DOS DADOS-------------###


def create_piece(final_list):

    indicators = find_indicators(final_list)
    components = find_components(final_list, indicators)
    parts_lists = make_parts_lists(components)

    staves = []
    keys = sorted(list(parts_lists.keys()))
    for ind, key in enumerate(keys):
        parte1 = sorted(parts_lists[key], key=lambda x: x[0])

        parte1merged = merge_comps_inds(parte1, indicators)
        indicator_index = []
        for i, key2 in enumerate(sorted(list(parte1merged.keys()))):
            if len(parte1merged[key2]) > 1:
                indicator_index.append((i,key2))

        new_part = []
        for z in parte1:
            if "Tuplet" in z[1]:
                new_part.append(m21toabjadtuplet(z))
            else:
                new_part.append(m21toabjad(z))
        staff1 = abjad.Staff(new_part, name=key)
        abjad_indicators = []
        for x in indicator_index:
            comp = parte1merged[x[1]]
            for y in comp:
                if len(y) == 3:
                    new_ind = create_indicator(y)
                    abjad_indicators.append((x[0],new_ind))
        for k in abjad_indicators:
            abjad.attach(k[1],staff1[k[0]],context="Score")
        staves.append(staff1)
    score = abjad.Score(staves, simultaneous=True)
    return score

###-------------EXIBIR A PEÇA CRIADA-------------###

def show_new_piece(score):
    cur_dir = os.path.dirname(os.path.realpath(__file__))
    abjad.show(score, output_directory = cur_dir)


###-------------MODIFICAR APENAS AQUI:-------------###

### Esse código é apenas um teste para extrair dados de uma peça
### e reconstruir a mesma peça a partir dos dados extraídos

if __name__ == "__main__":
    filename = "OPUS 02 N1\\op2movI.xml"
    final_list = extract_data(filename, new_filename="op02movI")


    #score = create_piece(final_list)
    #show_new_piece(score)
