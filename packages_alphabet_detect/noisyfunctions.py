import numpy as np
import matplotlib.pyplot as plt
import glob
from PIL import Image
import pandas as pd
import math
import time
import random
import copy
from collections import Counter


def get_images(alpha,path='Machine Learning - Assignment 1/Assignment 1 Dataset/'):
    alphabet=alpha
    allimages=[]
    allimages_test=[]
    for id_char,x in enumerate(alphabet):
        for filename in glob.glob(path+'Train/A1'+str(x)+'*'):
            im=Image.open(filename)
            templ=list(im.getdata())
            allimages.append([templ,id_char,filename.split('/')[-1]])    
        for filename in glob.glob(path+'Test/A1'+str(x)+'*'):
            im=Image.open(filename)
            templ=list(im.getdata())
            allimages_test.append([templ,id_char,filename.split('/')[-1]])
    return allimages,allimages_test

#get the euclidean distance 
def distanceCal(p1,p2):
    if len(p1)==len(p2):
        distance=0
        for i in range(len(p1)):
            distance+=abs(p1[i]**2-p2[i]**2)**0.5
        return distance
    else:
        return -1


def getDistancesMatrixSorted(training):
    t1=time.time()
    alldistances_sorted=[]
    lengthoftrain=len(training)
    for i in range(0,lengthoftrain):
        distances=[]
        for j in range(lengthoftrain):
            distances.append([distanceCal(training[i][0],training[j][0]),j,training[j][1]])
        distances.sort(key=lambda x: x[0])
        alldistances_sorted.append(distances[1:])
    print (int(time.time()-t1)," sec.")
    return alldistances_sorted



def getAllIndicies(training,alphabet):
    allindicies=[]
    for alphaindex in range(len(alphabet)):
        eachalphabetindces=[]
        for i,x in enumerate(training):
            if x[1]==alphaindex:
                eachalphabetindces.append(i)
        allindicies.append(eachalphabetindces)
    return allindicies


def splitrandomlist(split,allindicies):
    split1=[]
    split2=[]
    for row in allindicies:
        rowrandom=copy.deepcopy(row)
        random.shuffle(rowrandom)
        split1.append(rowrandom[:int(len(row)*split)])
        split2.append(rowrandom[int(len(row)*split):])
    return split1,split2


def getKresultslist(k,testinglist,distancesMatrix):
    #k=6
    errors=0
    kresultslist=[]
    lista=[]
    for alphaindex,train20row in enumerate(testinglist):
        for testelement in train20row:
            lista=[]
            for distances in distancesMatrix[testelement][:k]:
                #if the majority is not = to alphaindex
                lista.append(distances[2])
            kresultslist.append([testelement,alphaindex,lista])
    return kresultslist

def calculatenearestk(k,testpoint, trainingdata):
    distanceslist=[]
    for i,train in enumerate(trainingdata):
        distanceslist.append([train[1],distanceCal(testpoint,train[0])])
    distanceslist.sort(key=lambda x:x[1])
    distancesk=list(np.array(distanceslist).T[0])
    return distancesk[:k]

def getErrorList2(klist,alldistances_sorted):
    error_all=[]
    for testrowerror in klist:
        error=0
        cou=Counter(testrowerror[2])
        mcommon=cou.most_common()
        #if there's an agreement on vote
        if len(mcommon)==1:
            # if this agreement is wrong:
            if mcommon[0][0]!= testrowerror[1]: 
                error_all.append(1)

        else:
            # if there's a majority
            if mcommon[0][1] != mcommon[1][1]:
                # if this majority is false:
                if mcommon[0][0]!= testrowerror[1]:
                    #error++
                    error_all.append(1)

            else:
                #check the one closest 
                if alldistances_sorted[testrowerror[0]][0][2] != testrowerror[1]:
                    error_all.append(1)

                
    return error_all

def getErrorList(klist,alldistances_sorted):
    error_all=[]
    for klistelement in klist:
        if getMajority(klistelement[2])!= klistelement[1]:
            error_all.append(1)
    return error_all



def getMajority(listtocheck):

        cou=Counter(listtocheck)
        mcommon=cou.most_common()
        #if there's an agreement on vote
        if len(mcommon)==1:
            return mcommon[0][0]
        else:
            # if there's a majority
            if mcommon[0][1] != mcommon[1][1]:
                return mcommon[0][0]
            else:
                #check the one closest 
                return listtocheck[0]

