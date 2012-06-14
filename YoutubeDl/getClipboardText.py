#!/usr/bin/env python

#try the gtk method of getting the clipboard contents first
try:
    import gtk

    def getClipboardText():
        clipboard = gtk.clipboard_get(gtk.gdk.SELECTION_PRIMARY)      # selected with the mouse
        if not clipboard:                                             # nothing was selected with mouse
            clipboard = gtk.clipboard_get()
        else:
            text = clipboard.wait_for_text()
            if text.find("youtube.com/watch") == -1:
                clipboard = gtk.clipboard_get()
        text = clipboard.wait_for_text()
        if text.find("youtube.com/watch") == -1:
            text = ""
        return text
except:
    #next try the tkinter method of getting the clipboard contents
    try:
        import Tkinter
        def getClipboardText():
            root = Tkinter.Tk()
            root.withdraw() # Hide the main window (optional)
            text = root.selection_get()
            if (not text) or (text.find("youtube.com/watch") == -1):
                text = root.clipboard_get()
                if (not text) or (text.find("youtube.com/watch") == -1):
                    text = ""
            return text
    except:
        #finally try the xclip method of getting the clipboard contents
        try:
            import subprocess
            def getClipboardText():
                try:
                    p = subprocess.Popen(["xclip","-out","-selection","clipboard"],stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=False)
                    clipText, errors = p.communicate()
                    if (not clipText) or (clipText.find("youtube.com/watch") == -1):
                        p = subprocess.Popen(["xclip","-out","-selection","primary"],stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=False)
                        clipText, errors = p.communicate()
                        if (not clipText) or (clipText.find("youtube.com/watch") == -1):
                            clipText = ""
                    return clipText
                except:
                    #If xclip fails return nothing
                    return ""
        except:
            #If all fails then return nothing
            def getClipboardText():
                return ""
