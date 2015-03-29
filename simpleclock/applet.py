from rox import g, applet

class Applet(applet.Applet):

    def position_popup_window(self, window):
        x,y,__ = self.position_menu(window)
        window.move(x,y)

    def get_panel_orientation(self):
        pos = self.socket.property_get('_ROX_PANEL_MENU_POS', 'STRING', False)
        if pos: pos = pos[2]
        if pos:
            side = pos.split(',')[0]
        else:
            side = None
        return side
