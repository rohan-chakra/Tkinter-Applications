from Tkinter import *
import os
import Pmw
import tkFileDialog
import tkMessageBox
import tkFont


root = Tk()
root.geometry('700x450')
root.title("Text Editor")
root.iconbitmap("Icons/Text_Editor.ico")
global number
number = 0
Pmw.initialise()



def New():
 TextPad()
 show_line_number()


def Open():
   global filename, textpad
   filename = tkFileDialog.askopenfilename(title = 'Open')
   root.title(os.path.basename(filename) + " - Text Editor")
   New()
   current_pagename = notebook.getcurselection()
   Rename_page = notebook.tab(current_pagename)
   Rename_page["text"] = os.path.basename(filename)   
   fp = open(filename,"r")     
   textpad.insert(1.0,fp.read(), 'margin') 
   fp.close()
   show_line_number()

def Save():
 global filename
 try:
  fp = open(filename, "w")
  copytext = textpad.get(1.0, END) 
  fp.write(copytext)
  fp.close()
 except:
  saveas()
  

def saveas():
 try:
  savefile = tkFileDialog.asksaveasfilename(title = 'Save', defaultextension = '.txt', initialfile = 'new')
  file = open(savefile, "w")
  global filename
  filename = savefile
  copytext = textpad.get(1.0, END)
  file.write(copytext)
  root.title(os.path.basename(filename) + " - Text Editor")
  file.close
 except:
  pass


def Close():
   current_page = notebook.getcurselection()
   ans = tkMessageBox.askyesno(title = "Save", message = "Do you want to save the current file ?")
   if ans == 'yes':
      Save()
      notebook.delete(current_page)
      
   else:
      notebook.delete(current_page)      

def Close_All():
   global number
   page_names = notebook.pagenames()
   for i in range(0, len(page_names)):
    ans = tkMessageBox.askyesno(title = "Save", message = "Do you want to save the current file ?")
    if ans == 'yes':
       Save()
       notebook.delete(page_names[i])
      
    else:
       notebook.delete(page_names[i]) 
    

def Search(): 
   searchbox = Toplevel(root)
   searchbox.geometry('400x150')
   searchbox.title('Find')
   searchbox.iconbitmap("Icons/Search.ico")
   textpad.tag_configure('search', background = 'coral')
   
   def find_word():
       if x.get() == '1': 
        pos = textpad.search(entry.get(), '1.0', stopindex = END)
       if x.get() == '2':
        pos = textpad.search(entry.get(), END, stopindex = '1.0', backwards = TRUE)
       index = pos
       if not index:
        tkMessageBox.showerror("Info", "No match found")
       else:
        textpad.tag_add('search', index, '%s+ %sc' %(index, len(entry.get())))
       
   def find_all():
       start = "1.0"
       while 1:
        pos = textpad.search(entry.get(), start, stopindex = END)
        if not pos:
         break
        textpad.tag_add('search', pos, '%s+ %sc' %(pos, len(entry.get())))
        start = pos+ "+1c"
        
   def Cancel():
       textpad.tag_remove('search', '1.0', END)
       searchbox.destroy()
   
   label = Label(searchbox, text = 'Find what : ')
   label.grid(row = 0, column = 0, padx = 10, pady = 10)
   entry = Entry(searchbox)
   entry.grid(row = 0, column = 1, padx= 10, pady = 10)
   
   findButton = Button(searchbox, text = 'Find', command = find_word)
   findButton.grid(row = 0, column = 2, padx = 10, pady = 10)
   findAllButton = Button(searchbox, text = 'Find All', command = find_all)
   findAllButton.grid(row = 1, column = 2, padx = 10, pady = 10)
   cancelButton = Button(searchbox, text = 'Cancel', command = Cancel)
   cancelButton.grid(row = 2, column = 2, pady = 10)
   
   x = StringVar()
   x.set(1)
   Up = Radiobutton(searchbox, text = 'Up', variable = x, value = 1)
   Up.grid(row = 1, column = 0, padx = 10, pady = 10)
   Down = Radiobutton(searchbox, text = 'Down', variable = x, value = 2)
   Down.grid(row = 1, column = 1, pady = 10)
   
   searchbox.mainloop()
     
  
def Select_All():
   textpad.tag_add(SEL, 1.0, END)
  
def Undo():
   textpad.event_generate("<<Undo>>")
   show_line_number()
   
def Redo():
   textpad.event_generate("<<Redo>>")
   show_line_number()
   
def Cut():
   textpad.event_generate("<<Cut>>")
   show_line_number()
   
def Copy():
   textpad.event_generate("<<Copy>>")
   show_line_number()
   
def Paste():
   textpad.event_generate("<<Paste>>")
   show_line_number()
 

def highlight_line():
    textpad.tag_remove("current_line", 1.0, END)
    textpad.tag_add("current_line", "insert linestart", "insert lineend+1c")
    textpad.after(100, update_highlight)

def remove_highlight():
    textpad.tag_remove("current_line", 1.0, END)

def update_highlight():
    textpad.tag_configure("current_line", background = "lavender")
    check = highlight.get()
    if not check:
       remove_highlight()
       
    else:
       highlight_line()
       
def show_line_number(event = NONE):
    global sidebar
    lines = ''
    if show_lines.get(): 
        current_line, current_column = textpad.index('end-1c').split('.')
        lines = '\n'.join(map(str, range(1, int(current_line))))
    sidebar.config(text = lines, anchor = 'nw')
    
    
def Environment():
    environment = Toplevel(root)
    environment.geometry('800x400')
    environment.title('Environment Settings')
   
    def sampleFont():
       global sFont
       Sfont = combobox1.getcurselection()
       sFont = ''.join(Sfont)
       Font.config(font = sFont)
       
    def backgroundColor():
       global bColor
       bcolor = combobox2.getcurselection()
       bColor = ''.join(bcolor)
       color.config(bg = bColor)
       
    def foregroundColor():
       global fColor
       fcolor = combobox3.getcurselection()
       fColor = ''.join(fcolor)
       Color.config(bg = fColor)
       
    def fontSize():
       global fSize
       fsize = combobox4.getcurselection()
       fSize = ''.join(fsize)
       
    def saveButton():
       global bColor, fColor, sFont, fSize
       textpad.config(bg = bColor, fg = fColor, font = (sFont,fSize))
       environment.destroy()
    
    Font = Label(environment, text = 'Sample Text', relief = GROOVE, padx = 60, pady = 40, bg ='snow')
    Font.grid(row = 0, column = 0, padx = 10, pady = 10)
    fonts = list(tkFont.families())
    fonts.sort()
    combobox1 = Pmw.ScrolledListBox(environment, label_text = 'Chose font :', listbox_selectmode = SINGLE, items = fonts, labelpos = NW, listbox_height = 5, vscrollmode = 'dynamic', hscrollmode = 'dynamic', selectioncommand = sampleFont, dblclickcommand = sampleFont, usehullsize = 1, hull_width = 200, hull_height = 200)
    combobox1.grid(row = 2, column = 0, padx = 10, pady = 10)
    
    color = Label(environment, bg = 'snow', relief = GROOVE, padx = 40, pady = 20)
    color.grid(row = 0, column = 3, padx = 10, pady = 10)    
    Bcolors = ('gainsboro', 'snow', 'antique white', 'peach puff', 'navajo white', 'alice blue', 'dark slate gray', 'slate gray', 'navy', 'cornflower blue', 'medium blue', 'royal blue', 'blue', 'deep sky blue', 'sky blue',
               'cyan', 'dark green', 'sea green', 'pale green', 'lawn green', 'lime green', 'khaki', 'yellow', 'gold', 'salmon', 'orange', 'coral', 'tomato', 'red', 'pink', 'maroon', 'purple')
    combobox2 = Pmw.ScrolledListBox(environment, label_text = 'Background Colour :', listbox_selectmode = SINGLE, items = Bcolors, labelpos = NW, listbox_height = 5, vscrollmode = 'dynamic', hscrollmode = 'dynamic', selectioncommand = backgroundColor, dblclickcommand = backgroundColor , usehullsize = 1, hull_width = 200, hull_height = 200)
    combobox2.grid(row = 2, column = 3, padx = 10, pady = 10)
    
    Color = Label(environment, bg = 'gray1', relief = GROOVE, padx = 40, pady = 20)
    Color.grid(row = 0, column = 6, padx = 10, pady = 10)
    Fcolors = ('gainsboro', 'snow', 'antique white', 'peach puff', 'navajo white', 'alice blue', 'dark slate gray', 'slate gray', 'navy', 'cornflower blue', 'medium blue', 'royal blue', 'blue', 'deep sky blue', 'sky blue',
               'cyan', 'dark green', 'sea green', 'pale green', 'lawn green', 'lime green', 'khaki', 'yellow', 'gold', 'salmon', 'orange', 'coral', 'tomato', 'red', 'pink', 'maroon', 'purple')
    combobox3 = Pmw.ScrolledListBox(environment, label_text = 'Foreground Colour :', listbox_selectmode = SINGLE, items = Fcolors, labelpos = NW, listbox_height = 5, vscrollmode = 'dynamic', hscrollmode = 'dynamic', selectioncommand = foregroundColor, dblclickcommand = foregroundColor, usehullsize = 1, hull_width = 200, hull_height = 200)
    combobox3.grid(row = 2, column = 6, padx = 10, pady = 10)
    
    size = ('8', '10', '12', '14', '16', '18', '20', '22', '24', '26', '28', '36', '48', '60', '72')
    combobox4 = Pmw.ScrolledListBox(environment, label_text = 'Font Size :', listbox_selectmode = SINGLE, items = size, labelpos = NW, listbox_height = 5, vscrollmode = 'dynamic', hscrollmode = 'dynamic', selectioncommand = fontSize, dblclickcommand = fontSize, usehullsize = 1, hull_width = 100, hull_height = 200)
    combobox4.grid(row = 2, column = 9, padx = 10, pady = 10)
    
    save = Button(environment, relief = RAISED, text = 'Save changes', command = saveButton)
    save.grid(row = 4, column = 3, padx = 30, pady = 10)
    cancel = Button(environment, relief = RAISED, text = 'Cancel', command = environment.destroy)
    cancel.grid(row = 4, column = 6, pady = 10)
    
    environment.mainloop()
    
    
def About():
  Pmw.aboutversion('1.0')
  Pmw.aboutcontact(
        'For any query about this application refer to the following contact: \n'+
        'Email- ritikakumari1302@gmail.com \n'+
        'Github profile- https://github.com/riti1302'
                  )  
  about = Pmw.AboutDialog(root)
  
def Help():
   help = Pmw.MessageDialog(root, title = 'Help', defaultbutton = 0, buttons = ('OK', 'Cancel'), message_text = 'For any help associated with the text editor refer to my github profile- "https://github.com/riti1302"')
   help.activate()
   
def Exit():
    if tkMessageBox.askokcancel("Quit", "Do you really want to quit?"):
        root.destroy()
root.protocol('WM_DELETE_WINDOW',Exit)

   

#Shortcut Buttons
balloon = Pmw.Balloon(root)
icons = ['New', 'Open', 'Save', 'Close', 'Close_All', 'Select_All', 'Cut', 'Copy', 'Paste', 'Undo', 'Redo', 'Search', 'About']
ShortcutBar = Frame(root, bg = 'snow')

for i, icon in enumerate(icons):
   Image = PhotoImage(file = 'Icons/'+icon+'.gif')
   cmd = eval(icon)
   ShortcutButton = Button(ShortcutBar, image = Image, relief = FLAT, bg = 'snow', command = cmd)  
   balloon.bind(ShortcutButton, icon)
   ShortcutButton.image = Image
   ShortcutButton.pack(side=LEFT)
ShortcutBar.pack(fill = X)

#MenuBar
######################################################################

menubar = Menu(root)
#File
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="New", accelerator ='Ctrl+N', compound = LEFT, underline = 1, command= New)
filemenu.add_command(label="Open", accelerator ='Ctrl+O', compound = LEFT, underline=0, command= Open)
filemenu.add_command(label="Save", accelerator = 'Ctrl+S', compound = LEFT, underline = 0, command= Save)
filemenu.add_command(label="Save As..", accelerator = 'Ctrl+Alt+S', compound = LEFT, command=saveas)
filemenu.add_separator()
filemenu.add_command(label="Exit", accelerator = 'Alt+F4', compound = LEFT, command= root.quit)
menubar.add_cascade(label="File", menu= filemenu)


#Edit
editmenu = Menu(menubar, tearoff=0)
editmenu.add_command(label="Undo", accelerator = 'Ctrl+Z', compound = LEFT, command= Undo)
editmenu.add_command(label="Redo", accelerator = 'Ctrl+Y', compound = LEFT, command= Redo)
editmenu.add_separator()
editmenu.add_command(label="Cut", accelerator = 'Ctrl+X', compound = LEFT, command= Cut)
editmenu.add_command(label="Copy", accelerator = 'Ctrl+C', compound = LEFT, command= Copy)
editmenu.add_command(label="Paste", accelerator = 'Ctrl+V', compound = LEFT, command= Paste)
editmenu.add_command(label="Select All", accelerator = 'Ctrl+A', compound = LEFT, command= Select_All)
editmenu.add_command(label="Delete", accelerator = 'DEL', compound = LEFT)
menubar.add_cascade(label="Edit", menu= editmenu)


#View
show_lines = IntVar()
show_lines.set(1)
highlight = IntVar()

viewmenu = Menu(menubar, tearoff=0)
viewmenu.add_checkbutton(label = "Show number of lines", variable = show_lines)
viewmenu.add_checkbutton(label = "Highlight current line", variable = highlight, command = update_highlight)
viewmenu.add_separator()
viewmenu.add_command(label="Environment settings", command= Environment)
menubar.add_cascade(label="View", menu= viewmenu)


#About
aboutmenu = Menu(menubar, tearoff=0)
aboutmenu.add_command(label="About", compound = LEFT, command= About)
aboutmenu.add_separator()
aboutmenu.add_command(label="Help", compound = LEFT, command= Help)
menubar.add_cascade(label="Help", menu= aboutmenu)

#Display the menu
root.config(menu= menubar)

####################################################################################

notebook = Pmw.NoteBook(root, pagemargin = 2, borderwidth = 1)

def TextPad():
 global number, Page, textpad, sidebar
 number = number + 1
 Page = notebook.add('Untitled %i' %number)

 textpad = Text(Page, wrap = NONE, undo = True) 
 sidebar = Label(textpad, bg = 'snow3', width = 5)
 sidebar.pack(side = LEFT, fill = Y)
   
 verticalscroll = Scrollbar(textpad, orient = VERTICAL, command = textpad.yview)
 horizontalscroll = Scrollbar(textpad, relief = RAISED, orient = HORIZONTAL, command = textpad.xview)
 verticalscroll.pack(side = RIGHT, fill = Y)
 horizontalscroll.pack(side = BOTTOM, fill = X)

 textpad.tag_configure('margin', lmargin1 = 45)
 textpad.insert('1.0', ' \n', 'margin')
 textpad.configure(yscrollcommand = verticalscroll.set, xscrollcommand = horizontalscroll.set)
 textpad.pack(expand = YES, fill = BOTH)
 textpad.bind("<Any-KeyPress>", show_line_number)
 notebook.selectpage('Untitled %i' %number)
 notebook.pack(pady = 5, fill = BOTH, expand = 1)
   
 
root.mainloop() 