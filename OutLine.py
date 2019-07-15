import cv2
import glob
import csv
import numpy as np
#import cProfile
import math
#import imageio
import pickle
#import os


def process(i):
    """
Takes in image name (as a string), processes the image,
shows all external contours (between the sizes 200 and 400) on image,
and returns a list of these contours. Used for the pick_cells function. 
    """
    
    #import image
    img = cv2.imread(i)

    #modify image 
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    gray_blur = cv2.GaussianBlur(gray, (15, 15), 0)

    thresh = cv2.adaptiveThreshold(gray_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 1)

    kernel = np.ones((5,5), np.uint8)
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    
    kernel = np.ones((15,15), np.uint8)
    close = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)

    cont_img = close.copy()
    contours, hierarchy = cv2.findContours(cont_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    loe= []

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area < 200 or area > 40000:
            continue
        if len(cnt) < 5:
            continue
        ellipse = cv2.fitEllipse(cnt)
        loe.append(ellipse)
        cv2.drawContours(img, [cnt], 0, (0,255,0),2)
        cv2.ellipse(img, ellipse, 0, 5,2)
        
    
    cv2.namedWindow('img', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('img', 1000, 750)

 
    cv2.imshow("img", img)
    return contours




def process_small(i, x, y):
    

    """
Takes in image name (as a string) and two ints an x and y value,
processes the image, crops the image to 1000 x 1000 with (x,y) at the centre
shows all external contours (between the sizes 200 and 400) on image,
and returns a list of these contours. Used for the main function. 
    """
    
    #import image
    imgUncut = cv2.imread(i)
    #img = imgUncut[0:1000, 0:1000]
    minX = imgUncut.shape[1]
    minY = imgUncut.shape[0]
    dist = round(min(min(min(x,y),minX),minY)/2)
    #img = imgUncut[y-dist:y+dist, x- dist:x+ dist]
    img = imgUncut
    
    #img = np.full((100,80,3), 12, np.uint8)
    #modify image 
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray_blur = cv2.GaussianBlur(gray, (15, 15), 0)
    thresh = cv2.adaptiveThreshold(gray_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 1)
    kernel = np.ones((5,5), np.uint8)
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
##    cv2.namedWindow('thresh', cv2.WINDOW_NORMAL)
##    cv2.resizeWindow('thresh', 1000, 750)
##    cv2.imshow("thresh", thresh)
##    cv2.namedWindow('open', cv2.WINDOW_NORMAL)
##    cv2.resizeWindow('open', 1000, 750)
##    cv2.imshow("open", opening)
    
    kernel = np.ones((20,20), np.uint8)
    close = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
##    cv2.namedWindow('close', cv2.WINDOW_NORMAL)
##    cv2.resizeWindow('close', 1000, 750)
##    cv2.imshow("close", close)
        
    cont_img = close.copy()
    contours, hierarchy = cv2.findContours(cont_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    loe= []
    
    for cnt in contours:
        area = cv2.contourArea(cnt)
        #if area < 200 or area > 40000:
        #   continue
        if len(cnt) < 5:
            continue
        ellipse = cv2.fitEllipse(cnt)
        loe.append(ellipse)
        cv2.drawContours(img, [cnt], 0, (0,255,0),2)
        cv2.ellipse(img, ellipse, 0, 5,2)
    
    cv2.namedWindow('img', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('img', 1000, 750)
    if contours == []:
        co = []
        c = []
    else:
        co = [get_best_ctr(contours, img)]
        c= get_best_ctr(contours, img)
    
#----------------  TESTING  -----------------------
    #cv2.drawContours(img, co, 0, (0,0,255),2) 
    #print(str(get_centre_val(c)[0]) + ", " + str(get_centre_val(c)[1]))
#----------------------------------------    
    cv2.imshow("img", img)
    return loe, img

def distance_from_centre(c, img):
    """
Finds the distance of a taken in contour from the
centre of a 1000x1000 image
    """
    #based off of crop size in process_small
    x, y = get_centre_val(c)
    ax = abs(x - (img.shape[1]/2)) 
    ay = abs(y - (img.shape[0]/2))
    return x+y

def get_best_ctr(ctrs, img):
    """
takes a list of contours and finds the one with
the lowest distance_from_centre
   """
    closest= ctrs[0]
    for c in ctrs:
        if distance_from_centre(c, img)< distance_from_centre(closest, img):
            closest = c
    return closest

def best_to_cor(ctrs, x, y):
    closest = ctrs[0]
    for c in ctrs:
        if dist(c,x,y)< dist(closest,x,y):
            closest = c
    return closest

def best_to_cor_e(ctrs, x, y):
    closest = ctrs[0]
    for c in ctrs:
        if dist_e(c,x,y)< dist_e(closest,x,y):
            closest = c
    return closest

def dist(ctr, x, y):
    #(cx,cy),(MA,ma), angle = ctr
    cx, cy = get_centre_val(ctr)
    a = round(math.sqrt((cx-x)*(cx-x) + (cy-y)*(cy-y)))
    return a

def dist_e(ctr, x, y):
    (cx,cy),(MA,ma), angle = ctr
    #cx, cy = get_centre_val(ctr)
    a = round(math.sqrt((cx-x)*(cx-x) + (cy-y)*(cy-y)))
    return a

def good_cont(c):
    """
checks to see if a contour size falls in a range
    """
    return cv2.contourArea(c)>10 and cv2.contourArea(c)<10000


def get_centre_val(c):
    """
Takes in a contour and an x or y string and returns
the sellected coordinate of the centre of the contour 
    """
    x, y, w, h = cv2.boundingRect(c)
    return x,y

def pick_cells(i):
    """
takes in an image name, processes it, nubers every contour,
displays the image with numbers, asks for user input of cell selection
returns contour of selected cell. 
    """
    ctrs = process(i)
    img = cv2.imread(i)

    cv2.namedWindow('img', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('img', 1000, 750)

    #iterate over list of contours to only draw and count valid contours 
    i=0
    #cellCount = 0
    while (i< len(ctrs)):
        if (good_cont(ctrs[i])):
            #print(i)

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

    #just me testing to make sure the correct contour is being picked 
    cv2.drawContours(img, ctrs, cell, (0,0,255),2)
    cv2.namedWindow('img', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('img', 1000, 750)
    #test get centre functions 
    x,y = get_centre_val(ctrs[cell])
    
    cv2.putText(img,"the point", (x,y),
                        cv2.FONT_HERSHEY_TRIPLEX, 2, (0,0,255),4)
    cv2.imshow("img", img)
    #end testing 

    #print(x, y)
    ellipse = cv2.fitEllipse(ctrs[cell])

    return ellipse

def get_size_data(c):
    """
Take in a cell contour and returns area of the contour
    """
    return cv2.contourArea(c)

def get_size_data_e(e):
    (x, y), (MA, ma), angle = e
    A = math.pi * MA * ma
    return A

def main(directory):
    """
takes in an image name, runs pick_cells, finds contour of picked_cell
for every image that follows reg ex rules based on the first image
returns list of lists of contours of that cell and times of that cell
    """
    files = glob.glob(directory+"*")
    files.sort()
    #files.pop(len(files)-1)
    img = files[0]
    init = pick_cells(img)
#    initTime = int(img[-19:-6])
    #files = glob.glob('2019-03-01_20;0*.jpg')
    nfiles = len(files)

    last = init
    (cellX,cellY),(MA,ma), angle = last
    #cellX, cellY = get_centre_val(last)
    i = 0
    contours = []
    times= []

    for file in files:
        
        #print(cellX, cellY)
        i= i+1
        #if image_light(file)< 90:
        #    return contours
        c=[]
        time = int(file[-19:-6])
        times.append(time)
        if i ==nfiles :
            return contours
        
        ctrs, im = process_small(file, cellX,cellY) 
        #cv2.destroyWindow('img')
        if ctrs== []:
            print(i)
            continue
            #print(i)
            #return contours            
        else:
            
            (cellX,cellY),(MA,ma), angle = last
            #cellX, cellY = get_centre_val(last)
            best= best_to_cor_e(ctrs, cellX,cellY)
            
            #row = [time, best]
            c.append(best)
            print(get_size_data_e(best))
            last = best
            contours.append(c)
                
        #cv2.drawContours(im, best, 0, (0,0,255),2) 
        #cv2.imshow("img", im)
        
        
    return contours


def times(directory):
    files = glob.glob(directory+"*")
    files.sort()
    #files.pop(len(files)-1)
    #print(files)
    init = int(files[0][-19:-6])
    t= []
    for file in files:
        time = int(file[-19:-6])-init
        t.append(time)
        print(time)
    return t

def pickle_the_thing(time, ctrs):
    pickle_out= open("list.pickle","wb")
    pickle.dump(ctrs, pickle_out)
    pickle_out.close()

    pickle_out= open("time.pickle","wb")
    pickle.dump(time, pickle_out)
    pickle_out.close()


def globifier(img):
    pickle_the_thing(main(img))


def run():
    print("the directory:")
    d= input()
    times(d+"*")
    while True:
        print("do you want to get data? y or n")
        i = input()
        if i == "y":
            main(d+"*")
        if i == "n":
            quit()

run()

#tlist = times("../modified glass BB 90C 0523 2/")
#pickle_the_thing(tlist,clist)
#pick_cells("2019-05-23_10;35_1558633031815ms.jpg")

#process_small("2019-05-23_10;35_1558632981781ms.jpg", 1416,1273)
#process("2019-05-23_10;35_1558633092782ms.jpg")
#process("2019-05-23_10;35_1558633031815ms.jpg")
