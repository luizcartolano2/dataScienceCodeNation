# -*- coding: utf-8 -*-
import pandas as pd
import requests
import httplib, urllib
import json
import numpy as np
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score


def readCSV(filename):
	file = pd.read_csv(filename)
	file = file.fillna(0)
	
	return file
	
def getInterests(file):
	students = []
	for index in file.index:
		student = {}
		student['NU_INSCRICAO'] = file['NU_INSCRICAO'][index]
		student['TX_RESPOSTAS_MT'] = file['TX_RESPOSTAS_MT'][index]
		students.append(student)

	return students

def makeHTTPPost(studs):
	url = "https://api.codenation.com.br/v1/user/acceleration/data-science/challenge/enem-3/submit"

	params = urllib.urlencode({'@token': 'd78738ec890de3cf6b3f887ebd5b1a1c9929da0b',
							   '@email': 'cartolanoluiz@gmail.com', 
							   '@answer': studs})

	payload = {'token': 'd78738ec890de3cf6b3f887ebd5b1a1c9929da0b', 'email': 'cartolanoluiz@gmail.com', 'answer': studs}
	data_to_send = json.dumps(payload).encode("utf-8")

	r = requests.post(url, data=data_to_send)
	print(r.text)
 
def main():
	filename = "/Users/luizeduardocartolano/Dropbox/DUDU/python-test/dataScience/challenge3/test3.csv"
	
	print("Reading file:")
	file = readCSV(filename=filename)
	
	print("Get Interests:")
	students = getInterests(file=file)

	# print("Making HTTP post:")
	# makeHTTPPost(studs=students)

if __name__ == '__main__':
	main()