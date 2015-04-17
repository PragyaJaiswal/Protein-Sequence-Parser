#!/usr/bin/python
import re, os, json, requests, urllib
from ftplib import FTP

'''
Implemented for downloading 'proteome' sequence
data, of 'mammals', from the Ensembl FTP server.
'''

# Specify the mammals you wish to download data for in this.
# Only provide scientific names for each of them, as shown.

species = 'Mammals'

mammals = [
	'Homo sapiens',
	'Pan troglodytes',
	'Gorilla gorilla gorilla',
	'Macaca mulatta',
	'Rattus norvegicus',
	'Mus musculus'
]

# Specify the location where you wish to store the downloaded data.
store = '/home/pragya/Documents/GitHub/Protein-Sequence-Parser/Data/' + str(species) + '/'

i = 0
j = 0

for x in mammals:
	case = x.lower()
	mammals[j] = case.replace(' ', '_')
	j+=1

print(mammals)


'''
FTP Stuff here.
'''
ftp_host = 'ftp.ensembl.org'
ftp_user = 'anonymous'
ftp_pass = ''
ftp_path = '/pub/release-79/fasta'

ftp = FTP(ftp_host)
ftp.login(ftp_user, ftp_pass)
ftp.getwelcome()
ftp.cwd(ftp_path)

dirs = ftp.nlst()
# print(dirs)

# Navigate to the required diretory and thereby download data.
for dir in dirs:
	for p in range(0,len(mammals)):
		if re.search(str(mammals[p]), dir):
			print(str(mammals[p]) + ' present.')
			path=ftp_path + '/' + str(mammals[p])
			ftp.cwd(path)
			types=ftp.nlst()
			print(types)
			# if str(mammals[p]) in seq_type:
			# 	pass
			# else:
			# 	seq_type[str(mammals[p])]=ftp.nlst()
			for i in types:
				if re.search('pep', i):
					prefinal = path + '/' + str(i)
					ftp.cwd(prefinal)
					print(ftp.pwd())
					files = ftp.nlst()
					print(files)
					
					for i in files:
						print('here1')
						if re.search('abinitio', i):
							print('here2')
							final = prefinal + '/' + str(i)
							fullfilename = os.path.join(store + str(i))
							urllib.urlretrieve('ftp://' + ftp_host + str(final), fullfilename)
							# ftp.retrbinary('RETR ' + str(i), callback=None)
							break
		p+=1

print(ftp.pwd())