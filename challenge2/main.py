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
		student['NU_NOTA_CN'] = file['NU_NOTA_CN'][index]
		student['NU_NOTA_CH'] = file['NU_NOTA_CH'][index]
		student['NU_NOTA_LC'] = file['NU_NOTA_LC'][index]
		student['NU_NOTA_MT'] = None
		student['TP_PRESENCA_LC'] = file['TP_PRESENCA_LC'][index]
		students.append(student)

	return students

def trainingRegression():
	filename = "/Users/luizeduardocartolano/Dropbox/DUDU/python-test/dataScience/challenge1/train.csv"
	file = readCSV(filename)
	
	students = []
	for index in file.index:
		student = {}
		student['NU_NOTA_CN'] = file['NU_NOTA_CN'][index]
		student['NU_NOTA_CH'] = file['NU_NOTA_CH'][index]
		student['NU_NOTA_LC'] = file['NU_NOTA_LC'][index]
		student['NU_NOTA_MT'] = file['NU_NOTA_MT'][index]
		
		if file['TX_RESPOSTAS_CN'][index] != 0:
			cn_choices = list(file['TX_RESPOSTAS_CN'][index])
			cn_gab = list(file['TX_GABARITO_CN'][index])
			student['QUESTOES_CN'] = findRightAnswers(cn_choices, cn_gab)
		else:
			student['QUESTOES_CN'] = 0
		
		if file['TX_RESPOSTAS_CH'][index] != 0:
			ch_choices = list(file['TX_RESPOSTAS_CH'][index])
			ch_gab = list(file['TX_GABARITO_CH'][index])
			student['QUESTOES_CH'] = findRightAnswers(ch_choices, ch_gab)
		else:
			student['QUESTOES_CH'] = 0
		
		if file['TX_RESPOSTAS_LC'][index] != 0:
			lc_choices = list(file['TX_RESPOSTAS_LC'][index])
			lc_gab = list(file['TX_GABARITO_LC'][index])
			student['QUESTOES_LC'] = findRightAnswers(lc_choices, lc_gab)
		else:
			student['QUESTOES_LC'] = 0
		
		if file['TX_RESPOSTAS_MT'][index] != 0:
			mt_choices = list(file['TX_RESPOSTAS_MT'][index])
			mt_gab = list(file['TX_GABARITO_MT'][index])
			student['QUESTOES_MT'] = findRightAnswers(mt_choices, mt_gab)
		else:
			student['QUESTOES_MT'] = 0
		
		students.append(student)

	x_axis, y_axis = [],[]
	for st in students:
		x_axis.append(st['QUESTOES_CN'])
		x_axis.append(st['QUESTOES_CH'])
		x_axis.append(st['QUESTOES_LC'])
		x_axis.append(st['QUESTOES_MT'])
		y_axis.append(st['NU_NOTA_CN'])
		y_axis.append(st['NU_NOTA_CH'])
		y_axis.append(st['NU_NOTA_LC'])
		y_axis.append(st['NU_NOTA_MT'])

	del students[:]
	
	# plt.scatter(x_axis,y_axis)
	# plt.show()

	# X = np.array([])
	# for x in x_axis:
	# 	X = np.append(X, x)

	# X = X.reshape(1,-1)
	
	# Create linear regression object
	regr = linear_model.LinearRegression()
	# Train the model using the training sets
	regr.fit(np.transpose(np.matrix(x_axis)), np.transpose(np.matrix(y_axis)))

	coefficient_determination = regr.score(np.transpose(np.matrix(x_axis)), np.transpose(np.matrix(y_axis)))
	

def findRightAnswers(choices, gab):
	size = len(choices)
	count = 0

	for i in range(size):
		if choices[i] == gab[i]:
			count = count + 1

	return count

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
	
	# print("Reading file:")
	# file = readCSV(filename)
	
	# print("Get Interests:")
	# students = getInterests(file)
	
	# print("Calc math grade for people who miss the test:")
	# students = calcMiss(students)
	
	trainingRegression()

	# students = getAnswer(students)

	# print("Making HTTP post:")
	# makeHTTPPost(students)

if __name__ == '__main__':
	main()