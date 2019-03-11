# frequent-itemsets
A Python implementation of the Apriori algorithm. Works with Python 3.6 and 3.7.

The apriori algorithm uncovers hidden structures in categorical data. The classical example is a database containing purchases from a supermarket. Every purchase has a number of items associated with it. We would like to uncover association rules such as {bread, eggs} -> {bacon} from the data. This is the goal of association rule learning, and the Apriori algorithm is arguably the most famous algorithm for this problem. This repository contains an efficient, well-tested implementation of the apriori algorithm as descriped in the original paper by Agrawal et al, published in 1994.

This repository contains five python scripts.<br/>

It uses the retail dataset from: (http://fimi.ua.ac.be/data/retail.dat)<br/>
The dependencies for these scripts is matplotlib and numpy.<br/>
Each implementation runs the algorithm and graphs it after.<br/>

The first is apriori.py. This is an implementation of the apriori algortihm.<br/>
The second is pcy.py. This is an implementation of the PCY algorithm.<br/>
The third is SON.py. This is an implementation of the SON algorithm.<br/>
The fourth is RS.py. This is an implementation of the Random Sampling version of Apriori.<br/>
The fifth is graph.py. Which just runs all the implementations and graphs them on a single chart.<br/>
