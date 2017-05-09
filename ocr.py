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
import base64
import pytesseract as tess
from PIL import Image, ImageFilter, ImageOps

class OCR:
    """
    Class used to perform OCR
    """

    def __init__(self, input_file):
        """
        Constructor
        :param input_file: base64 string passed invoking function
        """
        #remove image encoding prefix
        image_data = input_file[24:]
        self.input_file = image_data


    def open_image(self):
        """
        Attempts to load an image from disk.
        """

        try:
            self.img = Image.open(BytesIO(base64.b64decode(self.input_file)))

        except:
            print "ERROR: Unable to load image!"
            exit(1)

        print self.img.size
        self.img = self.img.resize((1000,1300))

    def treat_image(self, img):

        img = img.filter(ImageFilter.UnsharpMask)
        img = img.filter(ImageFilter.EDGE_ENHANCE)
        img = img.filter(ImageFilter.GaussianBlur)
        img = img.filter(ImageFilter.MedianFilter)
        img = img.filter(ImageFilter.SMOOTH)

        # convert from grayscale to pure black and white
        img = img.point(lambda x: 0 if x < 125 else 250, '1')

        return img

    def process_image(self):
        """
        Treats the image, subjecting it to various steps in order to enhance the possibility of accurate text recognition.
        """
        gray_img = ImageOps.grayscale(self.img)
        treated_img = self.treat_image(gray_img)

        # crop desired regions
        # time region
        self.time_section = treated_img.crop((510, 350, 925, 510))

        # selection region
        self.selection_section = treated_img.crop((510, 515, 885, 750))

        # odds region
        self.odds_section = treated_img.crop((510, 815, 885, 1050))

        # stake region
        self.stake_section = treated_img.crop((660, 1080, 950, 1175))

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

            # detect time
            self.time_section.show()
            time = self.detect_text(self.time_section, 'time')
            if '.' in time:
                time = time.replace('.', ':')
            if '-' in time:
                time = time.replace('-', ':')
            if '+' in time:
                time = time.replace('+', '0')
            if ';' in time:
                time = time.replace(';', ':')

            if time[2] != ':':
                str = list(time)
                str[2] = ':'
                time = "".join(str)

            if len(time) > 5:
                time = time[:5]

            # detect selection
            self.selection_section.show()
            selection = self.detect_text(self.selection_section, 'selection')
            if '/' in selection:
                selection = selection.replace('/', '1')

            # detect odds
            self.odds_section.show()
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

            # print for debugging
            print "Stake identified as",stake
            if 'No text' not in stake:
                if 'o' in stake:
                    stake = stake.replace('o', '0')
                if 'O' in stake:
                    stake = stake.replace('O', '0')
                if 'C)' in stake:
                    stake = stake.replace('C)', '0')
                if 'C' in stake:
                    stake = stake.replace('C', '0')
                if 'c)' in stake:
                    stake = stake.replace('c)', '0')
                if 'c' in stake:
                    stake = stake.replace('c', '0')
                if ',' in stake:
                    stake = stake.replace(',', '.')
                if '~' in stake:
                    stake = stake.replace('~', '.')
                if '-' in stake:
                    stake = stake.replace('-', '.')
                if 'i' in stake:
                    stake = stake.replace('i', '1')
                if 'I' in stake:
                    stake = stake.replace('I', '1')
                if 's' in stake:
                    stake = stake.replace('s', '5')
                if 'S' in stake:
                    stake = stake.replace('S', '5')
                if ')' in stake:
                    stake = stake.replace(')', '')
                if ' ' in stake:
                    stake = stake.replace(' ', '')

            #_stake = ''.join(i for i in stake if i.isdigit())
            ocr_data = {'stake': stake}

            return ocr_data