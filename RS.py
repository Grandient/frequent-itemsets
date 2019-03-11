# -*- coding: utf-8 -*-
"""

@author: Gavin Gosling
@algorithm: Random Sampling 

"""
from random import randint
import time
import csv
import itertools
import matplotlib.pyplot as plt
import numpy as np

"""
Instead of using the entire file of baskets, we could pick a random subset of
the baskets and pretend it is the entire dataset. We must adjust the support
threshold to reflect the smaller number of baskets. For instance, if the support
threshold for the full dataset is s, and we choose a sample of 1% of the baskets,
then we should examine the sample for itemsets that appear in at least s/100
of the baskets.

The safest way to pick the sample is to read the entire dataset, and for each
basket, select that basket for the sample with some fixed probability p. Suppose
there are m baskets in the entire file. At the end, we shall have a sample whose
size is very close to pm baskets. 

"""
def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

def RS(_file, prob):
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
    file.write("Expected Size: %f, Actual Size: %f\n" % (expected, actual))
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


"""
times = []
prob = []

times.append(RS("retail.dat", 10))
times.append(RS("retail.dat", 20))
times.append(RS("retail.dat", 25))
times.append(RS("retail.dat", 33))
times.append(RS("retail.dat", 50))
prob.append(0.10)
prob.append(0.20)
prob.append(0.25)
prob.append(0.33)
prob.append(0.50)

times = np.array(times)
prob = np.array(prob)

fig = plt.figure(figsize=(11,8))
ax1 = fig.add_subplot(111)
ax1.plot(times, prob, label='Graph', color='c', marker='o')
plt.xticks(times)
plt.xlabel('Times in seconds')
plt.ylabel('Probability')
plt.savefig('rs.png')

file = open("RS_tests.txt", "w")
for x in range(0,5):
    file.write("Time: %f Prob: %f\n" % (times[x],prob[x]))
file.close() 
"""