from rox import g, applet

class Applet(applet.Applet):

    def position_popup_window(self, window):
        x,y = self.window.get_origin()
        orientation = self.get_panel_orientation()
        i,i, w,h, i = self.window.get_geometry()
        i,i, win_w, win_h, i = window.window.get_geometry()
        if orientation == 'Top':
            y += h
        elif orientation == 'Bottom':
            y -= win_h
        elif orientation == 'Left':
            x += w
        elif orientation == 'Right':
            x -= win_w
        x = min(x, g.gdk.screen_width()-win_w)
        y = min(y, g.gdk.screen_height()-win_h)
        window.move(x,y)

    def get_panel_orientation(self):
        pos = self.socket.property_get('_ROX_PANEL_MENU_POS', 'STRING', False)
        if pos: pos = pos[2]
        if pos:
            side = pos.split(',')[0]
        else:
            side = None
        return side
