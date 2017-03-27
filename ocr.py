# -*- coding: utf-8 -*-
"""
Author:         Dave Kavanagh
                R00013469
                david.j.kavanagh@mycit.ie

Date:           31/01/2017

Description:    Receives image data via the constructor and performs ocr on 
                specifically mapped portions of the image, returning the text
                as JSON.

© Dave Kavanagh, 2017
"""
from io import BytesIO
import re
import base64
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
        #remove image encoding prefix
        image_data = input_file[24:]
        self.input_file = image_data

    def open_image(self):
        """
        Attempts to load an image from disk.
        """
        global cropped_img
        try:
            self.img = Image.open(BytesIO(base64.b64decode(self.input_file)))

        except:
            print "ERROR: Unable to load image!"
            exit(1)

    def treat_image(self, img):
        img = img.filter(ImageFilter.UnsharpMask)
        img = ImageOps.autocontrast(img)
        img = img.filter(ImageFilter.GaussianBlur)
        img = img.filter(ImageFilter.SHARPEN)

        # convert from grayscale to pure black and white
        img = img.point(lambda x: 0 if x < 125 else 250, '1')
        return img

    def process_image(self):
        """
        Treats the image, subjecting it to various steps in order to enhance the possibility of accurate text recognition.
        """
        gray_img = ImageOps.grayscale(self.img)

        # crop desired regions
        # time region
        time_section = gray_img.crop((920, 630, 1600, 1020))
        self.time_section = self.treat_image(time_section)

        # selection region
        selection_section = gray_img.crop((920, 950, 1600, 1520))
        self.selection_section = self.treat_image(selection_section)

        # odds region
        odds_section = gray_img.crop((920, 1550, 1600, 1970))
        self.odds_section = self.treat_image(odds_section)#odds region

        # stake region
        stake_section = gray_img.crop((1160, 2200, 1700, 2350))
        self.stake_section = self.treat_image(stake_section)

    def detect_text(self, img, section):
        """
        Attempts to extract text from an image
        """
        text = tess.image_to_string(img)
        if len(text) < 1:
            text = "No text detected in " + section + " section!"

        return text

    def analyze_bet(self):
        """
        Perform OCR on betting slip
        """
        if self.input_file:
            self.open_image()
            self.process_image()

            #detect time
            #self.time_section.show()
            time = self.detect_text(self.time_section, 'time')
            if '.' in time:
                time = time.replace('.', ':')
            if '-' in time:
                time = time.replace('-', ':')
            if ';' in time:
                time = time.replace(';', ':')

            #detect selection
            #self.selection_section.show()
            selection = self.detect_text(self.selection_section, 'selection')

            # detect odds
            #self.odds_section.show()
            odds = self.detect_text(self.odds_section, 'odds')
            if '.' in odds:
                odds = odds.replace('.', '/')

            ocr_data = {'time': time, 'selection': selection, 'odds': odds}

        return ocr_data

    def identify_stake(self):
        """
        Perform OCR on bet to identify stake
        :return: JSON containing stake value
        """
        if self.input_file:
            self.open_image()
            self.process_image()

            # detect stake
            self.stake_section.show()
            stake = self.detect_text(self.stake_section, 'stake')
            print stake
            if 'o' in stake:
                stake = stake.replace('o', '0')
            if 'O' in stake:
                stake = stake.replace('O', '0')

            ocr_data = {'stake': stake}

        return ocr_data



