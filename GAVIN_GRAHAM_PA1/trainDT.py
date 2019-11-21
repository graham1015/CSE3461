#Author:Gavin Graham

#Import required libraries
import argparse
import numpy as np

#Initialize argument parser
parser = argparse.ArgumentParser()

#Add arguments to parser
parser.add_argument('-train_data')
parser.add_argument('-train_label')
parser.add_argument('-test_data')
parser.add_argument('-nlevels')
parser.add_argument('-pthrd')
parser.add_argument('-impurity')
parser.add_argument('-pred_file')

#Parse Arguments
args = parser.parse_args()

#Set variables for each of the parsed arguments
train_file = str(args.train_data)
label_file = str(args.train_label)
test_file = str(args.test_data)
nl = int(args.nlevels)
p = int(args.pthrd)
impurity_method = str(args.impurity)
out_file = str(args.pred_file)


#Create NumPy for the test set, the training set, and the labels
train = np.genfromtxt(train_file, delimiter=' ')
test = np.genfromtxt(test_file, delimiter=' ')
label = np.genfromtxt(label_file, delimiter=' ')
#set variables n and m for sizes and reshape train and test data
n = label.size
m = (train.size)/n
np.reshape(train, (n, m))
np.reshape(test, (n, m))



#Create a structure for the Nodes
class Node(object):

    #Initialize the node
    def __init__(self, val, impurity_method, lev):
        #Create all required attributes for a node
        self.data_idx = val
        self.left_child = None
        self.right_child = None
        self.impurity_method = impurity_method
        self.dfeature = None
        self.nlevels = lev
        self.impurity = None
        self.mfeatures = m
        self.Class = None


    #Build a Decision Tree
    def buildDT(self, data, label, impurity_method, nl, p):
        data_idx = data[]

        #Create a node at level 0
        dt = Node(data_idx, impurity_method, 0)
        #Split the tree
        dt.splitNode(nl, p)
        return dt


    #Split the tree
    def splitNode(self, nl, p):
        #if node is at lower than max level and impurity is less than the max
        if self.nlevels < nl and self.impurity > p:
            #initialize the max gain and splitFeature variables
            maxGain = -1
            splitFeature = -1

            #For all features from 0 to m
            for feature_i in range(0, self.mfeatures):
                Pleft = calculateIP()
                Pright = calculateIP()

                #calculate the impurity after split and find gain
                M=
                Gain = self.impurity - M

                #if gain  is greater than gainMax then set new gain max
                if Gain > maxGain:
                    maxGain = Gain
                    splitFeature = feature_i

            #set new dfeature
            self.dfeature = splitFeature

            #Find index of left and right children
            data_idx_left =
            data_idx_right =

            #Create left and right children
            self.left_child = Node(data_idx_left, impurity_method, self.nlevels +1)
            self.right_child = Node(data_idx_right, impurity_method, self.nlevels + 1)

            #Recursively split each child
            self.left_child.splitNode(nl, p)
            self.left_child.splitNode(nl, p)
        return

    # calculate P based on the impurity method
    def calculateIP(data_idx):
        #calculate if impurity method is gini
        if impurity_method is "gini":
            P = calculateGINI(data_idx)

        #calculate if impurity method is entropy
        elif impurity_method is "entropy":
            P = calculateEntropy(data_idx)

        #return probability
        return P


main():
#for each data point
for point in range(0, n):
    #set class attribute
    Class = label[point]
    #create root and build tree
    root = Node(train[point], impurity_method, 0)
    root.buildDT(0, Class, impurity_method, nl, p)
    
