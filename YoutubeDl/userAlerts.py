try:
    import pynotify

    def doUserAlert(master, message, time):
            """
            Notify user of alerts
            """
            if master.usePynotify and pynotify.init('YoutubeDl'):
                n = pynotify.Notification(message)
                n.show()
            else:
                master.icon.ShowDialog(message,time)
except ImportError:

    def doUserAlert(master, message, time):
            """ 
            Notify user of alerts
            """
            master.icon.ShowDialog(message,time)

