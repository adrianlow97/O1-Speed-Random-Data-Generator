from AliasMethod import VoseAlias
import os, random, re, sys, time, csv

def main():
#get the number of data sets needed to be generated
    numInputs = int(input("Please enter the number of data sets to generate: "))
#initialize empty arrays to store the generated data
    labelArray = []
    dataArray =[]
#get the labels for each data set
    for x in range(numInputs):
        label = input("Please enter a label for input " + str(x+1) + ": ")
        labelArray.append(label)
#generate random data for each data set
    for x in range(numInputs):
        print("Would you like to enter the data for "+labelArray[x]+" manually or enter a file?\n")
        choice = int(input("Enter 1 for MANUALMODE or enter 2 for FILEMODE: "))
        if choice == 1:
            temparray = manualMode()
            dataArray.append(temparray)
        else:
            file = input("Enter the name of the data file: ")
            temparray = fileMode(file)
            dataArray.append(temparray)

#write the randomly generated data with its corresponding label to a file
    finalArray = []
    for x in range(len(dataArray[0])):
        appendStr = ""
        for y in range(numInputs):
            appendStr += (labelArray[y] +": " + dataArray[x][y] + "\t\t")
        finalArray.append(appendStr)
    with open("outputs.csv", "w") as myFile:
        for item in finalArray:
            myFile.write(item)

def manualMode():
    dist = {}
    count = int(input("Please input number of different values: "))
    for i in range(count):
        dist[input("\nPlease input new value: ")] = float(input("\nPlease enter count/weight for this value: "))
    num = input("\nNow please input number of random values to generate: ")
    return VoseAlias(dist, num).return_list

def fileMode(filename):
    file = open(filename, "r")
    reader = csv.reader(file)
    dist = {}
    for line in reader:
        dist[line[1]] = float(line[2])
    return VoseAlias(dist, num).return_list

if __name__ == "__main__":
    main()
