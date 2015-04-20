#!/usr/bin/python
import re, os, json, requests, urllib
from ftplib import FTP

'''
Implemented for downloading 'proteome' sequence
data from the Uniprot FTP server.
'''

# Specify the species for which data is to be downloaded.
# The options are - Archae, Bacteria, Eukaryota and Viruses.
species = 'Viruses'

# Specify the location where you wish to store the downloaded data.
store = './dat/' + str(species) + '/'

def path_to_dir(store):
	# Create the specified folder if it does not already exist.
	if not os.path.exists(store) and not store == '':
		os.makedirs(store)

	# If no directory is specified to store the data, store it on user's desktop.
	if store == '':
		home = os.path.expanduser('~')
		store = './dat/' + str(species) + '/'
		os.makedirs(store)

i = 0
j = 0

'''
FTP Stuff here.
'''

def ftp_download():
	ftp_host = 'ftp.uniprot.org'
	ftp_user = 'anonymous'
	ftp_pass = ''
	ftp_path = '/pub/databases/uniprot/current_release/knowledgebase/reference_proteomes'

	ftp = FTP(ftp_host)
	ftp.login(ftp_user, ftp_pass)
	ftp.getwelcome()
	ftp.cwd(ftp_path)

	dirs = ftp.nlst()
	# print(dirs)
	p = 0

	# Navigate to the required directory and thereby download data.
	for dir in dirs:
		if re.search(species, dir):
			path = ftp_path + '/' + str(species)
			# print(path)
			ftp.cwd(path)
			types = ftp.nlst()
			for x in types:
				if not re.search('DNA.fasta.gz', x) and re.search('fasta.gz', x):
					final = path + '/' + str(x)
					# print(final)
					fullfilename = os.path.join(store + str(x))
					urllib.urlretrieve('ftp://' + ftp_host + str(final), fullfilename)
					p+=1
				else:
					pass

	print("Number of viruses: " + str(p))

	print(ftp.pwd())

if __name__ == '__main__':
	path_to_dir(store)
	ftp_download()