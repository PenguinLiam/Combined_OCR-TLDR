
#   MAIN FILE   #

# =========================================================================== #
'''
Master file, run file. The program will be launched from here and all files will
be collated here. Contains information about the interface and calls the OCR and
TLDR programs. Comments are attempted to be written in accordance with PEP 8
Style Guide: 
http://legacy.python.org/dev/peps/pep-0008/#comments
https://google.github.io/styleguide/pyguide.html
'''
# =========================================================================== #



# ====== Imports (Python Native Modules and My Program Modules) ====== #

import TLDR_Program as TLDR
import OCR_Program as OCR
import Encryption as E
import Variables as v
import time
import os
import pickle
import tkinter as tk
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from PIL import ImageTk, Image


# ====== Pre-Interface Processes ====== #

def checkFiles():
    '''Sub-routine for clearing any files older than the spefified length of
    time. Default is 30 days, but may be changed by the user in the settings
    tab.
    '''
    # Initialising the current time and identifying the file directories
    now = time.time()
    paths = ["Summaries", "OCR_Images", "OCR_Conversions"]
    # Gets a currently working directory (cwd) - file from which the program
    # is being run and appends the name of the folder within for checking.
    # If file is older than the specified time, delete the file.
    for i in paths:
        path = os.path.join(os.getcwd(), i)
        for f in os.listdir(path):
            f = os.path.join(path, f)
            if os.stat(f).st_mtime < now - v.settings["noOfDays"] * 8400:
                if os.path.isfile(f):
                    os.remove(f)


           
# ====== Creating the Interface ====== #

class Page(tk.Frame):
    '''Re-orders pages to make selected page the on on top.

    Attributes:
        tk.Frame: A tkinter frame upon which the page is placed
    '''

    def __init__(self, *args, **kwargs):
        '''Inits Page with the tkinter frame'''
        tk.Frame.__init__(self, *args, **kwargs)

    def show(self):
        '''Performs the page lift operation'''
        self.lift()


class Home_Page(Page):
    '''Page containing an introduction to the project.

    Introduces the user to the program with a message displayed on screen
    (infoText).

    Attributes:
        Page: The frame upon which the page is placed (using place geometry)
        *args: Arguments for tkinter Frames (size, frame/window placement, etc.)
        *kwargs: Arguments for tkinter Frames (size, frame/window placement, etc.)
    '''

    def __init__(self, *args, **kwargs):
        '''Inits the home page with the tkinter Frame and packs all
        the widgets to that frame'''
        Page.__init__(self, *args, **kwargs)
        titleFrame = tk.Frame(self, width=50, height=70, padx=10, bg="#22313F")
        titleFrame.pack(side="top", fill="x", expand=True)
        label = tk.Label(titleFrame, text="Welcome", pady=10, font=("Helvetica", 35), fg="white", bg="#22313F", anchor="center")
        label.pack(side="top", fill="both", expand=True)

        # Text displayed within the image window
        infoText = '''
            Welcome to my combined OCR and TL;DR program!\n
            This project was an A-Level work in an attempt to learn how to use:
            - OCR Software
            - TL;DR Software
            - Interfacing Tools (TKinter)\n
            This is in testing and not all of the features are functional so please don't be too harsh on me!
            '''
        WelcomeInfoLabel = tk.Label(self, text=infoText, font=("Helvetica", 16), padx=100, pady=60)
        WelcomeInfoLabel.pack(anchor="center")


class Settings_Page(Page):
    '''Page for altering program settings.

    Packs widgets to the frame and allows input for number of days to keep 
    files. Allows the user to save the altered settings or reset all settings
    and files - delete all program added files and return settings to defaults.

    Attributes:
        Page: The frame upon which the page is placed (using place geometry)
        *args: Arguments for tkinter Frames (size, frame/window placement, etc.)
        *kwargs: Arguments for tkinter Frames (size, frame/window placement, etc.)
    '''

    def __init__(self, *args, **kwargs):
        '''Inits the settings page with the tkinter Frame and packs all
        the pages widgets to that frame'''
        Page.__init__(self, *args, **kwargs)
        # ===== Title Frame Changes ===== #
        titleFrame = tk.Frame(self, width=50, height=70, padx=10, bg="#22313F")
        titleFrame.pack(side="top", fill="x", expand=True)
        label = tk.Label(titleFrame, text="Settings", pady=10, font=("Helvetica", 35), fg="white", bg="#22313F", anchor="sw")
        label.pack(side="top", fill="both", expand=True)

        # ===== Top of Page =====#
        daysFrame = tk.Frame(self, padx=20, pady=40, bg="blue")
        daysFrame.pack(side="top", anchor="w", fill="y", expand=True)
        daysLabel = tk.Label(daysFrame, text="Days to Keep Files", font=("Helvetica", 16), padx=5)
        daysLabel.pack(side="left", expand=True)
        self.daysEntry = tk.Entry(daysFrame, font=("Helvetica", 16))
        self.daysEntry.insert(0, str(v.settings["noOfDays"]))
        self.daysEntry.pack(side="left", expand=True)
        
        # ===== Bottom of Page =====#
        confirm = tk.Button(self, text="Confirm Changes", font=("Helvetica", 16), command=self.saveSettings)
        confirm.pack(side="left", expand=True)
        reset = tk.Button(self, text="Reset Settings to Default", font=("Helvetica", 16), command=self.warning)
        reset.pack(side="left", expand=True)
        tempFrame = tk.Frame(self, bg="green")
        tempFrame.pack(side="bottom", fill="both", expand=True)
        tempCanvas = tk.Canvas(tempFrame, height=800, bd=0, highlightthickness=0, relief='ridge')
        tempCanvas.pack(fill="both", expand=True)

    def saveSettings(self):
        '''Saves changes made by the user to the settings.txt file'''
        v.settings["noOfDays"] = int(self.daysEntry.get())
        if v.settings["noOfDays"] > 50:
            message = messagebox.showinfo("Alert", "To reduce this program's impact on your secondary memory, please enter a value lower than 50")
            v.settings["noOfDays"] = 30
            self.daysEntry.delete(0, "end")
            self.daysEntry.insert(0, str(v.settings["noOfDays"]))
        print(v.settings)
        message = messagebox.showinfo("Alert", "Settings saved successfully...")
    
    def warning(self):
        '''Warning icon for deleting all files (Yes/No response)'''
        # Procedes if 'Yes' was selected but returns if 'No' was selected
        if tk.messagebox.askyesno("WARNING", "WARNING: By clicking yes, you agree to delete all previous OCR conversions and TL; DR saves..."):
            self.reset()
        else:
            print("RETURNING...")
            return

    def reset(self):
        '''Resets the settings dictionary and removes settings.txt and all files
        from the folders Settings, OCR_Images, and OCR_Conversions.
        
        Raises:
            FileNotFoundError: The file settings.txt did not exist
            Exception: Any other error flagged and returned with error message
        '''
        print("RESETTING...")
        v.settings = {"noOfDays":30, "noOfSummaries":1, "noOfOCRs":1}
        try:
            os.remove("Settings.txt")
            paths = ["Summaries", "OCR_Images", "OCR_Conversions"]
            for i in paths:
                path = os.path.join(os.getcwd(), i)
                for f in os.listdir(path):
                    f = os.path.join(path, f)
                    if os.path.isfile(f):
                        os.remove(f)
            message = messagebox.showinfo("Alert", "All files were removed and settings restored")
        except FileNotFoundError:
            message = messagebox.showinfo("Alert", "All files were removed and settings restored")
            return
        except Exception as e:
            errorBox = messagebox.showinfo("Error", "An unexpected error occured:\n"+'"'+str(e)+'"')


class TLDR_Page(Page):
    '''Page for carrying out Too Long; Didn't Read functions.

    Packs widgets to frame and allows the input of text to the input widget
    from either a .txt file or manual text input. After text and title have
    been entered, allows the user to summarise the text, calling from the
    external TLDR module.

    Attributes:
        Page: The frame upon which the page is placed (using place geometry)
        *args: Arguments for tkinter Frames (size, frame/window placement, etc.)
        *kwargs: Arguments for tkinter Frames (size, frame/window placement, etc.)
    '''

    def __init__(self, *args, **kwargs):
        '''Inits the TLDR page with the tkinter Frame and packs all
        the widgets to that frame'''
        Page.__init__(self, *args, **kwargs)
        # ===== Title Frame Changes ===== #
        titleFrame = tk.Frame(self, width=50, height=70, padx=10, bg="#22313F")
        titleFrame.pack(side="top", fill="x", expand=True)
        label = tk.Label(titleFrame, text="TL;DR", pady=10, font=("Helvetica", 35), fg="white", bg="#22313F", anchor="sw")
        label.pack(side="top", fill="both", expand=True)
         
        # ===== Right Side of Page ===== #
        sTextBoxFrame = tk.Frame(self, width=70, height=100, padx=75, pady=50, bg="purple")
        sTextBoxFrame.pack(side="right", fill="both", expand=True)
        var = tk.IntVar()
        self.noOfSentences = tk.Entry(sTextBoxFrame, textvariable=var)
        self.noOfSentences.pack(side="bottom")
        getSummary = tk.Button(sTextBoxFrame, text="Get Summary", command=self.get_summary)
        getSummary.pack(side="bottom")      
        addFile = tk.Button(sTextBoxFrame, text="Add Text to Summarise", command=self.file_browser)
        addFile.pack(side="bottom")
        self.summaryBox = tk.Text(sTextBoxFrame, width=75, height=150, bg="pink")
        self.summaryBox.pack(side="top", expand=True)

        # ===== Left Side of Page ===== #
        titleBoxFrame = tk.Frame(self, width=70, height=100, padx=50, pady=50, bg="orange")
        titleBoxFrame.pack(side="top", expand=True)
        self.titleBox = tk.Text(titleBoxFrame, width=75, height=2, font=("Helvetica", 18), bg="yellow")
        self.titleBox.pack(side="top", expand=True)
        textBoxFrame = tk.Frame(self, width=70, height=100, padx=50, pady=50, bg="blue")
        textBoxFrame.pack(side="bottom", fill="both", expand=False)
        self.mainBox = tk.Text(textBoxFrame, width=75, height=150, bg="light blue")
        self.mainBox.pack(side="bottom", fill="both", expand=True)

    def get_summary(self):
        '''Calls External TLDR module to summarise text.
        
        Attributes:
            title: Text extracted from self.titlebox
            text: Text extracted from self.mainBox
            summaryAmount: Integer extracted from self.noOfSentences
            summary: the returned summary of text from the TLDR module

        Raises:
            TypeError: A non-integer was entered into self.noOfSentences
            UnicodeEncodeError: An unknown encoding format was used in the
                text for summary
            UnicodeDecodeError: An unknown decode format was used in the
                text for summary
            Exception: Any other error flagged and returned with error message
        '''
        title = self.titleBox.get(1.0, "end-1c")
        text = self.mainBox.get(1.0, "end-1c")
        try:
            summaryAmount = int(str(self.noOfSentences.get()))
            print(type(summaryAmount), summaryAmount)
            summary = TLDR.summarise(title, text, summaryAmount)
            self.summaryBox.delete(1.0, "end-1c")
            self.summaryBox.insert(1.0, summary)
        except TypeError:
            errorBox = messagebox.showinfo("Type Error", "You must enter an integer")
        except (UnicodeEncodeError, UnicodeDecodeError) as e:
            errorBox = messagebox.showinfo("Unicode Encode/Decode Error", "An error occured:\n"+'"'+str(e)+'"')
        except Exception as e:
            errorBox = messagebox.showinfo("Error", "An unexpected error occured:\n"+'"'+str(e)+'"')

    def file_browser(self):
        '''Opens a tkinter File Browser to select .txt files for summarising.
        
        Attributes:
            self.filename: Path to selected file from file browser
            text: Text from self.filename

        Raises:
            Exception: Any error flagged and returned with error message
        '''
        self.filename = askopenfilename(initialdir='OCR_Conversions', filetypes=[('Text files', '*.txt')])
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                text = f.read()
                self.mainBox.delete(1.0, "end-1c")
                self.mainBox.insert(1.0, E.decrypt(text))
        except Exception as e:
            errorBox = messagebox.showinfo("Error", "An unexpected error occured:\n"+'"'+str(e)+'"')
       

class OCR_Page(Page):
    '''Page for carrying out Optical Character Recognition functions.

    Packs widgets to frame and allows the input of image formats (.jpg, .jpeg
    .gif, .png., .bmp) selected in file browser. After an image is selected,
    calls the external OCR module to convert the images into text. Then outputs
    the text to a text box.

    Attributes:
        Page: The frame upon which the page is placed (using place geometry)
        *args: Arguments for tkinter Frames (size, frame/window placement, etc.)
        *kwargs: Arguments for tkinter Frames (size, frame/window placement, etc.)
    '''

    def __init__(self, *args, **kwargs):
        '''Inits the OCR page with the tkinter Frame and packs all
        the widgets to that frame'''
        Page.__init__(self, *args, **kwargs)  
        # ===== Title Frame Changes ===== #
        titleFrame = tk.Frame(self, width=50, height=70, padx=10, bg="#22313F")
        titleFrame.pack(side="top", fill="x", expand=True)
        label = tk.Label(titleFrame, text="OCR", pady=10, font=("Helvetica", 35), fg="white", bg="#22313F", anchor="sw")
        label.pack(side="top", fill="both", expand=True)

        mainFrame = tk.Frame(self, width=70, height=500)
        mainFrame.pack(fill="both", expand=True)

        # ===== Right of Page ===== #
        rightFrame = tk.Frame(mainFrame, width=70, height=100, padx=20, pady=50, bg="green")
        rightFrame.pack(side="right", fill="both", expand=True)
        self.outputBox = tk.Text(rightFrame, width=75, height=39, bg="pink")
        self.outputBox.pack(side="top", fill="y", expand=True)

        # ===== Left of Page ===== #
        leftFrame = tk.Frame(mainFrame, width=70, height=500, padx=75, pady=50, bg="blue")
        leftFrame.pack(side="left", fill="both", expand=True)
        browsebutton = tk.Button(leftFrame, text="BrowseFiles", command=self.file_browser)
        browsebutton.pack(side="top")
        self.imageLabel = tk.Label(leftFrame, width=300, height=20, padx=50, pady=50, bg="red")
        self.imageLabel.pack(side="top", expand=True)
        reConvertButton = tk.Button(leftFrame, text="Re-Convert", command=self.re_convert)
        reConvertButton.pack(side="bottom")
        convertButton = tk.Button(leftFrame, text="Convert", command=self.convert)
        convertButton.pack(side="bottom")

    def file_browser(self):
        '''Opens a tkinter File Browser to select image files for conversion.
        
        Attributes:
            self.filename: Path to selected file from file browser
            img: Image selected from file browser
            w, h: Image width and height (respectively)

        Raises:
            Exception: Any error flagged and returned with error message
        '''
        self.filename = askopenfilename(initialdir='C:/users/Liam/Pictures', filetypes=[("Image Formats", '*.jpg;*.jpeg;*.gif;*.png;*.bmp')])
        try:
            img = ImageTk.PhotoImage(Image.open(self.filename))
            w = img.width()
            h = img.height()
            if h > 550:
                h = 550
            self.imageLabel.configure(image = img, width=w+5, height=h+5)
            self.imageLabel.image = img
        except Exception as e:
            errorBox = messagebox.showinfo("Error", "An unexpected error occured:\n"+'"'+str(e)+'"')

    def convert(self):
        '''Calls the OCR module to convert the image to text.
        
        Attributes:
            text: Returned text from OCR conversion

        Raises:
            UnicodeEncodeError: If text returned contains unknown characters
                (not UTF-8 characters)
            Exception: Any other error flagged and returned with error message
        '''
        try:
            imageData = OCR.OCRConvert(self.filename)
            self.filename = imageData[1]
            text = imageData[0]
            print(self.filename)
            self.outputBox.delete(1.0, "end-1c")
            self.outputBox.insert(1.0, text)
        except UnicodeEncodeError as e:
            errorBox = messagebox.showinfo("Unicode Encode/Decode Error", "An error occured:\n"+'"'+str(e)+'"')
        except Exception as e:
            errorBox = messagebox.showinfo("Error", "An unexpected error occured:\n"+'"'+str(e)+'"')

    def re_convert(self):
        '''Calls the OCR module, starting with the cleanup process.
        
        Attributes:
            text: Returned text from OCR conversion
            
        Raises:
            UnicodeEncodeError: If text returned contains unknown characters
                (not UTF-8 characters)
            Exception: Any other error flagged and returned with error message
        '''
        try:
            imageData = OCR.cleanup_OCR(self.filename)
            self.outputBox.delete(1.0, "end-1c")
            self.outputBox.insert(1.0, imageData[0])
        except UnicodeEncodeError as e:
            errorBox = messagebox.showinfo("Unicode Encode/Decode Error", "An error occured:\n"+'"'+str(e)+'"')
        except Exception as e:
            errorBox = messagebox.showinfo("Error", "An unexpected error occured:\n"+'"'+str(e)+'"')

class MainWindow(tk.Frame):
    '''Main class for changing display page - Top level window.

    Packs widgets to frame. Creates the top level frame upon which any page is
    placed (using place geometry). Creates widgetsFrame containing the buttons
    for changing page, and mainFrame for layering everything else upon.

    Attributes:
        tk.Frame: Top level frame upon which everything else is placed
            (Place Geometry)
        *args: Arguments for tkinter Frames (size, frame/window placement, etc.)
        *kwargs: Arguments for tkinter Frames (size, frame/window placement, etc.)
    '''
    def __init__(self, *args, **kwargs):
        '''Inits the main window'''
        tk.Frame.__init__(self, *args, **kwargs)
        # Initialising the objects (each page)
        home = Home_Page(self)
        settings = Settings_Page(self)
        tldr = TLDR_Page(self)
        ocr = OCR_Page(self)

        # Builds the frame in which widgets are placed and the main frame for the interface
        widgetsFrame = tk.Frame(self, width=100, height=200, bg="#22313F")
        mainFrame = tk.Frame(self)
        
        # Packs the widget and main frame
        widgetsFrame.pack(side="left", fill="y", expand=False)
        mainFrame.pack(side="top", fill="both", expand=True)

        # Place geometry is used to overlap widgets within the program to give the illusion of multiple pages
        home.place(in_=mainFrame, x=0, y=0, relwidth=1) 
        settings.place(in_=mainFrame, x=0, y=0, relwidth=1)
        tldr.place(in_=mainFrame, x=0, y=0, relwidth=1, relheight=1)
        ocr.place(in_=mainFrame, x=0, y=0, relwidth=1)

        # Placing the buttons in the widgets frame on the left of the page
        settingsButton = tk.Button(widgetsFrame, text="Settings", font=("Helvetica", 12), pady=10, command=settings.lift)
        tldrButton = tk.Button(widgetsFrame, text="TLDR", font=("Helvetica", 12), pady=10, command=tldr.lift)
        ocrButton = tk.Button(widgetsFrame, text="OCR", font=("Helvetica", 12), pady=10, command=ocr.lift)
        
        # Packing the buttons and making them fill the bar on the X-Axis
        ocrButton.pack(fill="x")
        tldrButton.pack(fill="x")
        settingsButton.pack(fill="x")
        
        # Displays the first page (Home_Page)
        home.show()



# ====== Python Boiler Plate ====== #

if __name__ == "__main__":
    # File checking and save loading
    try:
        v.load()
    except:
        pass
    checkFiles()
    
    # Interface Boiler-Plate
    root = tk.Tk()
    root.title("Combined OCR & TL;DR Software")
    root.configure(bg="#DADFE1")
    main = MainWindow(root)
    main.pack(side="top", fill="both", expand=True)
    root.wm_geometry("1000x700")
    root.mainloop()
