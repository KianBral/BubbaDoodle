import os
from tkinter import *
from tkinter import messagebox, colorchooser
from tkinter.filedialog import asksaveasfilename,askopenfilename
import pyscreenshot as ImageGrab
from PIL import ImageTk,Image
import math
import time
# from pygame import mixer
import playsound


class Color_Button(Button):#Inherited custom made color button , with default command to change colour of pen
    def __init__(self,color):
        self.color=color
        super().__init__(
            borderwidth=0,
            highlightthickness=0,
            relief="flat",
            bg=color,
            width=10,
            height=5,
            command=self.on_click
        )
    def on_click(self):
        program.color_fg=self.color
        main.color_fg = self.color
        # main.canvas.config(cursor="dot "+self.color)

class main:
    def __init__(self, master, fileOpen):
        self.root = master
        self.root.title("BubbaDoodle!")
        self.root.state('zoomed')
        self.leah_mode = True
        self.fileOpen = ""

        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.button_width = math.floor(self.screen_width * .007)
        self.button_height = math.floor(self.screen_height * .002)
        self.root.geometry(f"{self.screen_width-int(self.screen_width*0.3)}x{self.screen_height-int(self.screen_height*0.3)}")


        self.color_fg = 'white'  # Colour of pen
        self.prev_color = 'white'
        self.color_bg = '#282828'  # Background colour
        self.root.configure(background='#282828')

        self.undo = open('undo.rec', 'w')

        # making the canvas and making it recognise movements of the mouse
        # Place the canvas as filling the entire screen
        #  + str(self.color_fg)
        self.canvas = Canvas(self.root, cursor="dot", bg='#282828', relief="flat", height=self.screen_height, width=(self.screen_width * .8))
        self.canvas.place(x=135, y=0)

        self.old_x = None
        self.old_y = None
        self.penwidth = 3
        self.tag = 0
        self.canvas.bind('<B1-Motion>', self.paint)  # drawing  line
        self.canvas.bind('<ButtonRelease>', self.reset)
        self.erasing = False
        
        if fileOpen != "":
            self.open(fileName=fileOpen)
            # try:
            #     self.fileOpen = fileOpen
            #     self.img = ImageTk.PhotoImage(Image.open(fileOpen))
            #     self.canvas.create_image(0,0, anchor=NW, image=self.img)
            # except:
            #     # TODO: add error message?
            #     messagebox.showwarning("Invalid file. Accepted types are JPEG, PNG, PS, BMP, and GIF")
            #     pass

        # making colour buttons
        colors = ['#a7d9fe', '#7f7f7f', 'white', '#ff3e49']
        i=.90;j=.37
        for color in colors:
            Color_Button(color).place(relx=i,rely=j)#Refer class Color_Button
            j+=.12
        
        # Brush + brushsize 
        self.Brush_Text = Label(self.root, text='BRUSH', bd=0, bg='white', font=('calibri', 11))
        self.Brush_Text.place(relx=.90, rely=.87, relwidth=.05)

        self.options = StringVar(self.root)
        self.options.set('3')#Default option
        self.size_chooser = OptionMenu(self.root, self.options, *( str(x) for x in range(21)))
        self.size_chooser.place(relx=.90, rely=.90, relwidth=.05)


        # Eraser 
        self.eraser_button = Button(self.root, text='ERASE', font=('calibri', 10), bd=2, bg='white', command=self.erase, width=self.button_width, height=self.button_height, relief=RIDGE)
        self.eraser_button.place(relx=.90, rely=.94)


        # Buttons on top left, from top to bottom
        self.Pallet_For_Foreground = Button(self.root, text='PALETTE', font=('calibri', 10), bd=2, bg='white', command=self.choose_color, width=self.button_width, height=self.button_height, relief=RIDGE)
        self.Pallet_For_Foreground.place(x=8,y=5)

        self.open_button=Button(self.root,text="OPEN" ,font=('calibri', 10), bd=2, width=self.button_width, height=self.button_height, bg='white',command=self.open, relief=RIDGE)
        self.open_button.place(x=8, y=45)

        self.save_button = Button(self.root, text='SAVE', font=('calibri', 10), bd=2, bg='white', command=self.save, width=self.button_width, height=self.button_height, relief=RIDGE)
        self.save_button.place(x=8, y=85)

        self.undo_button = Button(self.root, text='UNDO', font=('calibri', 10), bd=2, width=self.button_width, height=self.button_height, bg='white',command=self.undo_exec, relief=RIDGE)
        self.undo_button.place(x=8, y=125)

        self.clear_button = Button(self.root, text='CLEAR', font=('calibri', 10), bd=2, bg='white', command=self.clear, width=self.button_width, height=self.button_height, relief=RIDGE)
        self.clear_button.place(x=8, y=416)

        self.Background_Button = Button(self.root, text='BG COLOR', font=('calibri', 10),bd=2, bg='white', command=self.change_bg, width=self.button_width, height=self.button_height, relief=RIDGE)
        self.Background_Button.place(x=8, y=205)

        self.Toggle_Button = Button(self.root, text='DRAWER', font=('calibri', 10),bd=2, bg='white', command=self.togglePaint, width=self.button_width, height=self.button_height, relief=RIDGE)
        self.Toggle_Button.place(x=8, y=245)


    # All functions are defined below
    def paint(self, e):
        '''creates a canvas where you can paint'''

        if self.old_x and self.old_y:

            self.canvas.create_line(self.old_x, self.old_y, e.x, e.y,
                                    width=self.options.get(),
                                    fill=self.color_fg,
                                    capstyle=ROUND,
                                    smooth=True,
                                    tag='my_tag' + str(self.tag))

        self.old_x = e.x
        self.old_y = e.y

    def reset(self, e):
        '''reseting or cleaning the canvas'''
        self.old_x = None
        self.old_y = None

        self.canvas.create_oval(e.x, e.y, e.x, e.y,
                                width=self.options.get(),
                                outline=self.color_fg,
                                fill=self.color_fg,
                                tag='my_tag' + str(self.tag))
        self.undo.write(f"self.canvas.delete('{'my_tag' + str(self.tag)}')\n")
        self.tag += 1

    def clear(self, background_clear = False):
        '''clears the canvas'''
        if background_clear:
            res = messagebox.askquestion('Background Color', 'Changing the background color will clear the canvas, are you sure you want to do that?')
        else:
            res = messagebox.askquestion('Clear Canvas', 'Are you sure you want to clear the canvas?')
            
        if res == 'yes':
            self.canvas.delete(ALL)

            if self.fileOpen != "":
                self.img = ImageTk.PhotoImage(Image.open(self.fileOpen))
                self.canvas.create_image(0,0, anchor=NW, image=self.img)

            # TODO: make canvas clear before sound plays
            playsound.playsound("./Explosion.mp3")

            return True
        
        return False

    
    def togglePaint(self):
        if not self.leah_mode:
            self.canvas.unbind('<Motion>')
            self.canvas.unbind('<Leave>')
            self.canvas.bind('<B1-Motion>', self.paint)
            self.canvas.bind('<ButtonRelease-1>', self.reset)
            self.leah_mode = True
        else:
            self.canvas.bind('<Motion>', self.paint)
            self.canvas.bind('<Leave>', self.reset)
            self.canvas.unbind('<B1-Motion>')
            self.canvas.unbind('<ButtonRelease-1>')
            self.leah_mode = False

    def erase(self):
        '''erasing stuff simply by changing colour of the brush to white'''
        # When user is currently erasing
        if self.erasing:
            self.color_fg = self.prev_color
            self.canvas.config(cursor="dot")
            self.erasing = False
            return

        self.canvas.config(cursor="dotbox")
        self.prev_color = self.color_fg
        self.erasing = True
        self.undo.write(f"self.color_fg='{self.color_fg}'\n")
        self.undo.write(f"self.options.set({self.options.get()})\n")
        self.color_fg = self.canvas['bg']


    def undo_exec(self):
        self.undo.close()
        # Find last line and execute it
        file = open("copy.txt", 'w')
        with open("undo.rec", 'r') as undo:
            length = sum(1 for x in undo)
        with open("undo.rec", 'r') as undo:
            count = 0
            for line in undo:
                count += 1
                if count != length:
                    file.write(line)
                pass
        file.close()
        os.replace(r'copy.txt', r'undo.rec')
        try:
            command = line
            exec(command)

        except UnboundLocalError:
            pass
        self.undo = open("undo.rec", 'a')

    def save(self):
        # Asking format
        filename: str = asksaveasfilename(initialdir="/Desktop", title="Select file", filetypes=(
            ('JPEG', '*.jpg'), ('PNG', '*.png'), ('PS', '*.ps'),
            ('BMP', '*.bmp'),
            ('GIF', '*.gif')),defaultextension=".jpg")
        print(filename)
        if filename.endswith('.ps'):
            # Saving a postscript file
            try:
                self.canvas.postscript(file=filename, colormode='color')
                messagebox.showinfo('File saved : ', str(filename))
            except:
                print('No file saved')

        else:
            try:
                # Making values for a screenshort
                x = self.root.winfo_rootx() + self.canvas.winfo_x()
                y = self.root.winfo_rooty() + self.canvas.winfo_y()
                x1 = x + self.canvas.winfo_width()
                y1 = y + self.canvas.winfo_height()
                screenshort = ImageGrab.grab().crop((x, y, x1, y1))
                screenshort.save(filename)
                messagebox.showinfo('File saved : ', str(filename))
            except:
                print('Error Saving File')

    def open(self, fileName):
        # file_chosen=askopenfilename(initialdir="./dist/Doodles", title="Select file", filetypes=(
        #     ('JPEG', '*.jpg'), ('PNG', '*.png')),defaultextension=".jpg")
        try:
            self.img_src = Image.open(fileName)
            self.img = ImageTk.PhotoImage(self.img_src)
            img_height = self.img.height()
            img_width = self.img.width()
            
            height_scale = 1
            width_scale = 1
            if img_height > self.screen_height:
                height_scale = img_height // self.screen_height
            if img_width > self.screen_width * 0.8:
                width_scale = img_width // (self.screen_width * 0.8)

            if height_scale > width_scale:
                img_height //= height_scale
                img_width //= height_scale

            else:
                img_height //= width_scale
                img_width //= width_scale
            
            self.img_src = self.img_src.resize((int(img_width), int(img_height)))
            self.img_final = ImageTk.PhotoImage(self.img_src)

            self.canvas.create_image(0,0,anchor=NW, image=self.img_final)
        except Exception as e:
            return()

    def choose_color(self):
        # variable to store hexadecimal code of color
        self.undo.write(f"self.color_fg='{self.color_fg}'\n")
        color_code = colorchooser.askcolor(title="Choose color")
        if color_code != (None, None):
            self.color_fg=color_code[1]#colour_code[1] is hex value of chose color. color_code[0] is rgb value of chosen color

    def change_bg(self):
        self.undo.write(f"self.canvas['bg']='{self.color_bg}'\n")
        color_code = colorchooser.askcolor(title="Choose Color")
        res = self.clear(background_clear=True)

        if res:
            # if the eraser was selected, change drawing color to default
            if self.color_fg == self.canvas['bg']:
                self.color_fg = 'white'

            self.canvas['bg'] = color_code[1]

    def graph(self):
        try:
            MsgBox = messagebox.askyesnocancel(title='Graph',message='YES for Ruled Graph and No for Unruled Graph')
            if MsgBox:
                self.img = ImageTk.PhotoImage(Image.open('graph_ruled.png'))
                self.canvas.create_image(30, 20, anchor=NW, image=self.img)
            else:
                self.img = ImageTk.PhotoImage(Image.open('graph_unruled.png'))
                self.canvas.create_image(-100, 0, anchor=NW, image=self.img)

        except:
            messagebox.showwarning("That isn't working")

if __name__ == '__main__':

    #Splash Screen
    splash_root = Tk()
    splash_root.title('Bubba Doodle!')

    screen_width = splash_root.winfo_screenwidth()
    screen_height = splash_root.winfo_screenheight()
    splash_root.geometry(f"{screen_width-int(screen_width*0.3)}x{screen_height-int(screen_height*0.3)}")

    splash_img = ImageTk.PhotoImage(Image.open("bubbdoob_splash.jpg").resize((screen_width-int(screen_width*0.3), screen_height-int(screen_height*0.3))))
    splash_label = Label(splash_root, image=splash_img)
    splash_label.pack()

    def canvas(destroyRoot, fileName):
        destroyRoot.destroy()

        root = Tk()
        root.resizable(width=False, height=False)
        root.title('BubbaDoodle!')
        global program
        program=main(root, fileName)

        root.mainloop()

    types = [('JPEG', '*.jpg'), ('PNG', '*.png')]

    def openFileFunction(destroyRoot, dir):
        file_chosen=askopenfilename(initialdir=dir, title="Select file", filetypes=(types))
        canvas(destroyRoot, file_chosen)

    def homeScreen():
        # Home Screen
        splash_root.destroy()

        home_root = Tk()
        home_root.eval('tk::PlaceWindow . center')
        home_root.title('Bubba Doodle!')
        home_root.geometry("700x100")

        def emptyCanvas():
            canvas(home_root, "")

        t1_button = Button(home_root, text="Blank Canvas", command=emptyCanvas)
        t1_button.place(x=100, y=25)

        debug = True
        if (debug):
            temp1 = "./dist/Templates/connect_dots_star_invert.jpg"
            temp2 = "./dist/Templates/connect_dots_cloud_invert.jpg"
            openB = "./dist/Doodles"
        else:
            temp1 = "./Templates/connect_dots_star_invert.jpg"
            temp2 = "./Templates/connect_dots_cloud_invert.jpg"
            openB = "./Doodles"

        
        template1 = Button(home_root, text='Open Star', command=lambda:[canvas(home_root, temp1)])
        template1.place(x=200, y=25)

        template2 = Button(home_root, text='Open Cloud', command=lambda:[canvas(home_root, temp2)])
        template2.place(x=300, y=25)

        openButton = Button(home_root, text='Open Picture', command=lambda:[openFileFunction(home_root, openB)])
        openButton.place(x=400, y=25)

    splash_label.after(2000, homeScreen)
    splash_root.mainloop()