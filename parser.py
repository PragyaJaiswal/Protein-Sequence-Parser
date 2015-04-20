#!/usr/bin/python
import re, os, json, requests, urllib, gzip
from os import listdir
import matplotlib.pyplot as plt
from ftplib import FTP
import ensembl_data
import uniprot_data

# store :- Location where the downloaded data is stored.

global count
count = {}	# Contains the frequency of occurence of each amino acid in the proteome sequence.


def mammals():
	i = 0
	
	'''
	Specify the location where you wish to store the files containing only the
	entire proteome sequence and not the FASTA format sequence.
	'''	
	out = './output/' + str(ensembl_data.species) + '/'
	
	# List of all the files that have been downloaded.	
	files=os.listdir(ensembl_data.store)

	print("Mammal proteomes being processed.")
	
	for file in files:
		with gzip.open(ensembl_data.store + str(file), 'r') as infile:
			data = infile.readlines()
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
		break
	parse(out)

def viruses():
	i = 0

	'''
	Specify the location where you wish to store the files containing only the
	entire proteome sequence and not the FASTA format sequence.
	'''	
	out = './output/' + str(uniprot_data.species) + '/'

	# List of all the files that have been downloaded.	
	files=os.listdir(uniprot_data.store)

	print("Virus proteomes being processed.")

	for file in files:
		with gzip.open(uniprot_data.store + str(file), 'r') as infile:
			data = infile.readlines()
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
	parse(out)


def parse(out):
	datafiles = os.listdir(out)
	for file in datafiles:
		print(str(file))
		if re.search('additional', str(file)):
			add_file = open(file)
			lines=add_file.readlines()
			print(lines)
			file.write(lines)
		with open(out + str(file), 'r') as outfile:
			print("Reading sequence from file.")
			seq = outfile.read()
			# print(seq)

			"""
			Counts the occurence of each
			character in the sequence.
			"""

			for char in seq:
				if char == '\n' or char == '*' or char == 'X':
					pass
				else:
					if char in count:
						count[char] = count[char] + 1
					else:
						count[char] = 1
			print(count)
		jsonify(count)
		plot(count)

# Export dictionary to JSON for showing count in a presentable form.
def jsonify(count):
	a = json.dumps(count, sort_keys=True, indent=4, separators=(',', ': '))
	print(a)

# Plot a bar graph for the number of each amino acid in the proteome sequence.
def plot(count):
	plt.bar(range(len(count)), count.values(), align='center')
	plt.xticks(range(len(count)), list(count.keys()))
	plt.show()

if __name__ == '__main__':
	mammals()
	viruses()