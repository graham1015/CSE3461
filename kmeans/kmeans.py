#Author: Gavin Graham
#PA3
#11/21/2019


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

#read data from databaseFile
def read_data(databaseFile):
    #create tuple of datapoints
    database = ()
    file = open(databaseFile, "r")
    lines = file.readlines()
    #iterate through the lines and create a tuple of attributes for each data point
    for x in lines:
        line = tuple(float(y) for y in x.split())
        database.append(line)
    #close file and return database of 2d tuples
    file.close()
    return database


#given 2 lists the euchlidean distance base on the attributes
def findDist(array1, array2):
     sum = 0
     #sum the attributes and find the square root
     for x in range(0, len(array1)):
         sum = sum + ((array1[x] - array2[x])**2)
     return math.sqrt(sum)


#generate kmeans
def genKmeans (database, k, n, e, outFile):
    #randomly initiate k centroids and store in 
    centroids = []
    for x in range(0, k):
        centroids[x] = database[random.randint(0, len(database))]

    #repeat until the new and old cluster centroids are e-difference n iterations
    #initialize variables for clusters and old centroids
    i=0
    oldCentroids = [[None]] * k
    clusters = [[None]] * k
    while ((findDist(oldCentroids, centroids) >e) and (i<n)):
        #update olds centroids
        oldCentroids = centroids.copy()
        #increment iteration number
        i = i+1
        #assign each data point to each of the k clusters based on Euclidean distance to centroids
        for x in range(0, len(database)):
            #initialize the current centroid and min distance
            currentCent = 0
            minDist = findDist(centroids[0], database[x])
            #iterate through centroids and find distance
            for y in range (0, len(centroids)):
                dist = findDist(centroids[y], database[x])
                #if distance to this centroid is the min then update current centroid and min dist
                if dist < minDist:
                    minDist = dist
                    currentCent = y
            #append the point to the lowest distance cluster
            clusters[y].append(x)

        #update cluster centroids
        #iterate through clusters
        for j in range(0, len(clusters)):
            #create a list of attributes of the points that is the sum of each attribute
            sum = []
            #for each point in the cluster
            for m in clusters[j]:
                #for each attribute in the associated data point
                for n in range(0, len(database[m])):
                    #add the current attribute value to the sum of that attribute
                    sum[n] = sum[n] + database[m][n]
            #for each final sum of attributes, divide by the number of points in the cluster to find the average
            for r in range (0, len(sum)):
                sum[r] = sum[r]/len(j)
            #update centroid for each cluster
            centroids.clear()
            centroids[j] = sum

  #output k clusters
    #open file to write
    out = open(outFile, "w+")
    #print the points for each cluster
    for p in range(0, k):
        out.print(p +": " +clusters[p])
    return
  

#run the program
database = read_data(databaseFile)
genKmeans(database, k, n, e, outFile)
