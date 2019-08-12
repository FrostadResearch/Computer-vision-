import cv2
import glob
import csv
import numpy as np
import math
import pickle
import OutLine as op


def get_size_data_e(e):
    (x, y) = e[0][0]
    (MA, ma) = e[0][1]
    angle = e[0][2]
    A = math.pi * MA * ma
    return A



def process():
    
    """
Takes in an image name, runs pick cell, then finds size of cells
and globifier. Returns list of lists of time and cell size  
    """
    #op.globifier(img)
    pickle_in = open("list.pickle", "rb")
    ctrs = pickle.load(pickle_in)
    pickle_in_t = open("time.pickle", "rb")
    time = pickle.load(pickle_in_t)
    print(ctrs)
    output= []
    i=0
    while i < len(ctrs):
        j = 0
        if len(ctrs[i])==0:
            print("empty")
        else:
            row = [time[i]]
            while j <len(ctrs[i]):
                row.append(get_size_data_e(ctrs[i][j]))
                j= j+1
            output.append(row)
        i= i+1 

    return output


def make_csv(lolocd):
    """
take in a list of lists and writes the time and data value in a csv
    """
    with open('cell Data file', 'w') as csvfile:
        wr = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        wr.writerow(["time", "cells"])
        for locd in lolocd:
            wr.writerow(locd)
        return csv



make_csv(process())
    
