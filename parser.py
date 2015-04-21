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
	out = './out/' + str(ensembl_data.species) + '/'
	
	# List of all the files that have been downloaded.	
	files = os.listdir(ensembl_data.store)

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
	parse(out)


def viruses():
	i = 0
	j = 0
	listing = []
	print(type(listing))

	'''
	Specify the location where you wish to store the files containing only the
	entire proteome sequence and not the FASTA format sequence.
	'''	
	out = './out/' + str(uniprot_data.species) + '/'

	# Create the specified folder if it does not already exist.
	if not os.path.exists(out) and not out == '':
		os.makedirs(out)

	# If no directory is specified to store the data, store it on user's desktop.
	if out == '':
		home = os.path.expanduser('~')
		out = './' + str(uniprot_data.species) + '/'
		os.makedirs(out)


	# List of all the files that have been downloaded.	
	files=os.listdir(uniprot_data.store)
	print(type(files))

	print("Virus proteomes being processed.")

	for file in files:
		j+=1
		print(j)

		print(bool(re.search('additional', str(file))))

		if bool(re.search('additional', file)):
			with gzip.open(uniprot_data.store + str(file), 'r') as reading:
				data = reading.readlines()
				print('Pre: ' + str(pre))
				prev = open(str(pre), 'w+')
				for line in data:
					if line.startswith('>') or line.startswith('transcript_biotype'):
						pass
					else:
						prev.write(line)
		else:
			with gzip.open(uniprot_data.store + str(file), 'r') as infile:
				data = infile.readlines()
				filename = out + str((str(file)).split('.')[0]) + '.txt'
				outfile = open(out + str((str(file)).split('.')[0]) + '.txt', 'w+')
				print(str(outfile))
				for line in data:
					if line.startswith('>') or line.startswith('transcript_biotype'):
						pass
					else:
						outfile.write(line)
					# print("Number of lines written: " + str(i))
					i+=1
				pre = filename
				infile.close()
				print("Amino acid sequence written to the requested file for file " + str(file))
		# if j == 60:
		# 	break
	parse(out)


def parse(out):
	datafiles = os.listdir(out)
	print(datafiles)
	j = 0
	for file in datafiles:
		with open(out + str(file), 'r') as outfile:
			print("Reading sequence from file.")
			seq = outfile.read()

			"""
			Counts the occurence of each
			character in the sequence.
			"""

			for char in seq:
				if char == '\n' or char == '\x00' or char == '*' or char == 'X':
					pass
				else:
					if char in count:
						count[char] = count[char] + 1
					else:
						count[char] = 1
			print(count)
		j+=1
		print(j)
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
	# mammals()
	viruses()