#!/usr/bin/env python3
import json

amino_acids = {
    'I': None,
    'L': None,
    'V': None,
    'F': None,
    'M': None,
    'C': None,
    'A': None,
    'G': None,
    'P': None,
    'T': None,
    'S': None,
    'Y': None,
    'W': None,
    'Q': None,
    'N': None,
    'H': None,
    'E': None,
    'D': None,
    'K': None,
    'R': None,
    'X': None,
}

mammal = {
    'Homo_sapiens': None,
    'Macaca_mulatta': None,
    'Mus_musculus': None,
    'Pan_troglodytes': None,
    'Rattus_norvegicus': None,
}

out_mammal = mammal

for specie, acids in mammal.items():
    file_name = "stage/" + specie + ".txt"
    with open(file_name, "r") as minion:
        file_dat = minion.read()
        print(file_name)
        amino_acids_specie = amino_acids
        for acid, count in amino_acids_specie.items():
            amino_acids_specie[acid] = file_dat.count(acid)
            break
        print(out_mammal)

        out_mammal[specie] = amino_acids_specie

out_data = json.dumps(out_mammal, indent=4)

with open("stage/out.json", "w") as minion:
    minion.write(out_data)