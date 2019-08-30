import os, random, re, sys, time, csv
from decimal import *
from optparse import OptionParser
import matplotlib.pyplot as plt
import json


class VoseAlias(object):
    """ A probability distribution for discrete weighted random variables and its probability/alias
    tables for efficient sampling via Vose's Alias Method 
    """
	
    start_time = time.time()
    init_time = 0
    generation_time = 0
    generation_and_print_time = 0
    total_time = 0
    vals = []

######################################################################################################

    def __init__(self, dist, size):
        """ (VoseAlias, dict) -> NoneType """
        sum_of_inputs = 0
        dist = self.calc_probs(dist)
        for i in dist.keys():
            sum_of_inputs = sum_of_inputs + dist[i]
            if dist[i] < 0:
                print("Error, no non-negative values.")
                return
        if abs(1 - sum_of_inputs) > 0.05:
            print("Probabilities must add up to one.")
            return
        self.dist = dist
        self.alias_initialisation()
        self.init_time = time.time() - self.start_time
        self.sample_n(size)
		
########################################################################################################		
		
    def calc_probs(self, dist):
        """scales probabilities"""
        totalCount = 0
        probs = dist
        for i in dist.keys():
            totalCount = totalCount + dist[i]
        for i in dist.keys():
            probs[i] = (dist[i]/totalCount)
        return probs		
		
########################################################################################################		
		
    def alias_initialisation(self):
        """ Construct probability and alias tables for the distribution. """
        # Initialize variables
        n = len(self.dist)
        self.table_prob = {}   # probability table
        self.table_alias = {}  # alias table
        scaled_prob = {}       # scaled probabilities
        small = []             # stack for probabilities smaller that 1
        large = []             # stack for probabilities greater than or equal to 1

        # Construct and sort the scaled probabilities into their appropriate stacks
        for o, p in self.dist.items():
            scaled_prob[o] = Decimal(p) * n	#make new list of scaled probabilities (prob times n)

            if scaled_prob[o] < 1:	#put scaled values into new lists based on size
                small.append(o)	#values less than 1
            else:
                large.append(o)	#values greater than 1

        # Construct the probability and alias tables
        while small and large:	#while both lists are not empty
            s = small.pop()	#s is scaled probability less than 1
            L = large.pop()	#l is scaled probability greater than 1

            self.table_prob[s] = scaled_prob[s]	#put s in list of probabilities
            self.table_alias[s] = L	#put L in list of aliases corresponding to s

            scaled_prob[L] = (scaled_prob[L] + scaled_prob[s]) - Decimal(1)	#add s to L and subtract 1 to get new L (represents 1-s being taken from L)

            if scaled_prob[L] < 1:	#add new L to appropriate
                small.append(L)	#new L is less than 1
            else:
                large.append(L)	#new L is still greater than 1

        # The remaining outcomes (of one stack) must have probability 1
        while large:	#small list is now empty but large list is not
            self.table_prob[large.pop()] = Decimal(1)	#round whatever values are left to 1

        while small:
            self.table_prob[small.pop()] = Decimal(1)	#round whatever values are left to 1

###################################################################################################
			
    def alias_generation(self):
        """ Return a random outcome from the distribution. """
        # Determine which column of table_prob to inspect
        col = random.choice(list(self.table_prob))

        # Determine which outcome to pick in that column
        if self.table_prob[col] >= random.uniform(0,1):
            return col
        else:
            return self.table_alias[col]
			
######################################################################################################

    def sample_n(self, size):
        """ Retrun a sample of size n from the distribution, and print the results to stdout. """
        # Ensure a non-negative integer as been specified
        n = int(size)
        try:
            if n <= 0:
                raise ValueError("Please enter a non-negative integer for the number of samples desired: %d" % n)
        except ValueError as ve:
            sys.exit("\nError: %s" % ve)

        vals = []	#initialize empty list of values
        for i in range(n):	#loop through n times
            vals.append(self.alias_generation())	#get one alias_generation value (O(1)) and append (O(1)) it to vals
        self.generation_time = time.time() - self.init_time
        #print(vals)	#print the entire list
        #self.count_data(self.dist, vals) #function to print data nicely
        #self.print_raw(vals)
        self.generation_and_print_time = time.time() - self.generation_time
        self.total_time = time.time() - self.start_time
        self.print_times()
        #self.make_histogram(vals, n)	#make a histogram of results
        self.vals = vals

####################################################################################################		

    def make_histogram(self, values, size):
        """ Prints off a histogram of the values created in alias_generation """
        plt.hist(values, bins = "auto")	#values are the data being counted
        plt.title("Occurrences of Randomly Generated Values")	#title of histogram
        plt.xlabel("Value")	#x-axis label
        plt.ylabel("Count")	#y-axis label
        self.total_time = time.time() - self.start_time
        plt.show()	#print window of histogram

########################################################################################################

    def print_times(self):
        """This method just prints off the times taken for each part"""
        print("\nTotal time: %s seconds" %self.total_time)

########################################################################################################

    def count_data(self, dist, vals):
        """Makes the data nicer and easier to read"""
        with open("outputs.csv", "w") as myFile:
            for x in dist:
                varCount = vals.count(x)
                print("Count of " + x + ": " + str(varCount)) #print the count
                percent = str(100 * (varCount / len(vals)))
                print("Percent: " + str(100*(varCount / len(vals))) + "%") #print the percent
                myFile.write(str(x) + "," + str(varCount) + "," + percent + "\n")
		
####################################################################################
		
    def print_raw(self, vals):
        """Prints all values to csv"""
        with open("outputs.csv", "w") as myFile:
            for word in vals:
                myFile.write("%s\n" %word)

###########################################################################################
				
    def print_json(self, vals):
        """Prints json"""
        print(json.dumps(vals))
		
####################################################################################
		
		
    def return_list(self):
        """Returns list of vals for json"""
        return self.vals

#######################################################################################################
#######################################################################################################
#######################################################################################################
num = 100000
'''
if len(sys.argv) == 2:		
    file = open(sys.argv[1], "r")
    reader = csv.reader(file)
    dist = {}
    for line in reader:
        dist[line[1]] = float(line[2])
    vals = VoseAlias(dist, num)
    new_vals = vals.return_list()
    with open("outputs.csv", "w") as myFile:
        for item in new_vals:
            myFile.write(item + "\n")
elif len(sys.argv) == 3:
    #first data type (names)
    file = open(sys.argv[1], "r")
    reader = csv.reader(file)
    dist = {}
    for line in reader:
        dist[line[1]] = float(line[2])
    vals = VoseAlias(dist, num)
    vals1 = vals.return_list()
    file.close()
    #get list of second data type (ages)
    file2 = open(sys.argv[2], "r")
    reader = csv.reader(file2)
    dist2 = {}
    for line in reader:
        dist2[line[1]] = float(line[2])
    new_vals = VoseAlias(dist2, num)
    vals2 = new_vals.return_list()
    ssn = 100000000
    #now create list with all data pieces
    new_dist = []
    for x in range(len((vals1))):
        new_dist.append("Name: " + vals1[x] + "\t\tAge: " + vals2[x] + "\t\tSSN: " + str(ssn) + "\n")
        ssn = ssn + 1
    with open("outputs.csv", "w") as myFile:
            for item in new_dist:
                myFile.write(item)
else:
    dist = {}
    count = int(input("Please input number of values you have: "))
    for i in range(count):
        dist[input("\nPlease input new value: ")] = float(input("\nPlease enter count for this value: "))
    num = input("\nNow please input number of random values you want: ")
    VoseAlias(dist, num)
'''
