#!/usr/bin/python
import re, os, json, urllib, requests, httplib2
from bs4 import BeautifulSoup

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
	# print(redirect)
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
					# else:
					# 	for x in viruses:
					# 		if not tax_num == x:
					# 			viruses.append(str(y.split('/')[2]))
					# 		else:
					# 			pass
			print(output)
	print('No. of preoteomes to be retrieved: ' + str(num))


def remove_duplicates(viruses):
	output = []
	visited = set()
	for virus in viruses:
		if virus not in visited:
			output.append(virus)
			visited.add(virus)
	return output


def taxonomy():
	pass

if __name__ == '__main__':
	url = 'http://viralzone.expasy.org/all_by_species/678.html'
	urls = init(url)
	uniprot(urls)