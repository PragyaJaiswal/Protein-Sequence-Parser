#!/usr/bin/env python3
import gzip
import wget
import json
from ftplib import FTP
from Bio import SeqIO

DL_List = [
    'ailuropoda_melanoleuca',   # Giant Panda
    'anas_platyrhynchos',       # Mallard, Aves
    'anolis_carolinensis',      # Carolina anole, Retilia
    'astyanax_mexicanus',       # Mexican tetra, Actinopterygii
    'bos_taurus',               # Cattle, Mammalia
    'caenorhabditis_elegans',   # C. Elegans, Nematoda  SKIP
    'callithrix_jacchus',       # Common marmoset, Mammalia
    'canis_familiaris',         # Dog, Mammalia
    'cavia_porcellus',          # Guinea pig, Mammalia
    'chlorocebus_sabaeus',      # Green monkey, Mammalia
    'choloepus_hoffmanni',      # Sloth, Mammalia
    'ciona_intestinalis',       # Ciona intestinalis, Ascidiacea
    'ciona_savignyi',           # Ciona savignyi, Ascidiacea
    'danio_rerio',              # Zebrafish, Actinopterygii
    'dasypus_novemcinctus',     # Armadillo, Mammalia
    'dipodomys_ordii',          # Ord's kangaroo rat, Mammalia
    'drosophila_melanogaster',  # Drosophila melanogaster, Insecta
    'echinops_telfairi',        # hedgehog, Mammalia
    'equus_caballus',           # Horse, Mammalia
    'erinaceus_europaeus',      # European hedgehog, Mammalia
    'felis_catus',              # Cat, Mammalia
    'ficedula_albicollis',      # Collared flycatcher, Aves
    'gadus_morhua',             # Atlantic cod, Actinopterygii
    'gallus_gallus',            # Red junglefowl, Aves
    'gasterosteus_aculeatus',   # Three-spined stickleback, Actinopterygii
    'gorilla_gorilla',          # Gorilla, Mammalia
    'homo_sapiens',             # Human, Mammalia
    'ictidomys_tridecemlineatus', # Thirteen-lined ground squirrel, Mammalia
    'latimeria_chalumnae',      # West Indian Ocean coelacanth, Sarcopterygii
    'lepisosteus_oculatus',     # Spotted gar, Actinopterygii
    'loxodonta_africana',       # African bush elephant, Mammalia
    'macaca_mulatta',           # Rhesus macaque, Mammalia
    'macropus_eugenii',         # Tammar wallaby, Mammalia
    'meleagris_gallopavo',      # Wild turkey, Aves
    'microcebus_murinus',       # Gray mouse lemur, Mammalia
    'monodelphis_domestica',    # Gray short-tailed opossum, Mammalia
    'mus_musculus',             # House mouse, Mammalia
    'mustela_putorius_furo',    # Ferret, Mammalia
    'myotis_lucifugus',         # Little brown bat, Mammalia
    'nomascus_leucogenys',      # white-cheeked gibbon, Mammalia
    'ochotona_princeps',        # American pika, Mammalia
    'oreochromis_niloticus',    # Nile tilapia, Actinopterygii
    'ornithorhynchus_anatinus', # Platypus, Mammalia
    'oryctolagus_cuniculus',    # European rabbit, Mammalia
    'oryzias_latipes',          # oryzias_latipes, Actinopterygii
    'otolemur_garnettii',       # Northern greater galago, Mammalia
    'ovis_aries',               # Sheep, Mammalia
    'pan_troglodytes',          # Common chimpanzee, Mammalia
    'papio_anubis',             # Olive baboon, Mammalia
    'pelodiscus_sinensis',      # Chinese softshell turtle, Sauropsida
    'petromyzon_marinus',       # Sea lamprey, Hyperoartia 
    'poecilia_formosa',         # Amazon molly, Actinopterygii
    'pongo_abelii',             # Sumatran orangutan, Mammalia
    'procavia_capensis',        # Rock hyrax, Mammalia
    'pteropus_vampyrus',        # Large flying fox, Mammalia
    'rattus_norvegicus',        # Brown rat, Mammalia
    'saccharomyces_cerevisiae', # Saccharomyces cerevisiae, Saccharomycetes  SKIP
    'sarcophilus_harrisii',     # Tasmanian devil, Mammalia
    'sorex_araneus',            # Common shrew, Mammalia
    'sus_scrofa',               # Wild boar, Mammalia
    'taeniopygia_guttata',      # Zebra finch, Aves
    'takifugu_rubripes',        # Takifugu rubripes, Actinopterygii
    'tarsius_syrichta',         # Philippine tarsier, Mammalia
    'tetraodon_nigroviridis',   # Tetraodon nigroviridis, Actinopterygii
    'tupaia_belangeri',         # Northern treeshrew, Mammalia
    'tursiops_truncatus',       # Common bottlenose dolphin, Mammalia
    'vicugna_pacos',            # Alpaca, Mammalia
    'xenopus_tropicalis',       # Western clawed frog, Amphibia
    'xiphophorus_maculatus',    # Southern platyfish, Actinopterygii
]

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

ftp_conf = {
    'host': 'ftp.ensembl.org',
    'user': 'anonymous',
    'pswd': '',
    'root': '/pub/release-78/fasta/',
    'urif': 'ftp://ftp.ensembl.org/pub/release-78/fasta/{0}/pep/{1}'
}

class Ensemble:
    def __init__(self):
        self.ftp = FTP(ftp_conf['host'])
        self.ftp.login(ftp_conf['user'], ftp_conf['pswd'])
        self.ftp.getwelcome()
        self.ftp.cwd(ftp_conf['root'])

    def list_ftp_dir(self, dir):
        self.ftp.cwd('./' + dir + '/pep/')
        dat = self.ftp.nlst()
        self.ftp.cwd(ftp_conf['root'])
        return dat

    def get_file_uri_for_organism(self, name):
        # Get filename.
        ls = self.list_ftp_dir(name)
        for n in ls:
            if 'abinitio' in n:
                return ftp_conf['urif'].format(name, n)
        return None

ensemble = Ensemble()
count = 0

def routine_for(organism):
    global count
    count += 1
    uri = ensemble.get_file_uri_for_organism(organism)
    if uri is not None:
        print('Routine #{0}: Organism- {1}'.format(count, organism))
        file_name = wget.download(uri, out = './stage/dl')
        f = gzip.open(file_name, 'rb')
        file_extract = file_name + '.fasta'
        f_extracted = open(file_extract, 'wb')
        f_extracted.write(f.read())
        f_extracted.close()
        f.close()

        handle = open(file_extract, "rU")
        counts = dict((k, 0) for k in amino_acids)

        for record in SeqIO.parse(handle, "fasta"):
            for acid in amino_acids:
                counts[acid] += record.seq.count(acid)

        handle.close()
        print('\nRoutine Finished')
        return counts

    print('\nRoutine Skipped')
    return dict((k, 0) for k in amino_acids)

def main():
    final = {}
    for organism in DL_List:
        final[organism] = routine_for(organism)

    out_data = json.dumps(final, indent=4)

    with open("stage/out_full_final.json", "w") as minion:
        minion.write(out_data)

if __name__ == "__main__":
    main()