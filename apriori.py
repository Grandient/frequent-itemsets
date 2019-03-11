# -*- coding: utf-8 -*-
"""

@author: Gavin Gosling
@algorithm: Apriori Algorithm

"""
import time
import csv
import itertools
import matplotlib.pyplot as plt
import numpy as np

## Function finds length of the file
def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

## Function applys to apriori algorithm to file with support
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

"""
times = []
supp = []

times.append(apriori("retail.dat", 0.01))
times.append(apriori("retail.dat", 0.02))
times.append(apriori("retail.dat", 0.03))
times.append(apriori("retail.dat", 0.04))
times.append(apriori("retail.dat", 0.05))
supp.append(0.01)
supp.append(0.02)
supp.append(0.03)
supp.append(0.04)
supp.append(0.05)

times = np.array(times)
supp = np.array(supp)

fig = plt.figure(figsize=(11,8))
ax1 = fig.add_subplot(111)
ax1.plot(times, supp, label='Graph', color='c', marker='o')
plt.xticks(times)
plt.xlabel('Times in seconds')
plt.ylabel('Support')
plt.savefig('apriori.png')

file = open("apriori_tests.txt", "w")
for x in range(0,2):
    file.write("Time: %f Support: %f\n" % (times[x],supp[x]))
file.close() 
"""