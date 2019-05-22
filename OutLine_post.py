import cv2
import glob
import csv
import numpy as np
import cProfile
import math
import imageio
import OutLine_pre as op
import pickle
import matplotlib.pyplot as plt



def size(img):
    """
Takes in an image name, runs pick cell, then finds size of cells
and globifier. Returns list of lists of time and cell size  
    """
    #op.globifier(img)
    pickle_in = open("list.pickle", "rb")
    ctrs = pickle.load(pickle_in)
    output= []
    for ctr in ctrs:
        row = [ctr[0], op.get_size_data(ctr[1])]
        output.append(row)
    return output

def newSize(img):
    """
Takes in an image name, runs pick cell, then finds size of cells
and globifier. Returns list of lists of time and cell size  
    """
    op.globifier(img)
    pickle_in = open("list.pickle", "rb")
    ctrs = pickle.load(pickle_in)
    output= []
    for ctr in ctrs:
        row = [ctr[0], op.get_size_data(ctr[1])]
        output.append(row)
    return output


def make_csv(lolocd):
    """
take in a list of lists and writes the time and data value in a csv
    """
    with open('cell Data file', 'w') as csvfile:
        wr = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        wr.writerow(["time", "cell size"])
        for locd in lolocd:
            wr.writerow(locd)
        return csv

def final(img, fnc):
    """
takes in an image name and a string of the type of operation requested,
runs that function and returns the output
    """
    make_csv(fnc(img))

def visualize(img,fnc):
    data= fnc(img)
    startTime = data[0][0]
    x =[]
    y =[]
    for locd in data:
        x.append(locd[0] - startTime)
        y.append(locd[1])
    plt.plot(x,y)
    plt.xlabel("Time (ms)")
    plt.ylabel("Cell size (px)")
    plt.title("Cell size vs Time")
    plt.show() 
    
    
    
#op.globifier("2019-03-01_20;01_1551499548124ms.jpg")
 
#final("2019-03-01_20;01_1551499548124ms.jpg",size)
visualize("2019-03-01_20;01_1551499548124ms.jpg",newSize)
