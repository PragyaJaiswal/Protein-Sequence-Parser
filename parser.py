#!/usr/bin/python
import re, os, json, requests, urllib, gzip
import matplotlib.pyplot as plt
from ftplib import FTP

count={}

i=0
j=0
#p=0

outfile = open('/home/pragya/Documents/GitHub/Protein-Sequence-Parser/outfile.txt', 'w+')

mammals = ['Homo sapiens', 'Pan troglodytes', 'Gorilla gorilla gorilla', 'Macaca mulatta', 'Rattus norvegicus', 'Mus musculus']

for x in mammals:
	case=x.lower()
	mammals[j]=case.replace(' ', '_')
	j+=1

print(mammals)
print(len(mammals))
fullfilename = os.path.join('/home/pragya/Documents/GitHub/Protein-Sequence-Parser/Data/Mammals/','Homo_sapiens.GRCh38.pep.abinitio.fa.gz')
urllib.urlretrieve('ftp://ftp.ensembl.org/pub/release-79/fasta/' + str(mammals[0]) + '/pep/Homo_sapiens.GRCh38.pep.abinitio.fa.gz', fullfilename)


with gzip.open(fullfilename, 'r') as infile:
	data=infile.readlines()
	for line in data:
		if line.startswith('>') or line.startswith('transcript_biotype'):
			pass
		else:
			outfile.write(line)
		print("Number of lines written: " + str(i))
		i+=1
	infile.close()
	print("Amino acid sequence written to the requested file.")


with open('/home/pragya/Documents/GitHub/Protein-Sequence-Parser/outfile.txt', 'r') as outfile:
	print("Reading sequence from file.")
	seq = outfile.read()
	#print(seq)

	"""
	Counts the occurence of each
	character in the sequence.
	"""

	for char in seq:
		if char=='\n' or char=='*' or char=='X':
			pass
		else:
			if char in count:
				count[char] = count[char] + 1
			else:
				count[char] = 1
	print(count)

a=json.dumps(count, sort_keys=True, indent=4, separators=(',', ': '))
print(a)

plt.bar(range(len(count)), count.values(), align='center')
plt.xticks(range(len(count)), list(count.keys()))
plt.show()