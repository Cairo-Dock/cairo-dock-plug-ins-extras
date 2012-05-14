try:
    import pynotify

    def doUserAlert(master, message, time):
            """
            Notify user of alerts
            """
            if master.usePynotify:
                n = pynotify.Notification(message)
                n.show()
            else:
                master.ShowDialog(message,time)
except ImportError:

    def doUserAlert(master, message, time):
            """ 
            Notify user of alerts
            """
            master.ShowDialog(message,time)

