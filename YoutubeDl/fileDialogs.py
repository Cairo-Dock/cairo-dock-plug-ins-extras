try:
    import Tkinter, tkFileDialog
    def openUrlFilename(initialDirectory):

        rootDialog = Tkinter.Tk()

        # define options for opening or saving a file
        file_opt = options = {}
        options['defaultextension'] = 'txt' # couldn't figure out how this works
        options['filetypes'] = [('text files', '.txt'), ('all files', '.*')]
        options['initialdir'] = initialDirectory
        options['title'] = 'Please select a url list file to open'
        options['parent'] = rootDialog
        fileName = tkFileDialog.askopenfilename(**file_opt)
        rootDialog.destroy()
        return fileName

    def saveUrlFilename(initialDirectory):
        rootDialog = Tkinter.Tk()
        file_opt = options = {}
        options['defaultextension'] = 'txt' # couldn't figure out how this works
        options['filetypes'] = [('text files', '.txt'), ('all files', '.*')]
        options['initialdir'] = initialDirectory
        options['title'] = 'Please select a url list file to save'
        options['parent'] = rootDialog
        fileName = tkFileDialog.askopenfilename(**file_opt)
        rootDialog.destroy()
        return fileName

except ImportError:
    def openUrlFilename(initialDirectory):
        return None
    def saveUrlFilename(initialDirectory):
        return None
