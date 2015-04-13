#!/usr/bin/python
import re, os, json
import matplotlib.pyplot as plt

count={}

i=0
#a=0; c=0; d=0; e=0; f=0; g=0; h=0; i=0; k=0; l=0; m=0; n=0; p=0; q=0; r=0; s=0; t=0; v=0; w=0; x=0; y=0;


outfile = open('/home/pragya/Documents/GitHub/Protein-Sequence-Parser/outfile.txt', 'w+')


with open('/home/pragya/Downloads/Danio_rerio.Zv9.pep.abinitio.fa', 'r') as infile:
	data = infile.readlines()
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