from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *
#
import sys
import re
import PIL.ImageDraw
import PIL.Image
import string


FILE_NAME = None
 
def new_file():
    global FILE_NAME
    FILE_NAME = 'Untitled'
    textBox.delete('1.0', END)
 
def open_file():
    global FILE_NAME
    inPut = askopenfile(mode = 'r')
    if inPut is None:
        return
    FILE_NAME = inPut.name
    print(FILE_NAME)
 
def save_file():
    if FILE_NAME == None:
        showinfo(title = 'Error!', message = 'File is not load!')
    
    str = textBox.get('1.0', END)
    data = stringToBinary(str)
    if  binaryToImage(data) == 0:
        showinfo(title = 'Save', message = 'File has been saved.')
    else:
        showinfo(title = 'Save', message = 'Error!\nFile has not been saced!')

 
def save_as_text():
    if FILE_NAME == None:
        showinfo(title = 'Error!', message = 'File is not load!')
    
    out = asksaveasfile(mode = 'w', defaultextension = '.txt')
    data = textBox.get('1.0', END)
    try:
        out.write(data.rstrip())
    except Exception:
        showerror(title = 'Oops!', message = 'Unable to save file....')
 
def closeWindow():
    if askyesno(title = 'Exit', message = 'Do you want to quit?'):
        root.destroy()

def about():
    showinfo(title = 'About', message = 'Spyware GUI\n Version 0.9\n Jaroslav Bershacky (c)')

def product_help():
    showinfo(title = 'Help', message = 'Ask how it works creator.')

def save_file_button(event):
    save_file()

def clean():
    global FILE_NAME
    
    if FILE_NAME == None:
        showinfo(title = 'Error!', message = 'File is not load!')
    
    image = PIL.Image.open(FILE_NAME)
    lenght = area(image)
    if downToEven(image, lenght) == 0:
        showinfo(title = 'Clean', message = 'File has been cleared.')
    else:
        showinfo(title = 'Clean', message = 'Error!\nFile has not been cleard!')

def clean_button(event):
    clean()   

def read_button(event):
    if FILE_NAME == None:
        showinfo(title = 'Error!', message = 'File is not load!')
    
    data = readFromImage()
    
    if data != None:
        textBox.delete('1.0', END)
        textBox.insert('1.0', data)
    else:
        showinfo(title = 'Read', message = 'File is empty.')

#
#
#
#
#
#
#
#
def area (image):
    (width, height) = image.size
    return width * height

def downToEven (image, lenght):
    path = FILE_NAME
    draw = PIL.ImageDraw.Draw(image)
    (width, height) = image.size
    
    if (width * height) >= lenght:
        mod = lenght // width + 1
        div = lenght % width

        for i in range(mod):
            for j in range(width):
                (R, G, B, A) = image.getpixel((j, i))
               
                  
              
                if R % 2 != 0:
                    R = R - 1
                if G % 2 != 0:
                    G = G - 1
                if B % 2 != 0:
                    B = B - 1
                  
                draw.point((j, i), (R, G, B))
                if j == mod and i == div:
                    break
            image.save(path)
                    
        del draw
        return 0
    else:
        del draw
        return 1

def stringToBinary (str):
    str = "   " + str 
    
    binary = ''.join(format(ord(x), 'b') for x in str)
    
    while len(binary) % 3 != 0:
        binary = "0" + binary
    
    
    data = [(int(x)) for x in binary]
       

   
    return data

def binaryToImage (data):
    path = FILE_NAME
    image = PIL.Image.open(path)
    draw = PIL.ImageDraw.Draw(image)
    (width, height) = image.size

    lenght = len(data) // 3
    mod = lenght // width + 1
    
    if downToEven (image, lenght) == 0:
        for i in range(mod):
            for j in range(width):
                (R, G, B, A) = image.getpixel((j, i))
                
                R = R + data.pop()
                G = G + data.pop()
                B = B + data.pop()
                  
                draw.point((j, i), (R, G, B))
                if len(data) == 0:
                   break  
 
            image.save(path)

        del draw
        return 0
    else:
        del draw
        return 1

def readFromImage ():
    path = FILE_NAME
    image = PIL.Image.open(path)
    (width, height) = image.size
    
    numberOfStr = 1
    numberOfPix = 2
    s = ""

    while s.startswith("   ") == False:
        data = []
        s = ""
       
        for i in range(numberOfStr):
            for j in range(numberOfPix):
                (R, G, B, A) = image.getpixel((j, i))
        
                if R % 2 != 0:
                    data.append(1)
                else:
                    data.append(0)
                if G % 2 != 0:
                    data.append(1)
                else:
                    data.append(0)
                if B % 2 != 0:
                    data.append(1)
                else:
                    data.append(0)

        
        binary = ''
        
        for i in range(len(data)):
            binary +=  str(data.pop())
        print(binary)
        
        m = re.search('[1]{1}', binary)
        if m == None:
            return None
        else:
            binary  =  binary[:0] + binary[m.start():]
        
       
        ABC = " ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz.,:;!?-_=+1234567890"
        br = []

        for i in range(len(ABC)):
            br.append(''.join(format(ord(x), 'b') for x in ABC[i]))
        size = len(binary)
    
        for i in range(size):
            for j in range(len(ABC)):
                if (binary.startswith(br[j]) == True):
                    s = s + ABC[j]
                    binary = binary[:0] + binary[len(br[j]):]
                    break
        
        numberOfPix += 1
        if numberOfPix == width and numberOfStr <= height:
                numberOfStr += 1
                numberOfPix = 1
        elif numberOfPix == width and numberOfStr > height:
            return "This file is empty!"
            break
    s.replace("   ", "")
    return s    

#
#

root = Tk()
root.title('SpywareGUI')


#BACK GROUND
panelFrame = Frame(root, height = 60, bg = 'gray')
textFrame = Frame(root, height = 340, width = 600)

panelFrame.pack(side = 'top', fill = 'x')
textFrame.pack(side = 'bottom', fill = 'both', expand = 1)

#FUNCTIONAL
textBox = Text(textFrame, font = 'Arial 14', wrap = 'word')
scrollBar = Scrollbar(textFrame)

scrollBar['command'] = textBox.yview
textBox['yscrollcommand'] = scrollBar.set

textBox.pack(side = 'left', fill = 'both', expand = 1)
scrollBar.pack(side ='right', fill = 'y')

#BUTTON
cleanBut = Button(panelFrame, text = 'Clean')
readBut = Button(panelFrame, text = 'Read')
saveBut = Button(panelFrame, text = 'Save')

cleanBut.bind('<Button-1>', clean_button)
readBut.bind('<Button-1>', read_button)
saveBut.bind('<Button-1>', save_file_button)

cleanBut.place(x = 10, y = 10, height = 30, width = 60)
readBut.place(x = 85, y = 10, height = 30, width = 60)
saveBut.place(x = 160, y = 10, height = 30, width = 60)

# MENU
menuBar = Menu(root)
fileMenu = Menu(menuBar)
helpMenu = Menu(menuBar)

menuBar.add_cascade(label = 'File', menu = fileMenu)
#fileMenu.add_command(label = 'New', command = new_file)
fileMenu.add_command(label = 'Open', command = open_file)
fileMenu.add_command(label = 'Save', command = save_file)
fileMenu.add_command(label = 'Save as text', command = save_as_text)
fileMenu.add_command(label = 'Clean', command = clean)
#fileMenu.add_separator()
#fileMenu.add_command(label = 'Option')
fileMenu.add_separator()
fileMenu.add_command(label = 'Exit', command = closeWindow)

menuBar.add_cascade(label = 'Help', menu = helpMenu)
helpMenu.add_command(label = 'Product Help', command = product_help)
helpMenu.add_separator()
helpMenu.add_command(label = 'About', command = about)

root.config(menu = menuBar)
root.mainloop()