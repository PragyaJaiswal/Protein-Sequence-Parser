#!/usr/bin/python
import re, os, json, sys, gzip, urllib, requests, httplib2
from bs4 import BeautifulSoup
from ftplib import FTP
import fetch

sys.path.insert(0, '/home/pragya/Documents/GitHub/pragyajswl/Protein-Sequence-Parser/')
import parser

'''
Script to find proteomes of all viruses whose hosts are
homo_sapiens or mammals. List of these viruses is given at - 
http://viralzone.expasy.org/all_by_species/678.html
Go to the respective virus proteome on uniprot and download the
proteome of the virus.
'''

global hosts, viruses, output, hostnum, tax_num
hosts = []
viruses = []
output = []
hostnum = []
tax_num = []


def host_species(url, search):
	print('Getting: ' + str(url))
	# print(url)
	# print(search)
	hosts = []
	response = requests.get(url)

	soup = BeautifulSoup(response.content)

	# print(soup.prettify())
	count = 0
	# checks
	for link in soup.find_all('a'):
		if str(search) in str(link.get('href')):
			if not len(hosts) == 7:
				hosts.append(str(link.get('href')))
				count+=1
				hostnum.extend(re.findall('\d+', str(link.get('href'))))
			else:
				pass
	print('Host number: ' + str(hostnum))
	return hosts


def viruses(url, search, unwanted):
	print('Getting: ' + str(url))
	names = []
	final = []
	response = requests.get(url)

	soup = BeautifulSoup(response.content)
	count = 0

	for link in soup.find_all('a'):
		if str(search) in str(link.get('href')):
			count+=1
			unwanted.extend(hostnum)
			names.append(str(link.get('href')))
	rem = remove_duplicates(names)
	final = vertebrates(rem, unwanted)
	return final


def vertebrates(names, unwanted):
	final = []
	for name in names:
		proc = True
		for x in unwanted:
			if x in name:
				proc = False
				break
		if proc:
			final.append(name)
	return final


def remove_duplicates(names):
	output = []
	visited = set()
	for virus in names:
		if virus not in visited:
			output.append(virus)
			visited.add(virus)
	return output


def path_to_dir(out):
	# Create the specified folder if it does not already exist.
	if not os.path.exists(out) and not out == '':
		os.makedirs(out)

	# If no directory is specified to store the data, store it in the current directory of the user..
	if out == '':
		home = os.path.expanduser('~')
		out = './' + str(uniprot_data.species) + '/'
		os.makedirs(out)


def download(virus_url):
	print(virus_url)
	response = requests.get(virus_url)

	soup = BeautifulSoup(response.content)
	for link in soup.find_all('a', href = True, text = 'Proteome'):
		# print(str(link.get('href')))
		response = requests.get(str(link.get('href')))
		soup1 = BeautifulSoup(response.content)
		
		for x in soup1.find_all('a', href = True, text = 'Taxonomy'):
			response = requests.get(str(link.get('href')) + str(x.get('href')))
			soup2 = BeautifulSoup(response.content)

			for num in soup2.find_all('a', href = True):
				if '/taxonomy/' in str(num.get('href')):
					y = str(num.get('href'))
					tax = str(y.split('/')[2])
					tax_num.append(tax)
	output = remove_duplicates(tax_num)
	print(output)
	return output
			

'''
FTP Stuff here.
'''

def ftp_download(output, store):
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
					# print(final)
					fullfilename = os.path.join(store + str(virus))
					urllib.urlretrieve('ftp://' + ftp_host + str(final), fullfilename)
					p+=1
				else:
					pass

	print("Number of virus files downloaded: " + str(p))
	print(ftp.pwd())
	# fetch.taxonomy(store, None, './out/vertebrate_viruses/')


if __name__ == '__main__':
	host = 0
	url = 'http://viralzone.expasy.org/all_by_species/664.html'
	store = './dat/human_virus/'
	path_to_dir(store)
	hosts = host_species(url, 'all_by_protein')
	print('Done hosts. Finding viruses for each host now.')
	genetic = ['236', '238', '293', '294', '237', '295', '235', '283']
	print(hosts)
	for x in hosts:
		if '655' in str(x):
			# Viruses that attack Vertebrates
			store = './dat/vertebrate_virus/'
			path_to_dir(store)
			unwanted_vert = [
				'176', '528', '4', '5', '148', '12', '19', '174',
				'772', '11', '103', '162', '603', '104', '714', '28',
				'30', '33', '27', '32', '43', '47', '3', '71', '9' 
			]
			unwanted_vert.extend(genetic)
			names = viruses('http://viralzone.expasy.org' + str(x), 'all_by_species', unwanted_vert)
			# print(names)
			for virus in names:
				virus_url = 'http://viralzone.expasy.org' + str(virus)
				virus_tax_num = download(virus_url)
				ftp_download(virus_tax_num, store)
			fetch.taxonomy(store, './out/vertebrate_virus/', None)
		elif '654' in str(x):
			# Viruses that attack Invertebrates
			unwanted_vert = [
				'529', '139', '13', '19', '144', '4747', '147', '173',
				'103', '2957', '162', '104', '126', '36', '792', '129',
				'2936', '2938', '237'
			]
			unwanted_vert.extend(genetic)
			names = viruses('http://viralzone.expasy.org' + str(x), 'all_by_species', unwanted_vert)
			print(names)
			for virus in names:
				virus_url = 'http://viralzone.expasy.org' + str(virus)
				virus_tax_num = download(virus_url)
				ftp_download(virus_tax_num, store)
			fetch.taxonomy(store, './out/invertebrate_virus/', None)
		elif '658' in str(x):
			# Viruses that attack Eukaryotic organism
			unwanted_vert = [
				'4740', '17', '145', '166', '593', '167', '2996', '168',
				'104', '161', '738', '2897', '177', '730', '46'
			]
			unwanted_vert.extend(genetic)
			names = viruses('http://viralzone.expasy.org' + str(x), 'all_by_species', unwanted_vert)
			print(names)
			for virus in names:
				virus_url = 'http://viralzone.expasy.org' + str(virus)
				virus_tax_num = download(virus_url)
				ftp_download(virus_tax_num, store)
			fetch.taxonomy(store, './out/eukaryotic_organism_virus/', None)
		if '256' in str(x):
			# Viruses that attack Bacteria
			store = './dat/bacteria_virus/'
			path_to_dir(store)
			unwanted_vert = [
				'14', '146', '160', '140', '142', '141', '113',
				'114', '165', '163'
				]
			unwanted_vert.extend(genetic)
			# names = viruses('http://viralzone.expasy.org' + str(x), 'all_by_species', unwanted_vert)
			# print(names)
			# for virus in names:
			# 	virus_url = 'http://viralzone.expasy.org' + str(virus)
			# 	virus_tax_num = download(virus_url)
			# 	ftp_download(virus_tax_num, store)
			fetch.taxonomy(store, './out/bacteria_viruses/', None)
			break
		elif '663' in str(x):
			# Viruses that attack Archaea
			unwanted_vert = [
			'3016', '713', '2918', '20', '234', '535',
			'143', '140', '159', '4742', '2576'
			]
			unwanted_vert.extend(genetic)
			names = viruses('http://viralzone.expasy.org' + str(x), 'all_by_species', unwanted_vert)
			print(names)
			for virus in names:
				virus_url = 'http://viralzone.expasy.org' + str(virus)
				virus_tax_num = download(virus_url)
				ftp_download(virus_tax_num, store)
			fetch.taxonomy(store, './out/archaea_virus/', None)