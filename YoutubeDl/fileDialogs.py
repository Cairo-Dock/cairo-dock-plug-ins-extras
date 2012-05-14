try:
    import Tkinter, tkFileDialog
    def openUrlFilename(initialDirectory):

        rootDialog = Tkinter.Tk()

        # define options for opening or saving a file
        file_opt = options = {}
        options['defaultextension'] = 'txt' # couldn't figure out how this works
        options['filetypes'] = [('all files', '.*'), ('text files', '.txt')]
        options['initialdir'] = initialDirectory
        #options['initialfile'] = initialDirectory
        options['title'] = 'Please select a url list file to open'
        options['parent'] = rootDialog
        #fileName = tkFileDialog.askopenfilename(parent=rootDialog,title='Please select file to open')
        fileName = tkFileDialog.askopenfilename(**file_opt)
        rootDialog.destroy()
        return fileName

    def saveUrlFilename():
        rootDialog = Tkinter.Tk()
        fileName = tkFileDialog.asksaveasfilename(parent=rootDialog,title='Please select file to open')
        rootDialog.destroy()
        return fileName

except ImportError:
    def openUrlFilename():
        return None
    def saveUrlFilename():
        return None
    #from PopupDialogTypes import *

    #def openUrlFilename(master):
        #master.PopupDialog( {"message" : "Enter filename to open:",  
            #"buttons" : "ok;cancel",  
            #"icon" : "gtk-stock-edit"},  
            #{"widget-type" : "text-entry",  
            #"visible" : False} )
        #master.currentDialog = PopupDialogTypes.infoDialog
        #return None

    #def saveUrlFilename(master):
        #master.PopupDialog( {"message" : "Enter filename to open:",  
            #"buttons" : "ok;cancel",  
            #"icon" : "gtk-stock-edit"},  
            #{"widget-type" : "text-entry",  
            #"visible" : False} )
        #master.currentDialog = PopupDialogTypes.infoDialog
        #return None
