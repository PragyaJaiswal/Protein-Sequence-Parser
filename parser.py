#!/usr/bin/python
import re, os, json, requests, urllib, gzip
from os import listdir
import matplotlib.pyplot as plt
from ftplib import FTP
# from data import store
# print(data.store)


# Location where the downloaded data is stored. Will be updated for import from that file.
store = '/home/pragya/Documents/GitHub/Protein-Sequence-Parser/Data/Mammals/'

'''
Specify the location where you wish to store the files containing only the
entire proteome sequence and not the FASTA format sequence.
'''
out = '/home/pragya/Documents/GitHub/Protein-Sequence-Parser/Output/'

count={}	# Contains the frequency of occurence of each amino acid in the proteome sequence.
i=0
j=0

# urllib.urlretrieve('ftp://ftp.ensembl.org/pub/release-79/fasta/' + str(mammals[0]) + '/pep/Homo_sapiens.GRCh38.pep.abinitio.fa.gz', fullfilename)

# List of all the files that have been downloaded.
files=os.listdir(store)

for file in files:
	with gzip.open(store + str(file), 'r') as infile:
		data=infile.readlines()
		outfile = open(out + str((str(file)).split('.')[0]) + '.txt', 'w+')
		for line in data:
			if line.startswith('>') or line.startswith('transcript_biotype'):
				pass
			else:
				outfile.write(line)
			print("Number of lines written: " + str(i))
			i+=1
		infile.close()
		print("Amino acid sequence written to the requested file for file " + str(file))


# List of all the files whose output sequence has been generated for the entire proteome, not in FASTA format.
data=os.listdir(out)
for file in data:
	print(str(file))
	with open(out + str(file), 'r') as outfile:
		print("Reading sequence from file.")
		seq = outfile.read()
		# print(seq)

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

	# Export dictionary to JSON for showing count in a presentable form.
	a=json.dumps(count, sort_keys=True, indent=4, separators=(',', ': '))
	print(a)

	# Plot a bar graph for the number of each amino acid in the proteome sequence.
	plt.bar(range(len(count)), count.values(), align='center')
	plt.xticks(range(len(count)), list(count.keys()))
	plt.show()