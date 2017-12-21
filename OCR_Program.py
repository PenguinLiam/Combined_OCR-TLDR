
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
import time
import sys
import os



# ====== Main OCR Class ====== #

class OCR:
    '''Class for carrying out Optical Character Recognition functions.

    Class within which all the OCR tools reside. Receives image input and first
    tries to identify text within the image. If no text is found, the 
    'image clean-up' process is called, converting the image to black and white
    and enlarging in small incriments. The conversion is then re-tried.
    '''
    def __init__(self, file):
        '''Inits the class. Assigns the object wide variables.'''
        self.tries = 0
        self.OCRNumber = str(v.settings["noOfOCRs"])
        self.completeName = ("OCR_#"+self.OCRNumber+"_"+v.date)
        self.file = file

    def convert(self):
        '''Attempts to read the text from the image. If unsuccessful, the
        cleaupprocess is employed to improve readability.

        Returns:
            A list containing the image text and the file location of the image

        Raises:
            Exception: Any error causes the program to either clean-up image
                and retry (up to 5 times) or return a failure
        '''
        im = Image.open(self.file)
        im.save(os.path.join('OCR_Images', self.completeName+".jpeg"), 'JPEG', quality=90)
        self.file = "OCR_Images/"+self.completeName+".jpeg"
        while self.tries < 6:
            try:
                self.imageText = pytesseract.image_to_string(Image.open(self.file))
                if self.spellcheck():
                    self.save()
                    break
                else:
                    self.tries += 1
                    self.cleanup()
            except Exception as e:
                self.tries += 1
                print(str(e))
                self.cleanup()
        return [self.imageText, self.file]

    def cleanup(self):
        '''Removes image noise and improves image readability.'''
        im = Image.open(self.file).convert("L")
        width, height = im.size
        x, y = im.size
        # Smaller iterations for upscaling provide better quality. LANCZOS used
        # (new name for anti-aliasing in PIL)
        while width < (x * 2) and height < (y * 2):
            im = im.resize((width + 20, height + 20), Image.LANCZOS)
            im.save(os.path.join('OCR_Images', self.completeName+".jpeg"), 'JPEG', quality=90)
        self.file = "OCR_Images/"+self.completeName+".jpeg"
        # Identifies whether the script is being called from convert
        # or externally
        if self.tries > 0:
            return self.convert()

    def spellcheck(self):
        '''Checks to see whether there are any commonly appearing words in
        the converted text.

        Returns:
            A boolean value - True for success, False for failure.
        '''
        text = self.imageText
        for character in text:
            if character not in v.alphabet:
                text = text.replace(character, "")

        bool = False
        text.split(" ")
        for word in text:
            if i in v.alphabet:
                bool = True
                break
        return bool

    def save(self):
        '''Saves the OCR Converted file to the OCR_Conversions folder'''
        with open(os.path.join('OCR_Conversions', self.completeName+".txt"), "w", encoding="utf-8") as file:
            file.write(E.encrypt(self.imageText))
        v.settings["noOfOCRs"] += 1
        v.save()        
        


# ====== Main Sub-Routines ====== #

def convert(file):
    '''Main refferal sub-routine for OCR program'''
    ocr = OCR(file)
    return ocr.convert()

def cleanup(file):
    '''Cleanup referral sub-routine for OCR program'''
    ocr = OCR(file)
    return ocr.convert()



# ====== Python Boiler Plate ====== #

if __name__ == "__main__":
    '''Asks for inputs if called as main file'''
    try:
        file = ("Enter a file location: ")
        convert(file)
    except:
        print("There was an error or no text could be identified")











        
