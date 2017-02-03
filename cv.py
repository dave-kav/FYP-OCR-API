import cv2
import numpy as np
from PIL import Image
import pytesseract as tess

img = cv2.imread('static/bet1.jpg')
#gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(img,50,150,apertureSize = 3)
minLineLength = 100
maxLineGap = 10
lines = cv2.HoughLinesP(edges,1,np.pi/180,100,minLineLength,maxLineGap)
for x1,y1,x2,y2 in lines[0]:
    cv2.line(img,(x1,y1),(x2,y2),(255,0,0),2)

cv2.imwrite('houghlines5.jpg',img)
img = Image.fromarray(img)
img.show()

try:
    print tess.image_to_string(img)
except:
    print "Nothing to analyse..."
