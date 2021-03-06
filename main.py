import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import os 

caminho = 'dataset/image9.jpg'

def fillHoles(src):
    contours,hierarchy = cv.findContours(src, cv.RETR_CCOMP, cv.CHAIN_APPROX_SIMPLE)
    dst = np.zeros(src.shape, np.uint8)
    color = 255
    for i in range(len(contours)):
        cv.drawContours(dst, contours,i, color, -1, 8, hierarchy, 0)
    return dst

def eliminateCont(src):
    contours,hierarchy = cv.findContours(src, cv.RETR_CCOMP, cv.CHAIN_APPROX_SIMPLE)
    
    for i in range(len(contours)):
        if(cv.contourArea(contours[i],False) < 30000):
            color = 0
            cv.drawContours(src, contours, i, color, -1, 8, hierarchy, 0)
    return src

def create_dir():
    pastas = os.listdir('./results')
    if len(pastas) == 0:
        return 'result_1'
    else:
        indice = pastas[-1].split('_')
        indice = int(indice[1])+1
        return 'result_' + str(indice)

def createImgs(src):
    contours,hierarchy = cv.findContours(src, cv.RETR_CCOMP, cv.CHAIN_APPROX_SIMPLE)
    dir_name = create_dir()
    os.mkdir('./results/'+dir_name)
    for i in range(len(contours)):
        points = cv.boundingRect(contours[i])
        cv.imwrite('./results/'+dir_name+'/'+'img_'+str(i+1)+'.png', img[points[1]:points[1]+points[3], points[0]:points[0]+points[2]])

img = cv.imread(caminho)
img = cv.blur(img,(3,3))

gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

th = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 17, -3)

black = np.array(np.zeros(th.shape), dtype=np.uint8)

result = cv.morphologyEx(th, cv.MORPH_ERODE,cv.getStructuringElement( cv.MORPH_CROSS, ( 5, 5) ))

lines = cv.HoughLinesP(result, 1, np.pi/60, 100, minLineLength = 60,  maxLineGap=10)

for line in lines:
	x1, y1, x2, y2 = line[0]
	cv.line(black, (x1, y1), (x2, y2), (255,255,255), 3)

th1 = 60
th2 = th1 * 0.4
edges = cv.Canny(img, th1, th2)

black = fillHoles(cv.bitwise_or(black,edges))
black = cv.morphologyEx(black, cv.MORPH_ERODE,cv.getStructuringElement( cv.MORPH_RECT, ( 6, 6) ))
black = eliminateCont(black)

createImgs(black)