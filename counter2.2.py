import cv2
import glob
import csv
import numpy as np
import cProfile
import math
import imageio


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
    
    cv2.namedWindow('img', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('img', 1000, 750)
    co = [get_best_ctr(contours)]
    c= get_best_ctr(contours)
    
#----------------  TESTING  -----------------------
##    cv2.drawContours(img, co, 0, (0,0,255),2) 
##    print(str(get_centre_val(c, "x")) + ", " + str(get_centre_val(c, "y")))
#----------------------------------------    
    cv2.imshow("img", img)
    return contours

def image_light(fn):
    """
Takes in a file name and quantifies the darkness of an image
    """
    img = imageio.imread(fn, as_gray=True)
    return np.mean(img)

def good_cont(c):
    """
checks to see if a contour size falls in a range
    """
    return cv2.contourArea(c)>1000 and cv2.contourArea(c)<10000

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

    #just me testing to make sure the correct contour is being picked 
    cv2.drawContours(img, ctrs, cell, (0,0,255),2)
    cv2.namedWindow('img', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('img', 1000, 750)
    #test get centre functions 
    x = get_centre_val(ctrs[cell],"x")
    y = get_centre_val(ctrs[cell],"y")
    cv2.putText(img,"the point", (x,y),
                        cv2.FONT_HERSHEY_TRIPLEX, 2, (0,0,255),4)
    cv2.imshow("img", img)
    #end testing 
    
    return ctrs[cell]
   
    
def get_size_data(c):
    """
Take in a cell contour and returns area of the contour
    """
    return cv2.contourArea(c)


def get_centre_val(c,xy):
    """
Takes in a contour and an x or y string and returns
the sellected coordinate of the centre of the contour 
    """
    x, y, w, h = cv2.boundingRect(c)
    cx = x
    cy = y
    if xy == "x":
        return int(cx)
    else:
        return int(cy)
    

def distance_from_centre(c):
    """
Finds the distance of a taken in contour from the
centre of a 1000x1000 image
    """
    #based off of crop size in process_small
    x = abs(get_centre_val(c, "x") - 500) 
    y = abs(get_centre_val(c, "y") - 500)
    return x+y


def get_best_ctr(ctrs):
    """
takes a list of contours and finds the one with
the lowest distance_from_centre
   """
    closest= ctrs[0]
    for c in ctrs:
        if distance_from_centre(c)< distance_from_centre(closest):
            closest = c
    return closest



def globifier(img):
    """
takes in an image name, runs pick_cells, finds contour of picked_cell
for every image that follows reg ex rules based on the first image
returns list of lists of contours of that cell and times of that cell
    """
    init = pick_cells(img)
    initTime = int(img[-19:-6])
    files = glob.glob('2019-03-01_20;0*.jpg')
    nfiles = len(files)

    last = init
    cellY = get_centre_val(last, "y")
    cellX = get_centre_val(last, "x")
    i = 0
    contours = []

    for file in files:
        if image_light(file)< 90:
            return contours
        ctrs = process_small(file, cellX,cellY)
        best= get_best_ctr(ctrs)
        time = int(file[-19:-6])
        row = [time, best]
        if not(outlier(get_size_data(last), get_size_data(best))):
            contours.append(row)
            print(get_size_data(best))
            last = best

    return contours



def size(img):
    """
Takes in an image name, runs pick cell, then finds size of cells
and globifier. Returns list of lists of time and cell size  
    """
    ctrs = globifier(img)
    output= []
    for ctr in ctrs:
        row = [ctr[0], get_size_data(ctr[1])]
        output.append(row)
    return output

def outlier(point1, point2):
    return abs(point1-point2)> 600


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

def main(img, fnc):
    """
takes in an image name and a string of the type of operation requested,
runs that function and returns the output
    """
    if fnc == "size":
        make_csv(size(img))

 
main("2019-03-01_20;01_1551499548124ms.jpg","size")    
        
def profile():
    cProfile.run('main("2019-03-01_20;01_1551499548124ms.jpg")')


    

## USELESS FUNCTIONS
##--------------------------------------------------------------------
def reasonable(c, e):
    return get_data(c) > get_data(e) - 50 #and get_data(c) < get_data(e) + 100 

def good_cell(i, c):
    diff = 10
    iCell = get_centre(i)
    cCell = get_centre(i)
    x = abs(iCell[0] - cCell[0])
    y = abs(iCell[1] - cCell[1])
    return x < diff and y < diff    

def get_centre(c):
    x, y, w, h = cv2.boundingRect(c)
    cx = x
    cy = y
    return [cx,cy]

##def make_file(locd):
##    with open('cell Data file', 'w') as csvfile:
##        wr = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
##        wr.writerow(locd)
##        # I realize that this adds this all in one row


#not actually callable, just storing my code fragment
#so i dont have to look for it later
def test():
    #start testing
    img = process_small_test(file, cellX, cellY)
    cv2.drawContours(img, best, -1, (0,0,255),2)
    cv2.namedWindow('img', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('img', 1000, 750)
    cv2.imshow("img", img)
    #end testing

def process_small_test(i, x, y):
    
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
    return img

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

##def main(img):
##
##    init = pick_cells(img)
##    initTime = int(img[-19:-6])
##    files = glob.glob('2019-03-01_20;0*.jpg')
##    nfiles = len(files)
##
##    last = init
##    cellY = get_centre_val(last, "y")
##    cellX = get_centre_val(last, "x")
##    print(cellX)
##    print(cellY)
##    i = 0
## 
##    with open('cell Data file', 'w') as csvfile:
##        wr = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
##        wr.writerow(["time", "cell size"])
##    
##        for file in files:
##           if image_light(file)< 90:
##               return csv
##           ctrs = process_small(file, cellX,cellY)
##           best= get_best_ctr(ctrs)
##           print(get_size_data(best))               
##           cellData = get_size_data(best)
##           last = best
##           time = int(file[-19:-6])
##           row = [time, cellData]
##           wr.writerow(row)
##
##
##           i += 1
##           if i == 650:
##               return csv
##    
##    return csv

