#!/usr/bin/env python3
import json

amino_acids = [
    'I',
    'L',
    'V',
    'F',
    'M',
    'C',
    'A',
    'G',
    'P',
    'T',
    'S',
    'Y',
    'W',
    'Q',
    'N',
    'H',
    'E',
    'D',
    'K',
    'R',
    'X',
]

mammals = [
    'Homo_sapiens',
    'Macaca_mulatta',
    'Mus_musculus',
    'Pan_troglodytes',
    'Rattus_norvegicus',
]

out = {}

for specie in mammals:
    file_name = "stage/" + specie + ".txt"

    out[specie] = {}

    with open(file_name, "r") as minion:
        file_dat = minion.read()
        for acid in amino_acids:
            out[specie][acid] = file_dat.count(acid)

out_data = json.dumps(out, indent=4)

with open("stage/out.json", "w") as minion:
    minion.write(out_data)