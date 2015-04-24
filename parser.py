#!/usr/bin/python
import re, os, json, requests, urllib, gzip
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

def viruses():
	i = 0
	j = 0

	'''
	Specify the location where you wish to store the files containing only the
	entire proteome sequence and not the FASTA format sequence.
	'''	
	out = './out/' + str(uniprot_data.species) + '/'

	path_to_dir(out)

	# List of all the files that have been downloaded.	
	files=os.listdir(uniprot_data.store)

	print("Virus proteomes being processed.")

	for file in files:
		j+=1
		print(j)

		# print(bool(re.search('additional', str(file))))

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
		# if j == 10:
		# 	break
	parse(out, str(uniprot_data.species))


def parse(out, species):
	datafiles = os.listdir(out)
	j = 0
	save = {}
	for file in datafiles:
		with open(out + str(file), 'r') as outfile:
			print("Reading sequence from file: " + str(file))
			seq = outfile.read()

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
			# print(save[str(file)])
			# print(save)

		j+=1
		print('No. of files processed: ' + str(j))
		jsonify(count)
		add(count)
		name = str.split(file, '.')[0]
		plot(count, species, name)
		if j == 5:
			break
	
	# print(len(save))
	jsonify(save)
	print(species)
	for x in save:
		name = str.split(str(x), '.')[0]
		print(name)
		percentage(save[x], total, species, name)


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
	jsonify(total)


'''
Calculates the percentage of each amino acid for a organism when compared to
the amount of that amino acid in the whole species.
Example - Suppose we wish to know to percentage of an amino acid, say L, in a
virus X when compared to the total amount of L in the viruses species.
'''
def percentage(count, total, species, name=None):
	perc = {}
	k = 0
	for i in count.keys():
		if not len(perc) == 21:
			j = [j for j in total.keys()]
			if i == str(j[k]):
				print(str(i) + ' in this organism: ' + str(int(count[i])))
				print('Total ' + str(i) + ' in the species ' + str(species) +
					': ' + str(int(total[i])))
				perc[i] = (float(count[i])/float(total[j[k]]))*100
				k+=1
			else:
				pass
	print('Percentage of amino acid in each organism with respect to the total amino acid in its species.')
	jsonify(perc)
	plot(perc, species, name, 'percent')


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
def jsonify(count):
	a = json.dumps(count, sort_keys=True, indent=4, separators=(',', ': '))
	print(a)


# Plot a bar graph for the number of each amino acid in the proteome sequence.
def plot(count, species, name, location=None):
	if location == None:
		figs = './plots/' + str(species) + '/'
	else:
		figs = './plots/' + str(species) + '/' + str(location) + '/'
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