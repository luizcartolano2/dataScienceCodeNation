# -*- coding: utf-8 -*-
import pandas as pd
import requests
import httplib, urllib
import json
import numpy as np
from sklearn.neural_network import MLPClassifier

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
		student['answer'] = None
		students.append(student)

	return students

def makeHTTPPost(studs):
	url = "https://api.codenation.com.br/v1/user/acceleration/data-science/challenge/enem-3/submit"

	payload = {'token': 'd78738ec890de3cf6b3f887ebd5b1a1c9929da0b', 'email': 'cartolanoluiz@gmail.com', 'answer': studs}
	data_to_send = json.dumps(payload).encode("utf-8")

	# print(data_to_send)

	r = requests.post(url, data=data_to_send)
	print(r.text)

def getProbability(answers):
	a,b,c,d,e = [0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]
	lastAnswer = answers[0]
	actualAnswer = None
	size = len(answers)
	# print(size)
	for i in range(1,40):
		# print(str(i) + ' ' + str(answers[i]))
		actualAnswer = answers[i]
		if lastAnswer == 'A':
			if actualAnswer == 'A':
				a[0] = a[0] + 1
			elif actualAnswer == 'B':
				a[1] = a[1] + 1
			elif actualAnswer == 'C':
				a[2] = a[2] + 1
			elif actualAnswer == 'D':
				a[3] = a[3] + 1
			else:
				a[4] = a[4] + 1
		elif lastAnswer == 'B':
			if actualAnswer == 'A':
				b[0] = b[0] + 1
			elif actualAnswer == 'B':
				b[1] = b[1] + 1
			elif actualAnswer == 'C':
				b[2] = b[2] + 1
			elif actualAnswer == 'D':
				b[3] = b[3] + 1
			else:
				b[4] = b[4] + 1
		elif lastAnswer == 'C':
			if actualAnswer == 'A':
				c[0] = c[0] + 1
			elif actualAnswer == 'B':
				c[1] = c[1] + 1
			elif actualAnswer == 'C':
				c[2] = c[2] + 1
			elif actualAnswer == 'D':
				c[3] = c[3] + 1
			else:
				c[4] = c[4] + 1
		elif lastAnswer == 'D':
			if actualAnswer == 'A':
				d[0] = d[0] + 1
			elif actualAnswer == 'B':
				d[1] = d[1] + 1
			elif actualAnswer == 'C':
				d[2] = d[2] + 1
			elif actualAnswer == 'D':
				d[3] = d[3] + 1
			else:
				d[4] = d[4] + 1
		else:
			if actualAnswer == 'A':
				e[0] = e[0] + 1
			elif actualAnswer == 'B':
				e[1] = e[1] + 1
			elif actualAnswer == 'C':
				e[2] = e[2] + 1
			elif actualAnswer == 'D':
				e[3] = e[3] + 1
			else:
				e[4] = e[4] + 1
		lastAnswer = answers[i]

	totalAnswersA = a[0] + a[1] + a[2] + a[3] + a[4]
	totalAnswersB = b[0] + b[1] + b[2] + b[3] + b[4]
	totalAnswersC = c[0] + c[1] + c[2] + c[3] + c[4]
	totalAnswersD = d[0] + d[1] + d[2] + d[3] + d[4]
	totalAnswersE = e[0] + e[1] + e[2] + e[3] + e[4]

	if totalAnswersA != 0:
		probA = [float(float(a[0])/float(totalAnswersA)),float(float(a[1])/float(totalAnswersA)),float(float(a[2])/float(totalAnswersA)),float(float(a[3])/float(totalAnswersA)),float(float(a[4])/float(totalAnswersA))]
	else:
		probA = [0,0,0,0,0]
	if totalAnswersB != 0:
		probB = [float(float(b[0])/float(totalAnswersB)),float(float(b[1])/float(totalAnswersB)),float(float(b[2])/float(totalAnswersB)),float(float(b[3])/float(totalAnswersB)),float(float(b[4])/float(totalAnswersB))]
	else:
		probB = [0,0,0,0,0]
	if totalAnswersC != 0:
		probC = [float(float(c[0])/float(totalAnswersC)),float(float(c[1])/float(totalAnswersC)),float(float(c[2])/float(totalAnswersC)),float(float(c[3])/float(totalAnswersC)),float(float(c[4])/float(totalAnswersC))]
	else:
		probC = [0,0,0,0,0]
	if totalAnswersD != 0:
		probD = [float(float(d[0])/float(totalAnswersD)),float(float(d[1])/float(totalAnswersD)),float(float(d[2])/float(totalAnswersD)),float(float(d[3])/float(totalAnswersD)),float(float(d[4])/float(totalAnswersD))]
	else:
		probD = [0,0,0,0,0]
	if totalAnswersE != 0:
		probE = [float(float(e[0])/float(totalAnswersE)),float(float(e[1])/float(totalAnswersE)),float(float(e[2])/float(totalAnswersE)),float(float(e[3])/float(totalAnswersE)),float(float(e[4])/float(totalAnswersE))]
	else:
		probE = [0,0,0,0,0]

	del a[:]
	del b[:]
	del c[:]
	del d[:]
	del e[:]

	a = getBigger(probA)
	del probA[:]
	b = getBigger(probB)
	del probB[:]
	c = getBigger(probC)
	del probC[:]
	d = getBigger(probD)
	del probD[:]
	e = getBigger(probE)
	del probE[:]

	return a,b,c,d,e

def getBigger(probs):
	small = 0
	for i in range(0,len(probs)):
		if probs[i] > probs[small]:
			small = i

	if small == 0:
		return 'A'
	elif small == 1:
		return 'B'
	elif small == 1:
		return 'C'
	elif small == 1:
		return 'D'
	else:
		return 'E'

def getAnswers(lastAnswer, a, b, c, d, e):
	answer = ''
	for i in range(0,5):
		if lastAnswer == 'A':
			answer = answer + a
			lastAnswer = a
		elif lastAnswer == 'B':
			answer = answer + b
			lastAnswer = b
		elif lastAnswer == 'C':
			answer = answer + c
			lastAnswer = c
		elif lastAnswer == 'D':
			answer = answer + d
			lastAnswer = d
		else:
			answer = answer + e
			lastAnswer = e

	return answer

def markovChain(studs):
	students = []
	for st in studs:
		student = {}
		student['NU_INSCRICAO'] = st['NU_INSCRICAO']
		respostas = list(st['TX_RESPOSTAS_MT'])
		# print(respostas)
		a,b,c,d,e = getProbability(respostas)
		student['answer'] = str(getAnswers(respostas[39],a,b,c,d,e))
		students.append(student)
				
	del studs[:]
	return students

def main():
	filename = "/Users/luizeduardocartolano/Dropbox/DUDU/python-test/dataScience/challenge3/test3.csv"
	
	print("Reading file:")
	file = readCSV(filename=filename)
	
	print("Get Interests:")
	students = getInterests(file=file)

	print("Applying Markov Chain:")
	students = markovChain(students)

	print("Making HTTP post:")
	makeHTTPPost(studs=students)

if __name__ == '__main__':
	main()