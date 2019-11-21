#Author: Gavin Graham

#Import required libraries
import argparse
import itertools
import numpy as np

#Initialize argument parser
parser = argparse.ArgumentParser()


#Add arguments to parser
parser.add_argument('-database_file')
parser.add_argument('-minsupp')
parser.add_argument('-output_file')


#Parse Arguments
args = parser.parse_args()


#Set variables for each of the parsed arguments
databaseFile = str(args.database_file)
alpha = int(args.minsupp)
out = str(args.output_file)



#function to read database
def read_database(databaseFile):
    #open database file
    file = open(databaseFile, "r")
    #read and set variables n and m
    first = (int(x) for x in file.readline().split())

    n = first[0]
    m = first[1]
    #create 2d array for database
    i=0
    database = []
    database[0] = [n, m]
    #iterate through file to fill database
    for i in range(1, n):
        itemset = (int(x) for x in file.readline().split())
        itemset = np.asarray(itemset)
        database[i] = itemset
    #close file and return databse
    file.close()
    return database




#generate F1
def generate_F1 (database, n, alpha):
    #create dictionary for inputs and counts
    F1 = {}
    #iterate through itemsets in database
    for i in range(1, n):
        #iterate through items in sets
        for j in range(0, len(database[i])):
            num = database[i][j]
            #input values into dictionary and increment count if already exist
            if num in F1:
                F1[num] = F1[num] + 1
            else:
                F1[num] = 1
    #determine if each dictionary entry is frequent
    for x in F1:
        if F1[x] < alpha:
            #pop if infrequent
            F1.pop(x)
    return F1





#Generate Lk+1 from Fk
def generate_candidate(Fk, k):
    #create set of all values in Fk
    lk = {}
    for x in Fk:
        lk.add(x)
    Lk ={}
    #add all possible unions of sets in Fk to Lk
    for j in lk:
        for r in lk:
            Lk.add(j.union(r))
    #remove sets from Lk if not equal to k
    for l in Lk:
        if len(l) != k+1:
            Lk.remove(l)
    return Lk





# Prune candidate itemsets in Lk+1 containing
# subsets of length k that are infrequent
def prune_candidate(Lk, Fk, k):
    #create set of values in Fk
    fk = {}
    for x in Fk:
        fk.add(x)
        #for each set in Lk
    for j in Lk:
        #find all subsets
        lk = set(itertools.combinations(j, k))
        #determine if any subsets exist from set in lk but not in fk
        toPrune = lk.difference_update(fk)
        #if any subsets exist then prune the set in Lk
        if len(toPrune) >0:
            Lk.remove(j)
    return Lk





# Count the support of each candidate in Lk+1 by scanning the DB
def count_support(Lk, database, n):
    #create dictionary for Fk
    Fk = {}
    #for each set in LK
    for x in Lk:
        #iterate through each itemset in the database
        for i in range(1, n):
            flag = 0
            #check that each item in the set(x) is found in the given itemset(i) of the database
            for y in x:
                for j in range(0, len(database[i])):
                    if database[i][j] ==  y:
                        flag = flag+1
            #if all items in the set exist in the itemset of the database
            if flag == len(x):
                #Increment the count of the set in the dictionary Fk
                if x in Fk:
                    Fk[x] = Fk[x]+1
                else:
                    Fk[x] = 1
    return Fk





# Eliminate candidates in Lk+1 that are infrequent, leaving only those that are frequent=> Fk+1
def eliminate_candidate(Fk, alpha):
    #iterate through Fk to see that all entries are >= alpha
    for x in Fk:
        if Fk[x] < alpha:
            Fk.pop(x)
    return Fk





def output_itemsets(Fk, out):
    file=open(out, "w")
    for x in Fk:
        file.write(x +"\n")
    return





def apriori(database , alpha , out) :

    k=1
    n = database[0][0]
    m = database[0][1]

    #generate F1 = {frequent 1-itemsets}
    Fk = generate_F1(database, n, alpha)

    while len(Fk) > 0:

        # output F1 , F2 , . . . , Fk to output
        output_itemsets(Fk, out)

        #Generate Lk+1 from Fk
        Lk = generate_candidate(Fk, k)

        # Prune candidate itemsets in Lk+1 containing
        # subsets of length k that are infrequent
        Lk = prune_candidate(Lk, Fk, k)

        # Count the support of each candidate in Lk+1 by scanning the DB
        Fk = count_support(Lk, database, n)

        #Eliminate candidates in Lk+1 that are infrequent, leaving only those that are frequent=> Fk+1
        eliminate_candidate(Fk, alpha)

        k= k+1

    return

database = read_database(databaseFile)
apriori(database, alpha, out)
