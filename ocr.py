# -*- coding: utf-8 -*-
"""
Author:         Dave Kavanagh
                R00013469
                david.j.kavanagh@mycit.ie

Date:           31/01/2017

Description:    Receives image data via the constructor and performs ocr on 
                specfically mapped portions of the image, returning the text 
                as JSON.

© Dave Kavanagh, 2017
"""
import sys
#import cv2
import numpy as np
import pytesseract as tess
from PIL import Image, ImageFilter, ImageOps

class OCR:
    """
    Class used to perform OCR
    """

    def __init__(self, input_file):
        """
        Constructor
        :param input_file: file path passed from command line
        """
        self.input_file = input_file

    def open_image(self):
        """
        Attempts to load an image from disk.
        """
        global cropped_img
        try:
            self.img = Image.open(self.input_file)

        except:
            print "ERROR: Unable to load image!"
            exit(1)

    def detect_lines(self):
        """
        Detect lines in an image using the "Hough Transform" - NOT CURRENTLY USED!!
        """
        minLineLength = 5
        maxLineGap = 1
        img_arr = np.array(self.img)
        #lines = cv2.HoughLinesP(img_arr, 1, np.pi / 180, 100, minLineLength, maxLineGap)
        #for x1, y1, x2, y2 in lines[0]:
        #    cv2.line(img_arr, (x1, y1), (x2, y2), (255, 255, 255), 2)

        #convert ndarray back to image object
        self.img = Image.fromarray(img_arr)

    def process_image(self):
        """
        Treats the image, subjecting it to various steps in order to enhance the possibility of accurate text recognition.
        """
        gray_img = ImageOps.grayscale(self.img)

        # crop desired region
        #cropped_img = gray_img.crop((20, 500, 1200, 1720))
        #cropped_img = gray_img.crop((900, 500, 1300, 820))
        cropped_img = gray_img.crop((120, 1350, 2300, 3020))

        img = cropped_img.filter(ImageFilter.UnsharpMask)
        img = ImageOps.autocontrast(img)
        img = img.filter(ImageFilter.GaussianBlur)
        img = img.filter(ImageFilter.SHARPEN)

        #convert from grayscale to pure black and white
        self.img = img.point(lambda x: 0 if x<125 else 250, '1')

    def detect_text(self):
        """
        Attempts to extract text from an image
        """
        self.text = tess.image_to_string(self.img)
        if len(self.text) < 1:
            self.text = "No text detected in this image!"

    def ocr(self):
        """
        Perform OCR on an image
        """
        if self.input_file:
            self.open_image()
            self.process_image()
            "self.img.show()"
            self.detect_text()

        return self.text

if __name__ == "__main__":
    file_path = sys.argv[1]
    ocr_obj = OCR(file_path)
    print ocr_obj.ocr()
