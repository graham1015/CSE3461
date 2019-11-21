#Author: Gavin Graham

#Import required libraries
import argparse
import math
import random

#Initialize argument parser
parser = argparse.ArgumentParser()


#Add arguments to parser
parser.add_argument('-database_file')
parser.add_argument('-k')
parser.add_argument('-max_iters')
parser.add_argument('-eps')
parser.add_argument('-output_file')


#Parse Arguments
args = parser.parse_args()


#Set variables for each of the parsed arguments
databaseFile = str(args.database_file)
k = int(args.k)
n = int(args.max_iters)
e = float(args.eps)
outFile = str(args.output_file)

def read_data(databaseFile):
    database = ()
    file = open(databaseFile, "r")
    lines = file.readlines()
    for x in lines:
        line = tuple(int(y) for y in x.split())
        database.append(line)
    file.close()
    return database

def findDist(array1, array2):
     sum = 0
     for x in range(0, len(array1)):
         sum = sum + ((array1[x] - array2[x])**2)
     return math.sqrt(sum)

def genKmeans (database, k, n, e, outFile):

    #randomly initiate k centroids
    centroids = []
    for x in range(0, k):
        centroids[x] = database[random.randint(0, len(database))]

    #repeat until the new and old cluster centroids are e-difference n iterations
    i=0
    oldCentroids = [[None]] * k
    clusters = [[None]] * k
    while ((centroids != oldCentroids) and (i<e)):
        oldCentroids = centroids.copy()
        i = i+1
        #assign each data point to each of the k clusters based on Euclidean distance
        for x in range(0, len(database)):
            currentCent = 0
            minDist = findDist(centroids[0], database[x])
            for y in range (0, len(centroids)):
                dist = findDist(centroids[y], database[x])
                if dist < minDist:
                    minDist = dist
                    currentCent = y
            clusters[y].append(x)

        #update cluster centroids
        for j in range(0, len(clusters)):
            sum = []
            for m in clusters[j]:
                for n in range(0, len(database[m])):
                    sum[n] = sum[n] + database[m][n]
            for r in range (0, len(sum)):
                sum[r] = sum[r]/len(j)
            centroids.clear()
            centroids[j] = sum

  #output k clusters
    out = open(outFile, "w+")
    for p in range(0, k):
        out.print(p +": " +clusters[p])

    return
  


database = read_data(databaseFile)
genKmeans(database, k, n, e, outFile)
