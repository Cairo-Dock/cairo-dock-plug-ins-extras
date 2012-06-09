#!/usr/bin/env python
 
try:
    from Tkinter.junk import *
    import tkFont

    class  urlListEditor(Frame):

        def __init__(self,urlList):
            self.root = Tk()
            Frame.__init__(self)
            self.urlList = False
            self.root.title("Listbox Operations")
            self.root.rowconfigure(0, weight=1)
            self.root.columnconfigure(0, weight=1)

            RWidth=self.root.winfo_screenwidth()
            RHeight=self.root.winfo_screenheight()
            self.root.geometry("550x350+300+100")
            # create the listbox (note that size is in characters)
            myFont = tkFont.Font ( family="Courier",size=10)
            self.listbox1 = Listbox(self.root, width=50, height=6, font=myFont)
            self.listbox1.grid(row=0, column=0,rowspan=2, columnspan=2, sticky=N+S+E+W)
 
            # create a vertical scrollbar to the right of the listbox
            self.yscroll = Scrollbar(command=self.listbox1.yview, orient=VERTICAL)
            #self.yscroll.grid(row=0, column=1, sticky=N+S)
            self.yscroll.grid(row=0,rowspan=2, column=2, sticky=N+S)
            self.listbox1.configure(yscrollcommand=self.yscroll.set)
            # create a horizontal scrollbar to the bottom of the listbox
            self.xscroll = Scrollbar(command=self.listbox1.xview, orient=HORIZONTAL)
            self.xscroll.grid(row=2, column=0, columnspan=2, sticky=E+W)
            self.listbox1.configure(xscrollcommand=self.xscroll.set)
 
            # button to move a line up in the list box
            self.button1 = Button(self.root, text='Move Up', command=self.move_up)
            self.button1.grid(row=0, column=3, sticky=W+N)
            # button to move a line down in the list box
            self.button2 = Button(self.root, text='Move Down', command=self.move_down)
            #self.button2.grid(row=4, column=0, sticky=W)
            self.button2.grid(row=1, column=3, sticky=W+N)
            # button to delete a line from the listbox
            self.button3 = Button(self.root, text='Delete Selected', command=self.delete_item)
            #self.button3.grid(row=3, column=0, sticky=E)
            self.button3.grid(row=3, column=0,sticky=W+N)
            # button to commit changes and close
            self.button4 = Button(self.root, text='Commit Changes', command=self.save_list)
            #self.button4.grid(row=4, column=0, sticky=E)
            self.button4.grid(row=3, column=1,sticky=E+N)
 
            # left mouse click on a list item to display selection
            #self.listbox1.bind('<ButtonRelease-1>', self.get_list)
 
            for item in range(len(urlList)):
                tempString = ' -> '.join(urlList[item])
                self.listbox1.insert(END, tempString)

        def run(self):
            self.mainloop()
            return self.urlList

        def delete_item(self):
            """
            delete a selected line from the listbox
            """
            try:
                # get selected line index
                index = self.listbox1.curselection()[0]
                self.listbox1.delete(index)
            except IndexError:
                pass
 
        #def get_list(self,event):
            #"""
            #function to read the listbox selection
            #"""
            # get selected line index
            #index = self.listbox1.curselection()[0]

        def set_list(self,event):
            """
            insert an edited line from the entry widget
            back into the listbox
            """
            try:
                index = self.listbox1.curselection()[0]
                # delete old listbox line
                self.listbox1.delete(index)
            except IndexError:
                index = END

        def move_up(self):
            """
            function to sort listbox items case insensitive
            """
            try:
                index = self.listbox1.curselection()[0]
                if index > 0:
                    newindex = str(int(index) - 1)
                    self.listbox1.insert((int(index) - 1), self.listbox1.get(index))
                    # delete old listbox line
                    self.listbox1.delete(int(index)+1)
                    self.listbox1.select_set(int(index)-1)
                    #self.listbox1.yview(int(index)-1)
                else:
                    self.listbox1.select_set(0)
                    self.listbox1.yview(0)
            except IndexError:
                index = END

        def move_down(self):
            """
            function to sort listbox items case insensitive
            """
            try:
                index = self.listbox1.curselection()[0]
                if index < END:
                    self.listbox1.insert((int(index) + 2), self.listbox1.get(index))
                    # delete old listbox line
                    self.listbox1.delete(index)
                    self.listbox1.select_set(int(index)+1)
                    self.listbox1.yview(int(index)+1)
                else:
                    self.listbox1.select_set(END)
                    self.listbox1.yview(END)
            except IndexError:
                index = END

        def save_list(self):
            """
            save the current listbox contents to a file
            """
            self.urlList = list()
            # get a list of listbox lines
            temp_list = list(self.listbox1.get(0, END))
            for item in temp_list:
                tempItem = item.split(" -> ",1)
                self.urlList.append([tempItem[0].lstrip(),tempItem[1].lstrip()])
            self.root.destroy()

        def onClose():
            print "closing"
            self.root.destroy()
    
except ImportError:
    class  urlListEditor():
        def __init__(self,myUrlList):
            self.urlList = None

        def run(self):
            return self.urlList

if __name__ == "__main__":
    root=urlListEditor([['test','1'],['test','2'],['test','3']]).run()

