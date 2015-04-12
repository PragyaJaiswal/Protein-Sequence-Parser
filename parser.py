import re, os

count={}

i=0
a=0; c=0; d=0; e=0; f=0; g=0; h=0; i=0; k=0; l=0; m=0; n=0; p=0; q=0; r=0; s=0; t=0; v=0; w=0; x=0; y=0;

outfile = open('/home/pragya/Documents/GitHub/Protein-Sequence-Parser/outfile.txt', 'w+')

with open('/home/pragya/Downloads/Homo_sapiens.GRCh38.pep.abinitio.fa', 'r') as infile:
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

	"""
	for char in seq:
		if char == 'A':
			a+=1
			count['A'] = a
			#print(count['M'])
		elif char == 'C':
			c+=1
			count['C'] = c
		elif char == 'D':
			d+=1
			count['D'] = d
		elif char == 'E':
			e+=1
			count['E'] = e
		elif char == 'F':
			f+=1
			count['F'] = f
		elif char == 'G':
			g+=1
			count['G'] = g
		elif char == 'H':
			h+=1
			count['H'] = h
		elif char == 'I':
			i+=1
			count['I'] = i
		elif char == 'K':
			k+=1
			count['K'] = k
		elif char == 'L':
			l+=1
			count['L'] = l
		elif char == 'M':
			m+=1
			count['M'] = m
		elif char == 'N':
			n+=1
			count['N'] = n
		elif char == 'P':
			p+=1
			count['P'] = p
		elif char == 'Q':
			q+=1
			count['Q'] = q
		elif char == 'R':
			r+=1
			count['R'] = r
		elif char == 'S':
			s+=1
			count['S'] = s
		elif char == 'T':
			t+=1
			count['T'] = t
		elif char == 'V':
			v+=1
			count['V'] = v
		elif char == 'W':
			w+=1
			count['W'] = w
		elif char == 'Y':
			y+=1
			count['Y'] = y
		else:
			"Not present."

	print(count)
	"""