# -*- coding: utf-8 -*-
"""
@author: Gavin Gosling
@algorithm: PCY algorithm

"""

"""
Pass 1 of PCY: In addition to item counts,
maintain a hash table with as many
buckets as fit in memory
"""

import time
import csv
import itertools
import matplotlib.pyplot as plt
import numpy as np

# Returns file length
def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

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


pcy("netflix.data", 2000,0.05)
"""
#Support
times = []
supp = []

times.append(pcy("retail.dat", 2000,0.01))
times.append(pcy("retail.dat", 2000,0.02))
times.append(pcy("retail.dat", 2000,0.03))
times.append(pcy("retail.dat", 2000,0.04))
times.append(pcy("retail.dat", 2000,0.05))
##supp.append(0.01)
##supp.append(0.02)
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
plt.savefig('pcy_supp.png')

'''
#Buckets
'''
times = []
buck = []

times.append(pcy("retail.dat", 1000))
times.append(pcy("retail.dat", 2000))
times.append(pcy("retail.dat", 3000))
times.append(pcy("retail.dat", 5000))
times.append(pcy("retail.dat", 10000))
buck.append(1000)
buck.append(2000)
buck.append(3000)
buck.append(5000)
buck.append(10000)

times = np.array(times)
buck = np.array(buck)

fig = plt.figure(figsize=(11,8))
ax1 = fig.add_subplot(111)
ax1.plot(times, buck, label='Graph', color='c', marker='o')
plt.xticks(times)
plt.xlabel('Times in seconds')
plt.ylabel('Buckets')
plt.savefig('pcy_buck.png')

file = open("pcy_tests.txt", "w")
for x in range(0,5):
    file.write("Time: %f Buckets: %f\n" % (times[x],buck[x]))
file.close() 
"""