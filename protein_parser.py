#!/usr/bin/python
import re, os, json, requests, urllib, gzip
from os import listdir
import matplotlib.pyplot as plt
from ftplib import FTP
import ensembl_data
import uniprot_data


global count, total, save
count = {}	# Contains the frequency of occurence of each amino acid in the proteome sequence.

"""
The script parses the amino acid sequence sequence for the organism and 
thereby plots the amino acid content in each protein.
"""

def mammals():
	i = 0
	j = 0
	
	'''
	Specify the location where you wish to store the files containing only the
	entire proteome sequence and not the FASTA format sequence.
	'''	
	out = './out/' + str(ensembl_data.species) + '/'
	
	# Create the specified folder if it does not already exist.
	path_to_dir(out)

	# List of all the files that have been downloaded.
	files = os.listdir(ensembl_data.store)

	print("Mammal proteomes being processed.")
	
	for file in files:
		j+=1
		count = {}
		parse(str(file), count, str(ensembl_data.species))
		print('No. of files done: ' + str(j) + ', Last File: ' + str(file))
		# if j == 2:
		# 	break

'''
The amino acid content in each protein of the organism is calculated here.
'''

def parse(file, count, species):
	with gzip.open(ensembl_data.store + str(file), 'r') as infile:
		data = infile.readlines()
		print('file: ' + str(file))
		i = 0
		for line in data:
			if line.startswith('>'):
				if not i == 0:
					print('No. of genes processed: ' + str(i))
					jsonify(count)
					plot(count, species, str(file), 'Protein ' + str(i))
				i+=1
				# if i > 10:
				# 	break
				count = {}
				continue
			elif line.startswith('transcript_biotype'):
				continue
			else:
				for char in line:
					if char == '\n' or char == '\x00' or char == '*' or char == 'X':
						pass
					else:
						if char in count:
							count[char] = count[char] + 1
						else:
							count[char] = 1
		infile.close()


def path_to_dir(out):
	# Create the specified folder if it does not already exist.
	if not os.path.exists(out) and not out == '':
		os.makedirs(out)

	# If no directory is specified to store the data, store it on user's desktop.
	if out == '':
		home = os.path.expanduser('~')
		out = './' + str(uniprot_data.species) + '/'
		os.makedirs(out)


# Export dictionary to JSON for showing count in a presentable form.
def jsonify(count):
	a = json.dumps(count, sort_keys=True, indent=4, separators=(',', ': '))
	print(a)


# Plot a bar graph for the number of each amino acid in the proteome sequence.
def plot(count, species, name, pro_num):
	figs = './plots/' + str(species) + '/individual proteins/' + str(name) + '/'
	path_to_dir(figs)
	filename = str(figs) + str(pro_num)
	plt.figure().canvas.set_window_title(str(name))
	plt.bar(range(len(count)), count.values(), align='center')
	plt.xticks(range(len(count)), list(count.keys()))
	plt.savefig(filename)
	plt.close()


if __name__ == '__main__':
	mammals()