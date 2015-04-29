#!/usr/bin/python
import re, os, sys, json, requests, urllib, gzip
from os import listdir
import matplotlib.pyplot as plt
from ftplib import FTP
import ensembl_data
import uniprot_data

global count, total, save
count = {}	# Contains the frequency of occurence of each amino acid in the proteome sequence.
total = {}	# Contains the total no. of each amino acid in the species.

'''
save :- is a dictionary that contains the virus file name as keys and another
dictionary (containing amino acid as key and its corresponding frequency as values) as values.
'''
save = {}

def mammals():
	i = 0
	
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
		with gzip.open(ensembl_data.store + str(file), 'r') as infile:
			data = infile.readlines()
			outfile = open(out + str((str(file)).split('.')[0]) + '.txt', 'w+')
			for line in data:
				if line.startswith('>') or line.startswith('transcript_biotype'):
					pass
				else:
					outfile.write(line)
				# print("Number of lines written: " + str(i))
				i+=1
			infile.close()
			print("Amino acid sequence written to the requested file for file " + str(file))
	parse(out, str(ensembl_data.species))

'''
Creates another output file with the entire proteome sequene only
This proteome sequene is no more in FASTA format.
'''

def viruses(species=None, store=None):
	i = 0
	j = 0

	'''
	Specify the location where you wish to store the files containing only the
	entire proteome sequence and not the FASTA format sequence.
	'''

	if species == None:
		out = './out/' + str(uniprot_data.species) + '/'
	else:
		out = './out/' + str(species) + '/'

	print(out)
	path_to_dir(out)


	# List of all the files that have been downloaded.	
	if store == None:
		files = os.listdir(uniprot_data.store)
		files.sort()
	else:
		files = os.listdir(store)

	print(files[0])
	print("Virus proteomes being processed.")

	for file in files:
		j+=1
		print(j)

		# print(bool(re.search('additional', str(file))))

		if bool(re.search('additional', file)):
			pass
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
				# print(str(outfile))
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
	parse(out, str(uniprot_data.species))


def parse(out, species, plot_loc=None):
	datafiles = os.listdir(out)
	j = 0
	total_amino_acid = 0
	save = {}
	for file in datafiles:
		with open(out + str(file), 'r') as outfile:
			print("Reading sequence from file: " + str(file))
			seq = outfile.read()
			total_amino_acid+=len(seq)
			"""
			Counts the occurence of each
			character in the sequence.
			"""
			
			count={}		# Fixed the reported error. Credits - Devesh Khandelwal.
			for char in seq:
				if char == '\n' or char == '\x00' or char == '*' or char == 'X':
					pass
				else:
					if char in count:
						count[char] = count[char] + 1
					else:
						count[char] = 1

		if str(file) in save:
			pass
		else:
			save[str(file)] = count

		j+=1
		print('No. of files processed: ' + str(j))
	jsonify(save)
		# # print(count)
		# total = add(count)
		# name = str.split(file, '.')[0]
		# plot(count, species, name, plot_loc)
		# print(total_amino_acid)
		# scaled_count = scale(count, total_amino_acid)
		# jsonify(scaled_count)


	# for x in save:
	# 	name = str.split(str(x), '.')[0]
	# 	print(name)
	# 	perc = percentage(save[x], total, species, name)
	# 	print(perc)
	# 	save[x] = perc
	# 	# loc = plot_loc + '/percent/'
	# 	# plot(perc, species, name, loc)
	# jsonify(save)


def scale(count, total_amino_acid):
	for x in count:
		count[x] = (count[x]/total_amino_acid)
	return count


'''
Adds the total number of amino acids in the species.
For example, we wish to know the number of a particular amino acid, say L, in
the viruses species.
total :-  Contains the total number of each amino acid in the species.
'''
def add(count):
	for x in count:
		if x in total:
			total[x] = total[x] + count[x]
		else:
			total[x] = count[x]
	print('Printing the total amino acids in the species for the files processed: ')
	# print(total)
	return total


'''
Calculates the percentage of each amino acid for a organism when compared to
the amount of that amino acid in the whole species.
Example - Suppose we wish to know to percentage of an amino acid, say L, in a
virus X when compared to the total amount of L in the viruses species.
'''
def percentage(count, total, species, name=None):
	perc = {}
	visited = []
	k = 0
	for i in count.keys():
		if i in total.keys() and not i in visited:
			print(total[i])
			visited.append(i)
			perc[i] = (float(count[i]))/(float(total[i]))*100
	return perc


def path_to_dir(out):
	# Create the specified folder if it does not already exist.
	if not os.path.exists(out) and not out == '':
		os.makedirs(out)

	# If no directory is specified to store the data, store it in the current directory of the user..
	if out == '':
		home = os.path.expanduser('~')
		out = './' + str(uniprot_data.species) + '/'
		os.makedirs(out)


# Export dictionary to JSON for showing count in a presentable form.
def jsonify(count, location=None):
	a = json.dumps(count, sort_keys=True, indent=4, separators=(',', ': '))
	if location == None:
		with open('virus_count.json', 'a+') as outfile:
			outfile.write(a)
	else:
		with open(str(location), 'a+') as outfile:
			outfile.write(a)
	# print(a)


# Plot a bar graph for the number of each amino acid in the proteome sequence.
def plot(count, species, name, location=None):
	if location == None:
		figs = './plots/' + str(species) + '/'
	else:
		figs = str(location) + '/'
	path_to_dir(figs)
	filename = str(figs) + str(name) + '.png'
	plt.figure().canvas.set_window_title(str(name))
	plt.bar(range(len(count)), count.values(), align='center')
	plt.xticks(range(len(count)), list(count.keys()))
	plt.savefig(filename)
	plt.close()


if __name__ == '__main__':
	mammals()
	viruses()
	# Same can be done for the data of Bcateria obtained from UniProt.
	viruses('Bacteria')