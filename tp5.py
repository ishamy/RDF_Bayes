import codecs
from collections import defaultdict
import operator
import random
import sets
import numpy as np
from random import shuffle
import math  
#commentDict= {"awfull" :0 , "bad" :0, "good" :0, "insightfully" :0, "performed" :0}


def open_file():
	n=0   
	cptMotPos = 0 
	cptMotNeg = 0 
	cptMotTotal = 0  
	setPhrase = list()
	setPhraseNeg = list()
	setPhrasePos = list()
	with codecs.open("data", "r",encoding="utf-8") as my_file:
		cptNeg =0
		cptPos = 0
		for line in my_file:
			line = line.strip()
			setPhrase.insert(n,line)
			#setPhrase[n] = line
			rank, rate, comment = line.split("|")
			if (float(rate) <= 0.5):
				#setPhraseNeg[cptNeg] = line
				setPhraseNeg.insert(cptNeg,line)
				cptNeg +=1 
			else:	
				setPhrasePos.insert(cptPos,line)
				#setPhrasePos[cptPos] = line
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
	return cptMotTotal,cptMotPos ,cptMotNeg,setPhrase,setPhraseNeg,setPhrasePos


def delete_n_lines(N , list_trie):       
	#list_trie = sorted(commentDict.iteritems(), reverse=True, key=operator.itemgetter(1))
	del list_trie[0:N]
	return list_trie;

def compute_vectors(setPhrase,setPhraseNeg,setPhrasePos ):  
	appr = 0.8
	dev = 0.1
	test = 0.1  
	
	apprentissageLen = int(float(appr)*len(setPhrase));
	devLen =int(float(dev)*len(setPhrase));
	testLen = int(float(test)*len(setPhrase));
	random.seed(None);

	setPhraseCopy = list(setPhrase);

	setApprent = list()
	setDev = list()
	setTest = list()
	shuffle(setPhraseCopy);
	random.seed(None);

	
	for i in range(apprentissageLen):
		setApprent.append(setPhraseCopy[i])
	setPhraseCopy = delete_n_lines(apprentissageLen,setPhraseCopy)

	for i in range(devLen):
		setDev.append(setPhraseCopy[i])
	setPhraseCopy = delete_n_lines(devLen,setPhraseCopy)

	for i in range(testLen):
		setTest.append(setPhraseCopy[i])
	setPhraseCopy = delete_n_lines(testLen,setPhraseCopy)

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
	cptMotNeg =0
	cptMotPos = 0
	cptPhraseNeg = 0
	cptPhrasePos = 0
	setPhraseNegApprent = list ()
	setPhrasePosApprent = list()
	for i in range(len(setApprent)):
		line = setApprent[i]
		rank, rate, comment = line.split("|")
		com = comment.split(" ")
		
		if (float(rate) <= 0.5):
			setPhraseNegApprent.insert(cptPhraseNeg,line)
			cptPhraseNeg +=1
		else :
			setPhrasePosApprent.insert(cptPhrasePos,line)
			cptPhrasePos += 1
		for i in range(len(com)):
			setMotApprent.add(com[i])
			if com[i] in apprendDict:
				apprendDict[com[i]]+=1
			else :	
				dic2 = {com[i]: 1}			
				apprendDict.update(dic2)
			
			if (float(rate) <= 0.5):
				cptMotNeg +=1
				if com[i] in apprendDictNeg:
					apprendDictNeg[com[i]]+=1
				else :	
					dic2 = {com[i]: 1}			
					apprendDictNeg.update(dic2)
			else: 
				cptMotPos += 1
				if com[i] in apprendDictPos:
					apprendDictPos[com[i]]+=1
				else :	
					dic2 = {com[i]: 1}			
					apprendDictPos.update(dic2)
	return setApprent,setDev,setTest,setPhrasePosApprent, setPhraseNegApprent
"""

on veut pour chaque mot la proba qu'il apparraisse dans une phrase positive et une phrase negative
(p(x|y) * p(y)) 

parcourir le setmot apprent
	recuperer dans commentDict
	recuperer dans commentDictNeg
	recuperer dans commentDictPos
"""

def compute_proba_apprent(setPhrase,setMotApprent,setApprent):  
	gamma  = 0.01
	nbPos= 0
	nbNeg= 0
	for line in setApprent:
		rank, rate, comment = line.split("|")
		if float(rate ) <= 0.5:
			nbNeg+= 1
		else :
			nbPos += 1

	for i in setMotApprent:
		valTotal = 0
		valPos = 0
		valNeg = 0
		if i in	commentDict:
			valTotal = commentDict[i]
		if i in	apprendDictNeg: # recuperer nb occurence dans phrase negatives
			valNeg = float (apprendDictNeg[i])/ float (len(setPhraseNegApprent))
		if i in	apprendDictPos: # recuperer nb occurence dans phrase positives
			valPos =  float (apprendDictPos[i])/ float (len(setPhrasePosApprent))
		#proba d'avoir une phrase negative
		probaPhraseNeg = (float(nbPos)/ float (len(setApprent) )) 
		#proba d'avoir une phrase positive
		probaPhrasePos = (float(nbNeg)/ float (len(setApprent) ))
		
		#proba d'avoir ce mot dans une phrase neg * proba d'avoir phrase neg
		probaNeg = (valNeg * float(probaPhraseNeg) + gamma ) 
		#proba d'avoir ce mot dans une phras epos * proba d'avoir phrase pos
		probaPos = (valPos * float(probaPhrasePos) + gamma )

		dic2 = {i: probaNeg}			
		dictProbaNegApprent.update(dic2)
		dic3 = {i: probaPos}			
		dictProbaPosApprent.update(dic3)

def compute_proba_test(setPhrase,setTest):  
	cptErreur =0
	cptTotal =0
	matrice=np.array([0,0,0,0])
	cpt = 0
	for i in range(len(setTest)):
		rank, rate, comment = setPhrase[i].split("|")
		com = comment.split(" ")
		cptP = 1
		cptN = 1
		for i in range(len(com)):
			if com[i] in dictProbaNegApprent:
				cptN*=  dictProbaNegApprent[com[i]] 
			if com[i] in dictProbaPosApprent:
				cptP*=  dictProbaPosApprent[com[i]]
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


def computeCaract(setMotApprent,setApprent):
	for mot in setMotApprent:
		cptPos = 0
		cptNeg = 0
		cptMot = 0
		cptAbsPos = 0
		cptAbsNeg = 0
		if mot in apprendDictNeg:
			cptNeg = apprendDictNeg[mot]
		if mot in apprendDictPos:
			cptPos = apprendDictPos[mot]
		cptAbsPos = (float(len(setPhrasePosApprent)) -  float(cptPos))
		cptAbsNeg = (float(len(setPhraseNegApprent)) -  float(cptNeg))
		
		caractNeg =  float(cptNeg) / float(len(setApprent))
		caractPos =  float(cptPos) / float(len(setApprent))
		caractPosAbs =  float(cptAbsPos) / float(len(setApprent))
		caractNegAbs =  float(cptAbsNeg) / float(len(setApprent))
		
		dic2 = {mot: caractPos}			
		dictCaractPosApprent.update(dic2)
		dic3 = {mot: caractNeg}			
		dictCaractNegApprent.update(dic3)
		
		dic4 = {mot: caractPosAbs}	
		dictCaractPosAbsApprent.update(dic4)
		dic5 = {mot: caractNegAbs}	
		dictCaractNegAbsApprent.update(dic5)
		print caractPosAbs
		print caractNegAbs

		if (caractNeg < caractPos and caractPosAbs < caractNegAbs):
			print "positif"
			print mot
		elif (caractNeg > caractPos and caractPosAbs > caractNegAbs):
			print "negatif"
			print mot
		print "------------------------"
		
def recup_N_info(Nmin,Nmax):
	list_trie = sorted(dictCaractPosApprent.iteritems(), reverse=True, key=operator.itemgetter(1))
	for i in range (float(Nmin),float(Nmax)):
		print list_trie[i]
	print "----------------"
	list_trie = sorted(dictCaractNegApprent.iteritems(), reverse=True, key=operator.itemgetter(1))
	for i in range (float(Nmin),float(Nmax)):
		print list_trie[i]
	print "----------------"
	list_trie = sorted(dictCaractPosAbsApprent.iteritems(), reverse=True, key=operator.itemgetter(1))
	for i in range (float(Nmin),float(Nmax)):
		print list_trie[i]
	print "----------------"
	list_trie = sorted(dictCaractNegAbsApprent.iteritems(), reverse=True, key=operator.itemgetter(1))
	for i in range (float(Nmin),float(Nmax)):
		print list_trie[i]	
		
commentDict = {} #dictionnaire des comptes de chaque mot
commentDictNeg = {} #dictionnaire des comptes de chaque mot dans les phrase positives
commentDictPos = {}#dictionnaire des comptes de chaque mot dans les phrase negatives

#dict = ["awfull", "bad", "good", "insightfully", "performed"]
setPhrase = []  # tableau de toutes les phrases
setPhraseNeg = []# tableau de toutes les phrases negatives
setPhrasePos = [] # tableau de toutes les phrases positives



setApprent = [] #ensemble des phrases pour l'apprentissage
setDev = [] #ensemble des phrases pour le dev
setTest = [] #ensemble des phrases pour les test

setMotApprent = set() # set de tous les mots dans ensemble d'apprent
setPhraseNegApprent = []# tableau de toutes les phrases negatives d'apprent
setPhrasePosApprent = [] # tableau de toutes les phrases positives d'apprent

dictProbaNegApprent = {}  # dictionnaire de proba pour phrase Negative
dictProbaPosApprent = {}# dictionnaire de proba pour phrase Positive

apprendDict = {} # dictionnaire de compte pour ensemble d'apprent
apprendDictNeg = {} # dictionnaire de compte pour ensemble d'apprent des phrase negatives
apprendDictPos = {} # dictionnaire de compte pour ensemble d'apprent des phrase positives

dictCaractPosApprent = {} #proba qu'une phrase soit positive si un mot est present
dictCaractNegApprent = {} #proba qu'une phrase soit negative si un mot est present
dictCaractPosAbsApprent = {} #proba qu'une phrase soit positive si un mot est present
dictCaractNegAbsApprent = {} #proba qu'une phrase soit negative si un mot est present

testDict = {} # dictionnaire de compte pour ensemble de test
setMotTest = set() # set de tous les mots dans ensemble de test

cptMotTotal, cptMotPos, cptMotNeg, setPhrase, setPhraseNeg, setPhrasePos = open_file()

setApprent,setDev,setTest,setPhrasePosApprent,setPhraseNegApprent = compute_vectors(setPhrase,setPhraseNeg,setPhrasePos)
compute_proba_apprent(setPhrase,setMotApprent,setApprent)
compute_proba_test(setPhrase,setTest)
computeCaract(setMotApprent,setApprent)
