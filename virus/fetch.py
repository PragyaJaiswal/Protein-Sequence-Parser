#!/usr/bin/python
import re, os, json, sys, gzip, urllib, requests, httplib2
from bs4 import BeautifulSoup
from ftplib import FTP

sys.path.insert(0, '/home/pragya/Documents/GitHub/Protein-Sequence-Parser/')
import parser

# parser.viruses()

'''
Script to find proteomes of all viruses whose hosts are
homo_sapiens or mammals. List of these viruses is given at - 
http://viralzone.expasy.org/all_by_species/678.html
Go to the respective virus proteome on uniprot and download the
proteome of the virus.
'''

global redirect, viruses, output
redirect = []
viruses = []
output = []

def init(url):
	print('Getting: ' + str(url))
	response = requests.get(url)

	soup = BeautifulSoup(response.content)

	# print(soup.prettify())
	num = 0

	for link in soup.find_all('a'):
		redirect.append(str(link.get('href')))
		num+=1
	return redirect

		
def uniprot(urls):
	num = 0
	for x in urls:
		if re.search('uniprot', str(x)):
			num+=1
			res = init(x)
			for y in res:
				if re.search('taxonomy/', str(y)):
					tax_num = str(y.split('/')[2])
					viruses.append(str(tax_num))
			output = remove_duplicates(viruses)
			print(output)
		# if num == 3:
		# 	break
	print('No. of preoteomes to be retrieved: ' + str(num))
	return output


def remove_duplicates(viruses):
	output = []
	visited = set()
	for virus in viruses:
		if virus not in visited:
			output.append(virus)
			visited.add(virus)
	return output


'''
FTP Stuff here.
'''

def ftp_download(output):
	ftp_host = 'ftp.uniprot.org'
	ftp_user = 'anonymous'
	ftp_pass = ''
	ftp_path = '/pub/databases/uniprot/current_release/knowledgebase/reference_proteomes/Viruses/'

	ftp = FTP(ftp_host)
	ftp.login(ftp_user, ftp_pass)
	ftp.getwelcome()
	ftp.cwd(ftp_path)

	virus_names = ftp.nlst()
	
	print(output)
	p = 0

	# Navigate to the required directory and thereby download data.
	for num in output:
		for virus in virus_names:
			if str(num) in str(virus):
				if not re.search('DNA.fasta.gz', virus) and re.search('fasta.gz', virus):
					final = ftp_path + str(virus)
					print(final)
					fullfilename = os.path.join(store + str(virus))
					urllib.urlretrieve('ftp://' + ftp_host + str(final), fullfilename)
					p+=1
				else:
					pass

	print("Number of virus files downloaded: " + str(p))

	print(ftp.pwd())


def path_to_dir(out):
	# Create the specified folder if it does not already exist.
	if not os.path.exists(out) and not out == '':
		os.makedirs(out)

	# If no directory is specified to store the data, store it in the current directory of the user..
	if out == '':
		home = os.path.expanduser('~')
		out = './' + str(uniprot_data.species) + '/'
		os.makedirs(out)


def taxonomy(store):
	i = 0
	j = 0

	'''
	Specify the location where you wish to store the files containing only the
	entire proteome sequence and not the FASTA format sequence.
	'''	
	out = './out/' + 'Viruses/'

	path_to_dir(out)

	# List of all the files that have been downloaded.	
	files=os.listdir(store)

	print("Virus proteomes being processed.")

	for file in files:
		j+=1
		print(j)

		# print(bool(re.search('additional', str(file))))

		if bool(re.search('additional', file)):
			with gzip.open(store + str(file), 'r') as reading:
				data = reading.readlines()
				print('Pre: ' + str(pre))
				prev = open(str(pre), 'w+')
				for line in data:
					if line.startswith('>') or line.startswith('transcript_biotype'):
						pass
					else:
						prev.write(line)
		else:
			with gzip.open(store + str(file), 'r') as infile:
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
		if j == 10:
			break
	parser.parse(out, 'Viruses')


if __name__ == '__main__':
	url = 'http://viralzone.expasy.org/all_by_species/678.html'
	store = './dat/human_virus/'
	path_to_dir(store)
	urls = init(url)
	output = uniprot(urls)
	ftp_download(output)
	taxonomy(store)