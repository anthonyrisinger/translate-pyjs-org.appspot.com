
class Video(Media):

    def __init__(self, src=None, **kwargs):
        print "create object"
        obj = DOM.createElement("OBJECT")
        DOM.setAttribute(obj, "TYPE", "application/x-mplayer2")
        #DOM.setAttribute(obj, "type", "application/x-oleobject")
        DOM.setAttribute(obj, "classid",
                                #"CLSID:22D6F312-B0F6-11D0-94AB-0080C74C7E95")
                                "CLSID:6BF52A52-394A-11d3-B153-00C04F79FAA6")
        print "set element"
        self.setElement(obj)

        print "widget init"
        Media.__init__(self, **kwargs)

        print "setSrc"
        if src:
            self.setSrc(src)

        #self.setID("MediaPlayer")

        self.dispparam = DOM.createElement("PARAM")
        DOM.setAttribute(self.dispparam, "name", "ShowDisplay")
        DOM.setBooleanAttribute(self.dispparam, "VALUE", "false")
        self.getElement().appendChild(self.dispparam)

    def setSrc(self, src):
        print "setSrc", src
        #self.srcparam = DOM.createElement("PARAM")
        #DOM.setAttribute(self.srcparam, "name", "FileName")
        #DOM.setAttribute(self.srcparam, "VALUE", src)
        #self.getElement().appendChild(self.srcparam)
        obj = self.getElement()
        DOM.setAttribute(obj, "URL", src)
        #obj.URL = src

    def setControls(self, controls):
        print "setControls", controls
        self.ctrlparam = DOM.createElement("PARAM")
        DOM.setAttribute(self.ctrlparam, "name", "ShowControls")
        DOM.setBooleanAttribute(self.ctrlparam, "VALUE",
            controls and "true" or "false")
        self.getElement().appendChild(self.ctrlparam)

    def setStatusbar(self, statusbar):
        print "setstatus", statusbar
        self.statparam = DOM.createElement("PARAM")
        DOM.setAttribute(self.statparam, "name", "ShowStatusBar")
        DOM.setBooleanAttribute(self.statparam, "VALUE",
            statusbar and "true" or "false")
        self.getElement().appendChild(self.statparam)

    def setLoop(self, autorewind):
        print "autorewind", autorewind
        self.loopparam = DOM.createElement("PARAM")
        DOM.setAttribute(self.loopparam, "name", "autorewind")
        DOM.setBooleanAttribute(self.loopparam, "VALUE", 
            autorewind and "true" or "false")
        self.getElement().appendChild(self.loopparam)

    def setAutoplay(self, autostart):
        print "autoplay", autostart
        self.playparam = DOM.createElement("PARAM")
        DOM.setAttribute(self.playparam, "name", "autostart")
        DOM.setBooleanAttribute(self.playparam, "VALUE", 
            autostart and "true" or "false")
        self.getElement().appendChild(self.playparam)

