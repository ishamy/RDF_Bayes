import codecs
from collections import defaultdict
import operator
import random
import sets
import numpy as np


#commentDict= {"awfull" :0 , "bad" :0, "good" :0, "insightfully" :0, "performed" :0}


def open_file():
	n=0   
	cptMotPos = 0 
	cptMotNeg = 0 
	cptMotTotal = 0   
	with codecs.open("data", "r",encoding="utf-8") as my_file:
		cptNeg =0
		cptPos = 0
		for line in my_file:
			line = line.strip()
			setPhrase[n] = line
			rank, rate, comment = line.split("|")
			if (float(rate) <= 0.5):
				setPhraseNeg[cptNeg] = line
				cptNeg +=1 
			else:	
				setPhrasePos[cptPos] = line
				cptPos +=1 
			n+=1
			com = comment.split(" ")
			for i in range(len(com)):
				#for j in range(len(dict)):
					#if com[i] == dict[j]:
						cptMotTotal +=1
						if com[i] in commentDict:
							commentDict[com[i]]+=1
						else :	
							dic2 = {com[i]: 1}			
							commentDict.update(dic2)
						
						if (float(rate) <= 0.5):
							cptMotNeg +=1
							if com[i] in commentDictNeg:
								commentDictNeg[com[i]]+=1
							else :	
								dic2 = {com[i]: 1}			
								commentDictNeg.update(dic2)
						else: 
							cptMotPos += 1
							if com[i] in commentDictPos:
								commentDictPos[com[i]]+=1
							else :	
								dic2 = {com[i]: 1}			
								commentDictPos.update(dic2)
	return cptMotTotal,cptMotPos ,cptMotNeg


def delete_n_lines(N):       
	list_trie = sorted(commentDict.iteritems(), reverse=True, key=operator.itemgetter(1))
	del list_trie[0:N]


def compute_vectors():  
	appr = 0.8
	dev = 0.1
	test = 0.1  
	
	apprentissageLen = int(float(appr)*len(setPhrase));
	devLen =int(float(dev)*len(setPhrase));
	testLen = int(float(test)*len(setPhrase));
	
	# remplissage de l'ensemble d'apprentissage
	i =0
	while i< apprentissageLen:
		r = random.randint(0, len(setPhrase)-1)
		if (setPhrase[r] not in setApprent):
			setApprent[i] = setPhrase[r]
			i+= 1
	# remplissage de l'ensemble de dev
	i =0
	while i< devLen:
		r = random.randint(0, len(setPhrase) -1)
		if (setPhrase[r] not in setApprent and setPhrase[r] not in setDev):
			setDev[i] = setPhrase[r]
			i+= 1
	
	# remplissage de l'ensemble de test
	i =0
	while i< testLen:
		r = random.randint(0, len(setPhrase)-1 )
		if (setPhrase[r] not in setApprent and setPhrase[r] not in setDev and setPhrase[r] not in setTest ):
			setTest[i] = setPhrase[r]
			i+=1
	
	for i in range(len(setTest)):
		line = setTest[i]
		rank, rate, comment = line.split("|")
		com = comment.split(" ")
		for i in range(len(com)):
			setMotTest.add(com[i])
			if com[i] in testDict:
				testDict[com[i]]+=1
			else :	
				dic2 = {com[i]: 1}			
				testDict.update(dic2)
	
	for i in range(len(setApprent)):
		line = setApprent[i]
		rank, rate, comment = line.split("|")
		com = comment.split(" ")
		for i in range(len(com)):
			setMotApprent.add(com[i])
			if com[i] in apprendDict:
				apprendDict[com[i]]+=1
			else :	
				dic2 = {com[i]: 1}			
				apprendDict.update(dic2)

"""

on veut pour chaque mot la proba qu'il apparraisse dans une phrase positive et une phrase negative
(p(x|y) * p(y)) 

parcourir le setmot apprent
	recuperer dans commentDict
	recuperer dans commentDictNeg
	recuperer dans commentDictPos
"""

def compute_proba_apprent():  
	gamma  = 0.1
	for i in setMotApprent:
		valTotal = 0
		valPos = 0
		valNeg = 0
		if i in	commentDict:
			valTotal = commentDict[i]
		if i in	commentDictNeg: # recuperer nb occurence dans phrase negatives
			valNeg = float (commentDictNeg[i])/ float (cptMotNeg)
		if i in	commentDictPos: # recuperer nb occurence dans phrase positives
			valPos =  float (commentDictPos[i])/ float (cptMotPos)
	
		#proba d'avoir une phrase negative
		probaPhraseNeg = (float(len(setPhraseNeg))/ float (len(setPhrase) )) 
		#proba d'avoir une phrase positive
		probaPhrasePos = (float(len(setPhrasePos))/ float (len(setPhrase) ))
		
		#proba d'avoir ce mot dans une phrase neg * proba d'avoir phrase neg
		probaNeg = (valNeg * float(probaPhraseNeg) + gamma ) 
		#proba d'avoir ce mot dans une phras epos * proba d'avoir phrase pos
		probaPos = (valPos * float(probaPhrasePos) + gamma )
		
		dic2 = {i: probaNeg}			
		dictProbaNeg.update(dic2)
		dic3 = {i: probaPos}			
		dictProbaPos.update(dic3)

def compute_proba_test():  
	cptErreur =0
	cptTotal =0
	matrice=np.array([0,0,0,0])
	for i in range(len(setTest)):
		rank, rate, comment = setPhrase[i].split("|")
		com = comment.split(" ")
		cptP = 0
		cptN = 0
		for i in range(len(com)):
			if com[i] in dictProbaNeg:
				cptN+= dictProbaNeg[com[i]]
			if com[i] in dictProbaPos:
				cptP+= dictProbaPos[com[i]]
		if cptP < cptN and float(rate) > 0.5 :
			cptErreur += 1
			matrice[1] += 1
		elif cptP > cptN and float(rate) <= 0.5 :
			cptErreur += 1
			matrice[2] += 1
		elif cptP < cptN and float(rate) <= 0.5 :
			matrice[0] += 1
		elif cptP > cptN and float(rate) > 0.5 :
			matrice[3] += 1
		cptTotal += 1
	matrice=matrice.reshape(2,2)
	print matrice
	print float(cptErreur ) /float(cptTotal )
		
commentDict = {} #dictionnaire des comptes de chaque mot
commentDictNeg = {} #dictionnaire des comptes de chaque mot dans les phrase positives
commentDictPos = {}#dictionnaire des comptes de chaque mot dans les phrase negatives

#dict = ["awfull", "bad", "good", "insightfully", "performed"]
setPhrase = {}  # tableau de toutes les phrases
setPhraseNeg = {}# tableau de toutes les phrases negatives
setPhrasePos = {} # tableau de toutes les phrases positives


dictProbaNeg = {}  # dictionnaire de proba pour phrase Negative
dictProbaPos = {}# dictionnaire de proba pour phrase Positive

setApprent = {} #ensemble des phrases pour l'apprentissage
setDev = {} #ensemble des phrases pour le dev
setTest = {} #ensemble des phrases pour les test

apprendDict = {} # dictionnaire de compte pour ensemble d'apprent
setMotApprent = set() # set de tous les mots dans ensemble d'apprent
testDict = {} # dictionnaire de compte pour ensemble de test
setMotTest = set() # set de tous les mots dans ensemble de test

cptMotTotal, cptMotPos, cptMotNeg = open_file()

compute_vectors()
compute_proba_apprent()
compute_proba_test()

