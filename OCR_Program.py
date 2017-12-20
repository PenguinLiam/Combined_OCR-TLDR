
#    OCR PROGRAM    #

# =========================================================================== #
'''
Program for converting image files with text in them into text as a .txt format
or other format with the text also displayed in the program interface. Comments
are attempted to be written in accordance with PEP 8 Style Guide: 
http://legacy.python.org/dev/peps/pep-0008/#comments
https://google.github.io/styleguide/pyguide.html
'''
# =========================================================================== #



# ====== Imports (Python Native Modules and My Program Modules) ====== #

from PIL import ImageFilter, Image
import Encryption as E
import Variables as v
import pytesseract
import sys
import os
import time



# ====== Main OCR Class ====== #

class OCR:
    '''Class for carrying out Optical Character Recognition functions.

    Class within which all the OCR tools reside. Receives image input and first
    tries to identify text within the image. If no text is found, the 
    'image clean-up' process is called, converting the image to black and white
    and enlarging in small incriments. The conversion is then re-tried.
    '''

    def __init__(self):
        '''Inits the OCR class. Links pytesseract to the tesseract.exe file.'''
        pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract'
        self.tries = 0
        self.OCRNumber = str(v.settings["noOfOCRs"])
        self.completeName = ("OCR_#"+self.OCRNumber+"_"+v.date)

    def save(self, text):
        '''Saves the OCR Converted file to the OCR_Conversions folder'''
        with open(os.path.join('OCR_Conversions', self.completeName+".txt"), "w", encoding="utf-8") as file:
            file.write(E.encrypt(text))
        v.settings["noOfOCRs"] += 1
        v.save()

    def spellcheck(self, imageText):
        '''Checks to see whether there are any commonly appearing words in
        the converted text.

        Attributes:
            imageText: List for of the words identified by the OCR conversion.
            bool: Boolean value of whether a word is shared between the OCR
            conversion and the list of common english words.
           
         Returns:
            A boolean value stating whether there were any shared words between
            the list of common words and words in the text.
        '''
        imageText = imageText.split(" ")
        bool = False
        for i in imageText:
            if i in v.notAcceptedWords:
                bool = True
                break
        return bool

    def cleanup(self, file):
        '''Removes image noise and improves image "read-ability"

        Attributes:
            im: Opened image in black and white
            width, height: Image width and height (respectively) - dynamic
            x, y: Image width and height (respectively) - static 
            location: File location of the cleaned-up image
        '''
        im = Image.open(file).convert("L")
        print("# ------------------------------------------- #")
        print("Image info: \nFormat:", im.format, "\nSize:", im.size ,"\nMode:", im.mode)
        print("# ------------------------------------------- #\n\n\n")
        # Resizing the image
        width, height = im.size
        x, y = im.size
        # Smaller iterations in image size change provide better quality upscaling
        # LANCZOS is the new name for Antialiasing in PIL
        while width < (x * 2) and height < (y * 2):
            im = im.resize((width + 20, height + 20), Image.LANCZOS)
            im.save(os.path.join('OCR_Images', self.completeName+".jpeg"), 'JPEG', quality=90)
            width, height = im.size

        location = "OCR_Images/"+self.completeName+".jpeg"
        imageData = self.ocr_convert(location)
        return imageData

    def ocr_convert(self, location):
        '''Optical Character Recognition functions and additional logic
        
        Attempts to read the text from the image. If unsuccessful, the clean-up
        process is called improve OCR usability.

        Attributes:
            im: Image opened from location
            self.tries: Number of clean-up attempts used (max. 5)
            newLocation: location of image after being saved to OCR_Images
            imageText: Converted text from image

        Returns:
            A list containing the image text and the new location of the image

        Raises:
            Exception: Any error causes the program to either clean-up image
                and retry (up to 5 times) or return a failure
        '''
        im = Image.open(location)
        im.save(os.path.join('OCR_Images', self.completeName+".jpeg"), 'JPEG', quality=90)
        newLocation = "OCR_Images/"+self.completeName+".jpeg"
        while self.tries < 6:
            try:
                print(self.tries)
                imageText = pytesseract.image_to_string(Image.open(newLocation))
                bool = self.spellcheck(imageText)
                if bool == True:
                    self.save(imageText)
                    break
                else:
                    self.tries += 1
                    cleanup(newLocation)
            except Exception as e:
                print("# ------------------------------------------- #")
                print("Error:", str(e))
                print("CLEANING UP IMAGE ("+str(self.tries)+")")
                print("# ------------------------------------------- #")
                self.tries += 1
                # Only cleans up image if needed (saves processing time)
                self.cleanup(newLocation) 
        imageData = [imageText, newLocation]
        return imageData



# ====== Main Sub-Routines ====== #

def OCRConvert(file):
    '''Main referral sub-routine for OCR program'''
    imageData = ocr.ocr_convert(file)
    # Returns a list containing the text from the image and the new location
    return imageData

def cleanup_OCR(file):
    '''Cleanup referral sub-routine for OCR program'''
    imageData = ocr.cleanup(file)
    # Returns a list containing the text from the image and the new location
    return imageData



# ====== Python Boiler Plate ====== #

if __name__ == "__main__":
    '''Asks for inputs if not called by another module'''
    ocr = OCR()
    file = input("Enter file path: ")
    OCRConvert(file)
else:
    ocr = OCR()


    