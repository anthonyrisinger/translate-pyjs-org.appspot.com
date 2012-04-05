
class Video(Media):

    def __init__(self, src=None, **kwargs):
        obj = DOM.createElement("OBJECT")
        DOM.setAttribute(obj, "TYPE", "application/x-mplayer2")
        self.setElement(obj)

        if src:
            self.setSrc(src)

        Media.__init__(self, **kwargs)

        obj = self.getElement().object.ShowDisplay = False

    def setSrc(self, src):
        obj = self.getElement().object.FileName = src

    def setControls(self, controls):
        obj = self.getElement().object.ShowControls = \
                                    controls and "true" or "false"

    def setStatusbar(self, statusbar):
        obj = self.getElement().object.ShowStatusBar = \
                                    statusbar and "true" or "false"

    def setLoop(self, autorewind):
        obj = self.getElement().object.autorewind = \
                                    autorewind and "true" or "false"

    def setAutoplay(self, autostart):
        obj = self.getElement().object.autostart = \
                                    autostart and "true" or "false"

