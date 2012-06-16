#!/usr/bin/env python

#try the gtk method of getting the clipboard contents first
try:
    import gtk

    def getClipboardText():
        clipboard = gtk.clipboard_get()
        return clipboard.wait_for_text()
except:
    #next try the tkinter method of getting the clipboard contents
    try:
        import Tkinter
        def getClipboardText():
            root = Tkinter.Tk()
            root.withdraw() # Hide the main window (optional)
            return root.clipboard_get()
    except:
        #finally try the xclip method of getting the clipboard contents
        try:
            import subprocess
            def getClipboardText():
                try:
                    p = subprocess.Popen(["xclip","-out","-selection","clipboard"],stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=False)
                    clipText, errors = p.communicate()
                    return clipText
                except:
                    #If xclip fails return nothing
                    return ""
        except:
            #If all fails then return nothing
            def getClipboardText():
                return ""
