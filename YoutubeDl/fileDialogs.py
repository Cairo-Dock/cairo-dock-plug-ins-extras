try:
    import pygtk
    pygtk.require('2.0')

    import gtk
    def openUrlFilename(initialDirectory):
        # Check for new pygtk: this is new class in PyGtk 2.4
        if gtk.pygtk_version < (2,3,90):
           print "PyGtk 2.3.90 or later required for this example"
           raise SystemExit

        dialog = gtk.FileChooserDialog("Open..",
                                       None,
                                       gtk.FILE_CHOOSER_ACTION_OPEN,
                                       (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                        gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        dialog.set_default_response(gtk.RESPONSE_OK)

        filter = gtk.FileFilter()
        filter.set_name("Text Files")
        filter.add_pattern("*.txt")
        dialog.add_filter(filter)

        filter = gtk.FileFilter()
        filter.set_name("All files")
        filter.add_pattern("*")
        dialog.add_filter(filter)

        dialog.set_current_folder(initialDirectory)
        response = dialog.run()
        if response == gtk.RESPONSE_OK:
            print "OK pressed: " + dialog.get_filename(), 'selected'
            fileName = dialog.get_filename()
        elif response == gtk.RESPONSE_CANCEL:
            print "Cancel pressed: " + dialog.get_filename(), 'selected'
            #print 'Closed, no files selected'
            fileName = ''
        dialog.destroy()
        return fileName
    def saveUrlFilename(initialDirectory):
        # Check for new pygtk: this is new class in PyGtk 2.4
        if gtk.pygtk_version < (2,3,90):
           print "PyGtk 2.3.90 or later required for this example"
           raise SystemExit

        dialog = gtk.FileChooserDialog("Save..",
                                       None,
                                       gtk.FILE_CHOOSER_ACTION_SAVE,
                                       (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                        gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        dialog.set_default_response(gtk.RESPONSE_OK)

        filter = gtk.FileFilter()
        filter.set_name("Text Files")
        filter.add_pattern("*.txt")
        dialog.add_filter(filter)

        filter = gtk.FileFilter()
        filter.set_name("All files")
        filter.add_pattern("*")
        dialog.add_filter(filter)

        dialog.set_current_folder(initialDirectory)
        response = dialog.run()
        if response == gtk.RESPONSE_OK:
            print "OK pressed: " + str(dialog.get_filename()), 'selected'
            fileName = dialog.get_filename()
        elif response == gtk.RESPONSE_CANCEL:
            print "Cancel pressed: " + str(dialog.get_filename()), 'selected'
            #print 'Closed, no files selected'
            fileName = ''
        dialog.destroy()
        return fileName
#except ImportError:
except:
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
            fileName = tkFileDialog.asksaveasfilename(**file_opt)
            rootDialog.destroy()
            return fileName

    #except ImportError:
    except:
        def openUrlFilename(initialDirectory):
            return None
        def saveUrlFilename(initialDirectory):
            return None
