# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 19:45:35 2019

@author: Gradient
"""
import time
import csv
import itertools
from collections import Counter
import functools
from operator import add
import matplotlib.pyplot as plt
import numpy as np
from random import randint


def apriori(file, support):
    
    ## Start timer for pass 1
    startPass1 = time.perf_counter()
    ## First Pass 
    data = frequency(file)
    ## Time for First Pass
    pass1Time = time.perf_counter() - startPass1
    
    
    ## Get length of file 
    length = file_len(file)
    SUPPORT = length*support
    
    ## Counts
    file = open("counts_ap.txt", "w")
    for key, value in data.items():
        file.write("%s %s\n" % (key,value))
    file.close()
    
    ## Frequent items
    frequent = {k: v for k, v in data.items() if v >= SUPPORT}
    file = open("frequent_ap.txt", "w")
    for key, value in frequent.items():
        file.write("%s %s\n" % (key,value))
    file.close()
    
    ## Candidate Pairs
    pairs = {}
    for pair in itertools.combinations(frequent, 2):
        pairs[pair] = 0
    
    file = open("candidates_ap.txt", "w")
    for key, value in pairs.items():
        file.write("%s %s\n" % (key,value))
    file.close()
    
    startPass2 = time.perf_counter()
    
    ## Count of pairs
    data2 = frequency2(file, pairs)
   
    ## Frequent pairs
    frequent2 = {k: v for k, v in data2.items() if v >= SUPPORT}
    pass2Time = time.perf_counter() - startPass2
    
    file = open("freqpairs_ap.txt", "w")
    for key, value in frequent2.items():
        file.write("%s %s\n" % (key,value))
    file.close() 

    
    file = open("info_ap.txt", "w")
    file.write("Support: %f\n" % (SUPPORT))
    file.write("Pass 1: %f\n" % (pass1Time))
    file.write("Pass 2: %f" % (pass2Time))
    file.close() 
    print("Finished pass with support: %f" % (SUPPORT))
    return pass1Time+pass2Time


"""
Read baskets and count in main memory
the occurrences of each individual item
"""

def frequency(file):
    
    itemList = {}
    
    with open(file) as file:
        reader = csv.reader(file)
        for row in reader:
            for items in row:
                items = items.split()
                
                for item in items:
                    keys = itemList.keys()
                    ## If already in keys add one
                    if item in keys:
                        itemList[item] += 1
                    ## else start it off with one
                    else:
                        itemList[item] = 1
    return itemList


"""
Read baskets again and count in main
memory only those pairs where both elements
are frequent (from Pass 1)
"""

def frequency2(file,pairs):
    pairs = pairs
    with open("retail.dat") as file:
        reader = csv.reader(file)
        
        for row in reader:
            for items in row:
                for key, value in pairs.items():
                    if all(x in items for x in key):
                        pairs[key] += 1
                                  
    return pairs

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

def merge(dict):
    for items in dict:
        for item in items:
            if item in items and items[item] is not None:
                items[item] = 0
    return dict

def sum(dict):
    return functools.reduce(add, map(Counter, dict))

def SON(_file, chunk, supp):
    startPass1 = time.perf_counter()
    length = file_len(_file)
    current = 0
    SUPPORT = length*supp
    
    frequents = []
    data = {}
    i = 0
    ## Count of items
    while(length > current):
        if current+chunk>length:
            chunk = abs(length-current)
        data = frequency_SON(_file, chunk, i)
        frac = length/chunk
        i+=1
        SUPPORT = frac*0.02
        frequent = {k: v for k, v in data.items() if v >= SUPPORT}
        frequents.append(frequent)
        if current+chunk>length:
            current = length+1
        else:
            current += chunk
    
    frequent = merge(frequents)
    frequent = sum(frequent)
    ## Timing
    pass1Time = time.perf_counter() - startPass1
    
    ## Counts
    file = open("counts_SON.txt", "w")
    for key, value in data.items():
        file.write("%s %s\n" % (key,value))
    file.close()

    ## Frequent items
    frequent = {k: v for k, v in frequent.items() if v >= SUPPORT}
    file = open("frequent_SON.txt", "w")
    for key, value in frequent.items():
        file.write("%s %s\n" % (key,value))
    file.close()
    
    ## Candidate Pairs
    pairs = {}
    for pair in itertools.combinations(frequent, 2):
        pairs[pair] = 0
    
    file = open("candidates_SON.txt", "w")
    for key, value in pairs.items():
        file.write("%s %s\n" % (key,value))
    file.close()
    
    startPass2 = time.perf_counter()
    
    ## Count of pairs
    data2 = frequency2_SON(_file, pairs)
   
    ## Frequent pairs
    frequent2 = {k: v for k, v in data2.items() if v >= SUPPORT}
    pass2Time = time.perf_counter() - startPass2
    
    
    file = open("freqpairs_SON.txt", "w")
    for key, value in frequent2.items():
        file.write("%s %s\n" % (key,value))
    file.close() 

    
    file = open("info_SON.txt", "w")
    file.write("Support: %f\n" % (SUPPORT))
    file.write("Pass 1: %f\n" % (pass1Time))
    file.write("Pass 2: %f" % (pass2Time))
    file.close() 
    print("Finished pass with chunk: %f" % (chunk))
    return pass1Time + pass2Time


def frequency_SON(file, chunk,i):
    itemList = {}
    with open(file) as file:
        ## Selects only the chunk size to read
        lines_gen = itertools.islice(file,i*5000,chunk)
        for line in lines_gen:
            items = line.split()
            for item in items:
                keys = itemList.keys()
                ## If already in keys add one
                if item in keys:
                    itemList[item] += 1
                    ## else start it off with one
                else:
                    itemList[item] = 1
    return itemList



def frequency2_SON(file,pairs):
    pairs = pairs
    with open(file) as file:
        reader = csv.reader(file)
        
        for row in reader:
            for items in row:
                for key, value in pairs.items():
                    if all(x in items for x in key):
                        pairs[key] += 1
                                  
    return pairs

def RS(_file, prob, supp):
    startPass1 = time.perf_counter()
    length = file_len(_file)
    SUPPORT = length*0.02*(prob/100)
    data = frequency_RS(_file, prob)
    expected = length*0.02*(prob/100)
    actual = len(data)
    frequent = {k: v for k, v in data.items() if v >= SUPPORT}
    
    ## Timing
    pass1Time = time.perf_counter() - startPass1
    
    ## Counts
    file = open("counts_RS.txt", "w")
    for key, value in data.items():
        file.write("%s %s\n" % (key,value))
    file.close()
    
    ## Frequent items
    frequent = {k: v for k, v in data.items() if v >= SUPPORT}
    file = open("frequent_RS.txt", "w")
    for key, value in frequent.items():
        file.write("%s %s\n" % (key,value))
    file.close()
    
    ## Candidate Pairs
    pairs = {}
    for pair in itertools.combinations(frequent, 2):
        pairs[pair] = 0
    
    file = open("candidates_RS.txt", "w")
    for key, value in pairs.items():
        file.write("%s %s\n" % (key,value))
    file.close()
    
    startPass2 = time.perf_counter()
    
    ## Count of pairs
    data2 = frequency2_RS(_file, pairs)
   
    ## Frequent pairs
    frequent2 = {k: v for k, v in data2.items() if v >= SUPPORT}
    pass2Time = time.perf_counter() - startPass2
    
    
    file = open("freqpairs_RS.txt", "w")
    for key, value in frequent2.items():
        file.write("%s %s\n" % (key,value))
    file.close() 

    
    file = open("info_RS.txt", "w")
    file.write("Expected Support: %f, Actual Support: %f\n" % (expected, actual))
    file.write("Pass 1: %f\n" % (pass1Time))
    file.write("Pass 2: %f" % (pass2Time))
    file.close() 
    print("Finished pass with prob: %f" % (prob))
    return pass1Time+pass2Time


def frequency_RS(_file, prob):
    
    itemList = {}
    
    with open(_file) as file:
        reader = csv.reader(file)
        for row in reader:
            rand = randint(0, 100)
            if rand <= prob:
                for items in row:
                    items = items.split()
                    for item in items:
                        keys = itemList.keys()
                        ## If already in keys add one
                        if item in keys:
                            itemList[item] += 1
                            ## else start it off with one
                        else:
                            itemList[item] = 1
    return itemList



def frequency2_RS(file,pairs):
    pairs = pairs
    with open(file) as file:
        reader = csv.reader(file)
        
        for row in reader:
            for items in row:
                for key, value in pairs.items():
                    if all(x in items for x in key):
                        pairs[key] += 1
                                  
    return pairs

# Hash function for PCY
def hash(n1,n2, buckets):
    return (n1 ^ n2) % buckets

# Generates Bitmap for PCY
def bitmap(table, threshold):
    bitmap = []
    for k,v in table.items():
        if v > threshold:
            bitmap.insert(k,1)
        else:
            bitmap.insert(k,0)
    return bitmap
    
# PCY Function
def pcy(_file, size, supp):
    startPass1 = time.perf_counter()
    ## Count of items
    data = frequency_pcy(_file, size)
    ## Timing
    length = file_len(_file)
    SUPPORT = length*supp
    buckets = {}
    
    pass1Time = time.perf_counter() - startPass1
    ## Counts
    file = open("counts_pcy.txt", "w")
    for key, value in data.items():
        file.write("%s %s\n" % (key,value))
    file.close()
    
    ## Frequent items
    frequent = {k: v for k, v in data.items() if v >= SUPPORT}
            
    file = open("frequent_pcy.txt", "w")
    for key, value in frequent.items():
        file.write("%s %s\n" % (key,value))
    file.close()
    
    ## Pairs
    pairs = {}
    for pair in itertools.combinations(frequent, 2):
        pairs[pair] = 0
    
    ## Bucket creation
    for pair in pairs:
        index = hash(int(pair[0]),int(pair[1]),size)
        if index in buckets:
            buckets[index] += 1
        else:
            buckets[index] = 1
            
    bit_map = bitmap(buckets, SUPPORT)
    ## Removing pairs that dont hash to buckets
    for pair in list(pairs):
        hash_val = hash(int(pair[0]),int(pair[1]),size)
        try:
            if bit_map[hash_val] is not 1:
                pairs.pop(pair)
        except IndexError:
            c = 0

            
            
    file = open("candidates_pcy.txt", "w")
    for key, value in pairs.items():
        file.write("%s %s\n" % (key,value))
    file.close()
    
    startPass2 = time.perf_counter()
    
    ## Count of pairs
    data2 = frequency2_pcy(_file, pairs, size)
   
    ## Frequent pairs
    frequent2 = {k: v for k, v in data2.items() if v >= SUPPORT}
    pass2Time = time.perf_counter() - startPass2
    file = open("freqpairs_pcy.txt", "w")
    for key, value in frequent2.items():
        file.write("%s %s\n" % (key,value))
    file.close() 
    
    file = open("info_pcy.txt", "w")
    file.write("Support: %d\n" % (SUPPORT))
    file.write("Buckets: %d\n" % (size))
    file.write("Pass 1: %f\n" % (pass1Time))
    file.write("Pass 2: %f" % (pass2Time))
    file.close() 
    print("Finished pass with a bucket size of: %f" % (size))
    return pass1Time+pass2Time


"""
Read baskets and count in main memory
the occurrences of each individual item
"""

def frequency_pcy(file,size):
    
    itemList = {}
    
    with open(file) as file:
        reader = csv.reader(file)
        
        for row in reader:
            for items in row:
                items = items.split()
                for item in items:
                    keys = itemList.keys()
                    ## If already in keys add one
                    if item in keys:
                        itemList[item] += 1
                    ## else start it off with one
                    else:
                        itemList[item] = 1
     
    return itemList


"""
Read baskets again and count in main
memory only those pairs where both elements
are frequent (from Pass 1)
"""

def frequency2_pcy(file,pairs,size):
    
    pairs = pairs
    with open(file) as file:
        reader = csv.reader(file)
        
        for row in reader:
            for items in row:
                for key, value in pairs.items():
                    if all(x in items for x in key):
                        pairs[key] += 1
                                  
    return pairs



times = []
times1 = []
times2 = []
times3 = []
supp = []

##times.append(RS("retail.dat", 25,0.01))

times.append(RS("retail.dat", 25,0.02))
times.append(RS("retail.dat", 25,0.03))
times.append(RS("retail.dat", 25,0.04))
times.append(RS("retail.dat", 25,0.05))

##times1.append(pcy("retail.dat", 2000,0.01))
times1.append(pcy("retail.dat", 2000,0.02))
times1.append(pcy("retail.dat", 2000,0.03))
times1.append(pcy("retail.dat", 2000,0.04))
times1.append(pcy("retail.dat", 2000,0.05))

##times2.append(apriori("retail.dat", 0.01))
times2.append(apriori("retail.dat", 0.02))
times2.append(apriori("retail.dat", 0.03))
times2.append(apriori("retail.dat", 0.04))

times2.append(apriori("retail.dat", 0.05))

##times3.append(SON("retail.dat", 3000, 0.01))

times3.append(SON("retail.dat", 3000, 0.02))
times3.append(SON("retail.dat", 3000, 0.03))
times3.append(SON("retail.dat", 3000, 0.04))

times3.append(SON("retail.dat", 3000, 0.05))

times = np.array(times)
times1 = np.array(times1)
times2 = np.array(times2)
times3 = np.array(times3)

##supp.append(0.01)

supp.append(0.02)
supp.append(0.03)
supp.append(0.04)
supp.append(0.05)
supp = np.array(supp)

fig = plt.figure(figsize=(11,8))
ax1 = fig.add_subplot(111)

ax1.plot(times, supp, label='RS', color='c', marker='o')
ax1.plot(times1, supp, label='PCY', color='g', marker='o')
ax1.plot(times2, supp, label='Apriori', color='y', marker='o')
ax1.plot(times3, supp, label='SON', color='k', marker='o')

plt.xticks(times)
plt.xlabel('Times in seconds')
plt.ylabel('Support')
ax1.legend()
plt.savefig('graph.png')



