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

url = 'http://viralzone.expasy.org/all_by_species/678.html'
response = requests.get(url)

soup = BeautifulSoup(response.content)

print(soup.prettify())
num = 0

for link in soup.find_all('a'):
	redirect = link.get('href')
	if re.search('uniprot', str(redirect)):
		num+=1
		print(redirect)
print('No. of preoteomes to be retrieved: ' + str(num))
