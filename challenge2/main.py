# -*- coding: utf-8 -*-
import pandas as pd
import requests
import httplib, urllib
import json

def readCSV(filename):
	file = pd.read_csv(filename)
	file = file.fillna(0)
	
	return file
	
def getInterests(file):
	students = []
	for index in file.index:
		student = {}
		student['NU_INSCRICAO'] = file['NU_INSCRICAO'][index]
		student['NU_NOTA_CN'] = file['NU_NOTA_CN'][index]
		student['NU_NOTA_CH'] = file['NU_NOTA_CH'][index]
		student['NU_NOTA_LC'] = file['NU_NOTA_LC'][index]
		student['NU_NOTA_MT'] = None
		student['TP_PRESENCA_LC'] = file['TP_PRESENCA_LC'][index]
		students.append(student)

	return students

def calcMat(studs):
	students = []

	del studs[:]
	return students	


def calcMiss(studs):
	# people who miss the LC test also miss the MT test
	for st in studs:
		if st['TP_PRESENCA_LC'] == 0 or st['TP_PRESENCA_LC'] == 2:
			st['NU_NOTA_MT'] = 0

	return studs

def makeHTTPPost(studs):
	url = "https://api.codenation.com.br/v1/user/acceleration/data-science/challenge/enem-2/submit"

	params = urllib.urlencode({'@token': 'd78738ec890de3cf6b3f887ebd5b1a1c9929da0b',
							   '@email': 'cartolanoluiz@gmail.com', 
							   '@answer': studs})

	payload = {'token': 'd78738ec890de3cf6b3f887ebd5b1a1c9929da0b', 'email': 'cartolanoluiz@gmail.com', 'answer': studs}
	data_to_send = json.dumps(payload).encode("utf-8")

	r = requests.post(url, data=data_to_send)
	print(r.text)


def getAnswer(studs):
	students = []
	for st in studs:
		student = {}
		student['NU_INSCRICAO'] = st['NU_INSCRICAO']
		student['NU_NOTA_MT']	 = st['NU_NOTA_MT']
		students.append(student)

	del studs[:]
	return students
 
def main():
	filename = "/Users/luizeduardocartolano/Dropbox/DUDU/python-test/dataScience/challenge2/test2.csv"
	
	print("Reading file:")
	file = readCSV(filename)
	
	print("Get Interests:")
	students = getInterests(file)
	
	print("Calc math grade for people who miss the test:")
	students = calcMiss(students)
	
	# students = getAnswer(students)

	# print("Making HTTP post:")
	# makeHTTPPost(students)

if __name__ == '__main__':
	main()