import gtk

class CalendarWindow(gtk.Window):
    
    def __init__(self):
        gtk.Window.__init__(self, gtk.WINDOW_POPUP)
        self.stick()
        self.box = gtk.Frame()
        self.add(self.box)
        self.calendar = gtk.Calendar()
        self.box.add(self.calendar)
