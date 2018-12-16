#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 15 01:40:41 2018

@author: chiranjeev
"""

import urllib.request as uReq
                         
from bs4 import BeautifulSoup 

#import pickle                                 # important to save data 

site = "http://www.imdb.com/chart/moviemeter"
uClient = uReq.urlopen(site)
page_html = uClient.read()
uClient.close()

soup = BeautifulSoup(page_html,"html.parser")

containers = soup.findAll("tbody",{"class":"lister-list"})
print(len(containers))    #1

print(type(containers[0]))

rows = containers[0].findAll("tr")

dataSet = {
	'Name Of Movie':[],
	'Year Of Release':[],
	'Ranking Change_Jump':[],
	'Change':[],
	'Users_count':[],
	'Rating':[]

}

# for saving the data
file = open("Movies.csv","w+")

# Columns of the dataset
file.write('Name Of Movie'+','+'Year Of Release'+','+'Ranking Change_Jump'+','+'Change'+','+'Users_count'+','+'Rating'+'\n')

# Iterating over column and saving results to the dataset
for i in range(len(rows)):
	
    # Add Names of the movies to the dataset Dictionary
	dataSet['Name Of Movie'].append(rows[i].find("td",{"class":"titleColumn"}).find("a").text)

    # Add Release Year of the movies to the dataset Dictionary
	dataSet['Year Of Release'].append(int(rows[i].find("td",{"class":"titleColumn"}).find("span").text.split('(')[1].split(')')[0]))
	
    # Adding jump in change of popularity
	if (rows[i].find("td",{"class":"titleColumn"}).find("div").text.split('(')[1].split(')')[0] == 'no change'):
		dataSet['Ranking Change_Jump'].append('0')
	else:
		dataSet['Ranking Change_Jump'].append(rows[i].find("td",{"class":"titleColumn"}).find("div").text.split('(')[1].split(')')[0].split('\n')[2].replace(',',''))
	
    ## Add Change from previous state of the movies to the dataset Dictionary
	if (rows[i].find("td",{"class":"titleColumn"}).find("div").find("span") == None):
		dataSet['Change'].append('no change')
	else:
		dataSet['Change'].append(rows[i].find("td",{"class":"titleColumn"}).find("div").findAll("span")[1].attrs['class'][2])	


    # Adds totalno of users_count 
	try :
		dataSet['Users_count'].append(str(int(rows[i].find("td",{"class":["ratingColumn","imdbRating"]}).find("strong")['title'].split()[3].replace(',',''))))
	except TypeError:
		dataSet['Users_count'].append("")
	
    #Adds Rating of the movie
	dataSet['Rating'].append(rows[i].find("td",{"class":["ratingColumn","imdbRating"]}).text.split('\n')[1])

    
    # Write  All Scrapped details to the dataset
	file.write(str(dataSet['Name Of Movie'][i])+","+str(dataSet['Year Of Release'][i])+","+str(dataSet['Ranking Change_Jump'][i])+","+str(dataSet['Change'][i])+","+str(dataSet['Users_count'][i])+","+str(dataSet['Rating'][i])+"\n")

file.close()
#print(dataSet)