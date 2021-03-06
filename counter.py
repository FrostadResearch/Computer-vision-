import cv2
import glob
import csv
import numpy as np
import cProfile
import re

##def process(i):
##    
##    #import image
##    img = cv2.imread(i)
##
##    #modify image 
##    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
##
##    im, thresh = cv2.threshold(gray, 160, 255, cv2.THRESH_BINARY_INV)
##
##    #blur to make contour detection easier
##    thresh = cv2.GaussianBlur(thresh, (9,9), 0)
##    cv2.namedWindow('img', cv2.WINDOW_NORMAL)
##    cv2.resizeWindow('img', 1000, 750)
##
##    #find contours
##    ctrs, im = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
##    cv2.drawContours(img, ctrs, -1, (0,255,0),2)
##    cv2.imshow("img", img)
##    return ctrs

def process(i):
    
    #import image
    img = cv2.imread(i)

    #modify image 
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    gray_blur = cv2.GaussianBlur(gray, (15, 15), 0)

    thresh = cv2.adaptiveThreshold(gray_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 1)

    kernel = np.ones((5,5), np.uint8)
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    
    kernel = np.ones((10,10), np.uint8)
    close = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)

    cont_img = close.copy()
    contours, hierarchy = cv2.findContours(cont_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area < 200 or area > 40000:
            continue
        if len(cnt) < 5:
            continue
        ellipse = cv2.fitEllipse(cnt)
        cv2.drawContours(img, [cnt], 0, (0,255,0),2)
        #cv2.ellipse(img, ellipse, (0,255,0), 2)
    
    cv2.namedWindow('img', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('img', 1000, 750)

 
    cv2.imshow("img", img)
    return contours


def process_small(i, x, y):
    
    #import image
    imgUncut = cv2.imread(i)
    #img = imgUncut[0:1000, 0:1000]
    img = imgUncut[y-500:y+500, x-500:x+500]

    #modify image 
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    gray_blur = cv2.GaussianBlur(gray, (15, 15), 0)

    thresh = cv2.adaptiveThreshold(gray_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 1)

    kernel = np.ones((5,5), np.uint8)
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    
    kernel = np.ones((10,10), np.uint8)
    close = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)

    cont_img = close.copy()
    contours, hierarchy = cv2.findContours(cont_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area < 200 or area > 40000:
            continue
        if len(cnt) < 5:
            continue
        ellipse = cv2.fitEllipse(cnt)
        cv2.drawContours(img, [cnt], 0, (0,255,0),2)
        #cv2.ellipse(img, ellipse, (0,255,0), 2)
    
    cv2.namedWindow('img', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('img', 1000, 750)

 
    cv2.imshow("img", img)
    return contours

def good_cont(c):
    return cv2.contourArea(c)>1000 and cv2.contourArea(c)<10000

def pick_cells(i):
    ctrs = process(i)
    img = cv2.imread(i)

    cv2.namedWindow('img', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('img', 1000, 750)

    #find contours
    #cv2.drawContours(img, ctrs, -1, (0,255,0),2)
    #cv2.imshow("img", img)


    #iterate over list of contours to only draw and count valid contours 
    i=0
    #cellCount = 0
    while (i< len(ctrs)):
        if (good_cont(ctrs[i])):
            print(i)

            #draw and count valid contours
            cv2.drawContours(img, ctrs, i, (0,255,0),2)  
            #cellCount= cellCount + 1        

            # label contour on image 
            extRight = tuple(ctrs[i][ctrs[i][:, :, 0].argmax()][0])
            cv2.circle(img, extRight, 8, (255, 0, 0), -1)
            cv2.putText(img,str(i), extRight,
                        cv2.FONT_HERSHEY_TRIPLEX, 2, 255,4)
        
        i= i + 1
        
    print("choose a cell to track:")
    
    cv2.namedWindow('img', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('img', 1000, 750)
    cv2.imshow("img", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    cell_str = input()
    cell = int(cell_str)
    print("thanks!")

    #check to make sure the correct contour is being picked 
    cv2.drawContours(img, ctrs, cell, (0,0,255),2)
    cv2.namedWindow('img', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('img', 1000, 750)
    #test get centre functions 
    x = get_centre_val(ctrs[cell],"x")
    y = get_centre_val(ctrs[cell],"y")
    cv2.putText(img,"the point", (x,y),
                        cv2.FONT_HERSHEY_TRIPLEX, 2, (0,0,255),4)
    cv2.imshow("img", img)
    
    return ctrs[cell]
   
    
def get_data(c):
    return cv2.contourArea(c)

def get_centre(c):
    x, y, w, h = cv2.boundingRect(c)
    cx = x
    cy = y
    return [cx,cy]

def get_centre_val(c,xy):
    x, y, w, h = cv2.boundingRect(c)
    cx = x
    cy = y
    if xy == "x":
        return int(cx)
    else:
        return int(cy)
    

def good_cell(i, c):
    diff = 10
    iCell = get_centre(i)
    cCell = get_centre(i)
    x = abs(iCell[0] - cCell[0])
    y = abs(iCell[1] - cCell[1])
    return x < diff and y < diff

def make_file(locd):
    with open('cell Data file', 'w') as csvfile:
        wr = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        wr.writerow(locd)
        # I realize that this adds this all in one row

def reasonable(c, e):
    return get_data(c) > get_data(e) - 50 #and get_data(c) < get_data(e) + 100 


def main(img):

    init = pick_cells(img)
    time = []
    files = glob.glob('2019-03-01_20;0*.jpg')
    nfiles = len(files)

    last = init
    cellY = get_centre_val(init, "y")
    cellX = get_centre_val(init, "x")
    cellData = np.zeros((1,nfiles))
    i = 0
    time =[]
    for file in files:
       ctrs = process_small(file, cellX,cellY)
       for c in ctrs:
           if good_cell(last,c): #and reasonable(c,last):
               print(get_data(c))
               #print(i)
               cellData[0,i]= get_data(c)
               last = c
               time =  0.2*i
       i += 1
    make_file(cellData)
       
    cv2.destroyAllWindows()

    return csv

main("2019-03-01_20;01_1551499548124ms.jpg")
        
def profile():
    cProfile.run('main("2019-03-01_20;01_1551499548124ms.jpg")')
