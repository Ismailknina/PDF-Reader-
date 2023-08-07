from tkinter import * # For GUI
from PIL import Image # For Resizing The Images 
from pdf2image import convert_from_path # For Converting PDF pages to Images
from tkinter import filedialog # For taking The path of PDF File
import os # Giving The Filedialog a directory where it can starts
from tkinter import messagebox

parent=Tk() # parent object
parent.geometry("500x650+400+10") # geometry of the window
parent.iconbitmap("pdf-icon.ico") # icon of the window
parent.title("PDF Reader [Ismail Knina]") # title
parent.configure(background="White")
def on_closing():
    if messagebox.askyesno(title="Quit?",message="Do you really wants to Quit ? You will lose all the Processe!"):
        parent.destroy()
parent.protocol("WM_DELETE_WINDOW",on_closing)

def browse():
    """
    Taking The path of PDF File using filedialog module 
    """
    try:
        filename = filedialog.askopenfilename(initialdir=os.getcwd(),
                                            title="PDF Viewer [Ismail Knina]" ,
                                            filetypes=(("PDF File" , ".pdf"),
                                                        ("PDF File" , ".txt"),
                                                        ("PDF File" , ".PDF")))
    except:
         messagebox.showerror(title="ERROR",message="Sorry There is an Error! Close The App and Try Again")
         parent.destroy()
    finally:
        convert(filename)

# Creating Button for opening File
button = Button(master=parent , text="Open File" , font=("Tajawal 20") , bd=0 , cursor="hand2" , command=browse , fg="white" , bg="red")
button.pack(fill="both")

# Photo at the beginig
photo_at_the_beginig = PhotoImage(file='logo.png')
display_photo = Label(parent , image=photo_at_the_beginig , bg="White" )
display_photo.pack()


def convert(filename):
    """Converting PDF Pages Into Images using pdf2image module where convert_from_path is a function"""
    try:
        images = convert_from_path(poppler_path = r"poppler-23.07.0\Library\bin" , pdf_path=filename) # convert_from_path: This is a function provided by the pdf2image library, which is used to convert a PDF file into a list of images.
        global list_of_images_from_pdf # make it global so that we accesse it from another function
        list_of_images_from_pdf = [] # will contains the path of images
        for i in range(len(images)):
            # Save pages as images in the pdf
            images[i].save('new_folder_images\page'+ str(i) +'.png') # saving images in a folder called new_folder_images
            list_of_images_from_pdf.append('new_folder_images\page'+ str(i) +'.png') # storing the path of the images into a list
    except:
        messagebox.showerror(title="ERROR",message="Sorry There is an Error! Close The App and Try Again or check if the new_folder_images exist !")
        parent.destroy()
    finally:
        resizing_images()


def resizing_images():
    """ This piece of code is for reisizing the images and saving them before showing them  """
    try:
        global list_of_resizeble_images # make it global so that we accesse it from another function
        list_of_resizeble_images = [] # will contains the path of images being resized
        i=0
        for ph in list_of_images_from_pdf :       
            image = Image.open(ph) # Initializing the photo
            new_image = image.resize((500, 650)) # Resizing Photo
            new_image.save(f'resizable_images\p{i}.png') # Saving images in a folder called resizable_images
            list_of_resizeble_images.append(f'resizable_images\p{i}.png') # storing the path of the images into a list
            i+=1
    except:
        messagebox.showerror(title="ERROR",message="Sorry There is an Error! Close The App and Try Again or check if the resizable_images exist !")
        parent.destroy()
    finally:
        creating_canvas_and_showing_images_with_scrollbar()
     


def creating_canvas_and_showing_images_with_scrollbar():
    display_photo.destroy() # destroying the photo and the button so we have a place to show the images
    button.destroy()
    canvas = Canvas(parent, height=200) # a canvas in the parent object
    frame = Frame(canvas) # a frame in the canvas
    # a scrollbar in the parent
    scrollbar = Scrollbar(parent, orient="vertical", command=canvas.yview)
    # connect the canvas to the scrollbar
    canvas.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y") # comment out this line to hide the scrollbar
    canvas.pack(side="left", fill="both", expand=True) # pack the canvas
    # make the frame a window in the canvas
    canvas.create_window((4,4), window=frame, anchor="nw", tags="frame")
    # bind the frame to the scrollbar
    frame.bind("<Configure>", lambda x: canvas.configure(scrollregion=canvas.bbox("all")))
    parent.bind("<Down>", lambda x: canvas.yview_scroll(3, 'units')) # bind "Down" to scroll down
    parent.bind("<Up>", lambda x: canvas.yview_scroll(-3, 'units')) # bind "Up" to scroll up
    # bind the mousewheel to scroll up/down
    parent.bind("<MouseWheel>", lambda x: canvas.yview_scroll(int(-1*(x.delta/40)), "units"))

    #########################################################
    """ This part of the function code is for showing the images in a frame """
    for i, image_name in enumerate(list_of_resizeble_images):
            photo = PhotoImage(file=image_name)
            label = Label(frame, image=photo)
            label.photo = photo  # To prevent garbage collection 
            label.pack()  # pack them
    #########################################################


parent.mainloop() # run program        