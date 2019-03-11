# -*- coding: utf-8 -*-
"""
@author: Gavin Gosling
@algorithm: SON 

"""

import time
import csv
import itertools
from collections import Counter
import functools
from operator import add
import matplotlib.pyplot as plt
import numpy as np



"""
The idea is to divide the input file into chunks.
Treat each chunk as a sample, and run the algorithm of Section 6.4.1 on that
chunk. We use ps as the threshold, if each chunk is fraction p of the whole file
,and s is the support threshold. Store on disk all the frequent itemsets found for each
chunk.
"""


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

def SON(_file, chunk):
    startPass1 = time.perf_counter()
    length = file_len(_file)
    current = 0
    SUPPORT = length*0.10
    
    frequents = []
    data = {}
    i = 0
    ## Count of items
    while(length > current):
        if current+chunk>length:
            chunk = abs(length-current)
        data = frequency(_file, chunk, i)
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
    data2 = frequency2(_file, pairs)
   
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


def frequency(file, chunk,i):
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



def frequency2(file,pairs):
    pairs = pairs
    with open(file) as file:
        reader = csv.reader(file)
        
        for row in reader:
            for items in row:
                for key, value in pairs.items():
                    if all(x in items for x in key):
                        pairs[key] += 1
                                  
    return pairs

"""
times = []
chunk = []

times.append(SON("retail.dat", 1000))
times.append(SON("retail.dat", 3000))
times.append(SON("retail.dat", 5000))
times.append(SON("retail.dat", 10000))
times.append(SON("retail.dat", 20000))
chunk.append(1000)
chunk.append(3000)
chunk.append(5000)
chunk.append(10000)
chunk.append(20000)

times = np.array(times)
prob = np.array(chunk)

fig = plt.figure(figsize=(11,8))
ax1 = fig.add_subplot(111)
ax1.plot(times, prob, label='Graph', color='c', marker='o')
plt.xticks(times)
plt.xlabel('Times in seconds')
plt.ylabel('Chunk size')
plt.savefig('son.png')

file = open("SON_tests.txt", "w")
for x in range(0,5):
    file.write("Time: %f Chunk size: %f\n" % (times[x],chunk[x]))
file.close() 
"""