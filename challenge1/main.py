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
		student['NU_NOTA_MT'] = file['NU_NOTA_MT'][index]
		student['NU_NOTA_REDACAO'] = file['NU_NOTA_REDACAO'][index]
		students.append(student)

	return students

def calcAverage(studs):
	students = []

	for st in studs:
		student = {}
		student['NU_INSCRICAO'] = st['NU_INSCRICAO']
		average = (3*st['NU_NOTA_REDACAO'] + 3*st["NU_NOTA_MT"] + 1.5*st["NU_NOTA_LC"] + st["NU_NOTA_CH"] + 2*st["NU_NOTA_CN"])/(10.5)
		student['NOTA_FINAL'] = average
		students.append(student)

	del studs[:]
	return students	

def getTop20(studs):
	students = []
	studs = sorted(studs, key=lambda k: k['NOTA_FINAL'], reverse=True) 

	for i in range(0,20):
		students.append(studs[i])

	del studs[:]
	return students

def makeHTTPPost(studs):
	url = "https://api.codenation.com.br/v1/user/acceleration/data-science/challenge/enem-1/submit"

	params = urllib.urlencode({'@token': 'd78738ec890de3cf6b3f887ebd5b1a1c9929da0b',
							   '@email': 'cartolanoluiz@gmail.com', 
							   '@answer': studs})

	payload = {'token': 'd78738ec890de3cf6b3f887ebd5b1a1c9929da0b', 'email': 'cartolanoluiz@gmail.com', 'answer': studs}
	data_to_send = json.dumps(payload).encode("utf-8")

	r = requests.post(url, data=data_to_send)
	print(r.text)


def main():
	filename = "/Users/luizeduardocartolano/Dropbox/DUDU/python-test/dataScience/challenge1/train.csv"
	file = readCSV(filename)
	
	students = getInterests(file)
	
	students = calcAverage(students)

	top20 = getTop20(students)

	makeHTTPPost(top20)	

if __name__ == '__main__':
	main()