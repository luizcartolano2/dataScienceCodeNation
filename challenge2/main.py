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
		# student['MEDIA_S_MT']	= (3*file['NU_NOTA_REDACAO'][index] + 1.5*file["NU_NOTA_LC"][index] + file["NU_NOTA_CH"][index] + 2*file["NU_NOTA_CN"][index])/(7.5)
		# student['MEDIA_S_MT']	= (file['NU_NOTA_REDACAO'][index] + file["NU_NOTA_LC"][index] + file["NU_NOTA_CH"][index] + file["NU_NOTA_CN"][index])/4
		student['MEDIA_S_MT']	= (file["NU_NOTA_LC"][index] + file["NU_NOTA_CH"][index] + file["NU_NOTA_CN"][index])/3
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
		student['NOTA_MT'] = file['NU_NOTA_MT'][index]
		# student['MEDIA_S_MT']	= (3*file['NU_NOTA_REDACAO'][index] + 1.5*file["NU_NOTA_LC"][index] + file["NU_NOTA_CH"][index] + 2*file["NU_NOTA_CN"][index])/(7.5)
		# student['MEDIA_S_MT']	= (file['NU_NOTA_REDACAO'][index] + file["NU_NOTA_LC"][index] + file["NU_NOTA_CH"][index] + file["NU_NOTA_CN"][index])/4
		student['MEDIA_S_MT']	= (file["NU_NOTA_LC"][index] + file["NU_NOTA_CH"][index] + file["NU_NOTA_CN"][index])/3
		students.append(student)

	x_axis, y_axis = [],[]
	for st in students:
		x_axis.append(st['MEDIA_S_MT'])
		y_axis.append(st['NOTA_MT'])
		
	del students[:]
	
	
	# Create linear regression object
	regr = linear_model.LinearRegression()
	# Train the model using the training sets
	regr.fit(np.transpose(np.matrix(x_axis)), np.transpose(np.matrix(y_axis)))
	
	# Make predictions using the testing set
	y_pred = regr.predict(np.transpose(np.matrix(x_axis)))

	coefficient_determination = regr.score(np.transpose(np.matrix(x_axis)), np.transpose(np.matrix(y_axis)))
	b_coefficient = regr.coef_[0][0]
	a_coefficient = regr.intercept_[0]
	variance = r2_score(y_axis, y_pred)
	
	return b_coefficient, a_coefficient, variance

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

def calcHit(studs, a, b, variance):
	for st in studs:
		st['NU_NOTA_MT'] = (b * st['MEDIA_S_MT']) + a + variance

	return studs

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
	file = readCSV(filename=filename)
	
	print("Get Interests:")
	students = getInterests(file=file)
	
	print("Getting the coefficients for our linear regression:")
	b,a,variance = trainingRegression()

	print("Getting grades of the students who did the test:")
	students = calcHit(studs=students,a=a,b=b,variance=variance)

	print("Calc math grade for people who miss the test:")
	students = calcMiss(studs=students)

	print("Formatting answer:")
	students = getAnswer(studs=students)

	print("Making HTTP post:")
	makeHTTPPost(studs=students)

if __name__ == '__main__':
	main()