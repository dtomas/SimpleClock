# SimpleClock by Dennis Tomas, based on:
# MiniClock v. 2.0.0 - a very very simple clock
# Copyright (C) 2005  Edoardo Spadolini <pedonzolo@email.it>

import rox, time, sys, os, gobject
from rox import g, options, processes, InfoWin, filer

from pretty_time import rough_time
from calendar_window import CalendarWindow
from applet import Applet

rox.setup_app_options("SimpleClock", "Options.xml", "dtomas")

icon_theme = g.icon_theme_get_default()

o_set_prog = options.Option('set_program', "gksu time-admin")
o_line = options.Option('line', "%X")
o_tip = options.Option('tip', "%c")
o_textual_line = options.Option('textual_line', False)
o_textual_tip = options.Option('textual_tip', False)

rox.app_options.notify()

icon_size, ign = g.icon_size_lookup(g.ICON_SIZE_MENU)

class Clock:
    def __init__(self):
        self.calendar_window = None
        
        self.line_str = ''
        self.tip_str = ''

        self.tooltip = g.Tooltips()
        self.line_label = g.Label("")

        self.set_border_width(5)
        self.add(self.line_label)
        
        self.menu = g.Menu()
        
        item = g.ImageMenuItem(g.STOCK_HELP)
        item.connect("activate", self.help)
        self.menu.append(item)
        
        item = g.ImageMenuItem(g.STOCK_DIALOG_INFO)
        item.connect("activate", self.about)
        self.menu.append(item)
        
        self.menu.append(g.SeparatorMenuItem())

        item = g.ImageMenuItem(_("Set Time"))
        try:
            pixbuf = icon_theme.load_icon("clock", icon_size, 0)
        except:
            pixbuf = g.gdk.pixbuf_new_from_file(os.path.join(rox.app_dir,
                                                            'clock.png'))
        if pixbuf.get_width() != icon_size:
            pixbuf = pixbuf.scale_simple(icon_size, icon_size, g.gdk.INTERP_HYPER)
        item.get_image().set_from_pixbuf(pixbuf)
        item.connect("activate", self.set_time)
        self.menu.append(item)

        item = g.ImageMenuItem(g.STOCK_PREFERENCES)
        item.connect("activate", self.options)
        self.menu.append(item)
        
        self.menu.append(g.SeparatorMenuItem())
        
        item = g.ImageMenuItem(g.STOCK_QUIT)
        item.connect("activate", self.quit)
        self.menu.append(item)
        
        self.menu.show_all()

        rox.app_options.add_notify(self.options_changed)
        
        self.add_events(g.gdk.BUTTON_PRESS_MASK)
        self.connect("button-press-event", self.button_press)

        self.connect("destroy", self.destroyed)
        
        self.update_clock()
        self.timeout = gobject.timeout_add(1000, self.update_clock)
        
        self.show_all()

    def update_clock(self):
        if o_textual_line.int_value:
            show_time = (o_line.value == '%X' or o_line.value == '%c')
            show_date = (o_line.value == '%x' or o_line.value == '%c')
            line_str = rough_time(time.time(), show_time, show_date)
        else:
            line_str = time.strftime(o_line.value)
        
        if o_textual_tip.int_value:
            show_time = (o_tip.value == '%X' or o_tip.value == '%c')
            show_date = (o_tip.value == '%x' or o_tip.value == '%c')
            tip_str = rough_time(time.time(), show_time, show_date)
        else:
            tip_str = time.strftime(o_tip.value)

        if line_str != self.line_str:
            self.line_label.set_text(line_str)
            self.line_str = line_str
            
        if tip_str != self.tip_str:
            self.tooltip.set_tip(self, tip_str)
            self.tip_str = tip_str
        return True

    def destroyed(self, window):
        gobject.source_remove(self.timeout)

    def button_press(self, window, event):
        if event.button == 3:
            self.menu.popup(None, None, None, event.button, event.time)
        elif event.button == 1:
            self.show_calendar()
            
    def show_calendar(self):
        if self.calendar_window:
            self.calendar_window.destroy()
            return
        self.calendar_window = CalendarWindow()
        self.calendar_window.connect("realize", self._calendar_window_realized)
        self.calendar_window.connect("destroy", self._calendar_window_destroyed)
        self.calendar_window.show_all()
        
    def _calendar_window_destroyed(self, window):
        self.calendar_window = None
        
    def _calendar_window_realized(self, window):
        self.position_popup_window(self.calendar_window)
        
    def position_popup_window(self, window):
        x,y = self.window.get_origin()
        i,i, w,h, i = self.window.get_geometry()
        window.move(x,y+h)

    def options_changed(self):
        self.update_clock()

    def options(self, item):
        rox.edit_options()

    def about(self, item):
        InfoWin.infowin('SimpleClock')
        
    def help(self, item):
        filer.open_dir(os.path.join(rox.app_dir, 'Help'))

    def quit(self, item):
        if rox.confirm(_("Really quit the SimpleClock?"), g.STOCK_QUIT):
            self.destroy()
    
    def set_time(self, item):
        try:
            rox.processes.PipeThroughCommand(o_set_prog.value , None, None).wait()
        except:
            pass

    def mainloop(self):
        rox.mainloop()

class ClockWindow(rox.Window, Clock):
    def __init__(self):
        rox.Window.__init__(self)
        Clock.__init__(self)

class ClockApplet(Applet, Clock):
    def __init__(self, xid):
        Applet.__init__(self, xid)
        self.set_name("SimpleClockPanelApplet")
        Clock.__init__(self)

    def button_press(self, window, event):
        if event.button == 3:
            self.menu.popup(None, None, self.position_menu, event.button, event.time)
        elif event.button == 1:
            self.show_calendar()
