# Copyright (C) 2010 Luke Kenneth Casson Leighton <lkcl@lkcl.net>
# Copyright (C) 2011 Janjaap Bos <janjaapbos@gmail.com>

from pyjamas.builder.XMLFile import XMLFile
from pyjamas import Factory
from pyjamas import ui
from pyjamas.ui.MultiListener import MultiListener
from pyjamas.HTTPRequest import HTTPRequest
from pyjamas.ui.Tooltip import TooltipListener


# All event listeners with a tuple that comprises of the listener add 
# function and the additional (to 'self') parameters that are expected 
# for the listener. E.g., def onClick(self, sender): ...
# See also pyjamas.ui.MultiListener.MultiListener.combinations
eventListeners = dict(
    onClick = ("addClickListener", "sender"),
    onDoubleClick = ("addDoubleClickListener", "sender"),
    onChange = ("addChangeListener", "sender"),
    onFocus = ("addFocusListener", "sender"),
    onLostFocus = ("addFocusListener", "sender"),
    onLoad = ("addLoadListener", "sender"),
    onError = ("addLoadListener", "sender"),
    onKeyDown = ("addKeyboardListener", "sender", "keycode", "modifiers"),
    onKeyUp = ("addKeyboardListener", "sender", "keycode", "modifiers"),
    onKeyPress = ("addKeyboardListener", "sender", "keycode", "modifiers"),
    onMouseDown = ("addMouseListener", "sender", "x", "y"),
    onMouseUp = ("addMouseListener", "sender", "x", "y"),
    onMouseMove = ("addMouseListener", "sender", "x", "y"),
    onMouseEnter = ("addMouseListener", "sender"),
    onMouseLeave = ("addMouseListener", "sender"),
    onScroll = ("addScrollListener", "sender", "row", "col"),
    onCellClicked = ("addTableListener", "sender", "row", "col"),
    onTabSelected = ("addTabListener", "sender", "tabIndex"),
    onBeforeTabSelected = ("addTabListener", "sender", "tabIndex"),
    onTreeItemSelected = ("addTreeListener", "sender"),
        )

class BuilderState(object):
    def __init__(self, builder, eventTarget):
        self.builder = builder
        self.eventTarget = eventTarget

class Builder(object):

    def __init__(self, text=None):
        self.builder_text = None
        self.setText(text)

    def setText(self, text):
        if text is None:
            self.widgets_by_name = {}
            self.widget_instances = {}
            self.widget_order = {}
            self.widgets_by_class = {}
            self.properties = None
            self.components = None
            self.builder_text = None
            return

        text = str(text) # XMLFile only accepts str not unicode!
        if text == self.builder_text: # don't redo the xml file if same
            return

        self.builder_text = text

        self.widgets_by_name = {}
        self.widget_instances = {}
        self.widget_order = {}
        self.widgets_by_class = {}
        self.properties, self.components = XMLFile(text).parse()

    def createInstance(self, instancename,
                       eventTarget=None, targetItem=None, index=None):

        widget_instances = {}
        widgets_by_name = {}
        widgets_by_class = {}
        widget_order = []

        def addItem(comp, props, childs, parentInstance, eventTarget):
            klsname = comp['name']
            modname = comp.get('module')
            if modname is None:
                modname = '.'.join(["pyjamas.ui", klsname])
            kls = Factory.lookupClass('.'.join([modname, klsname]))

            args = {}
            wprops = {}
            if props.has_key("common"):
                wprops.update(props['common'])
            if props.has_key("widget"):
                wprops.update(props['widget'])
            for n in kls._getProps():
                name = n[ui.PROP_NAME]
                if not wprops.has_key(name):
                    continue
                fname = n[ui.PROP_FNAM]
                if wprops[name] == '':
                    continue
                args[fname] = wprops[name]

            # create item with properties including weird ones
            # which can't fit into the name value structure
            item = kls(**args)
            if hasattr(item, "_setWeirdProps"):
                item._setWeirdProps(wprops, BuilderState(self, eventTarget))

            tooltip = wprops.get('tooltip')
            if tooltip is not None:
                item.addMouseListener(TooltipListener(tooltip))

            identifier = comp['id']
            widget_order.append(identifier)
            widgets_by_name[identifier] = klsname
            widget_instances[identifier] = item
            l = widgets_by_class.get(klsname, [])
            l.append(identifier)
            widgets_by_class[klsname] = l

            #if parentInstance is not None:
            #    context = parentInstance.getIndexedChild(comp['index'])
            #    context.add(item.componentInstance)
            for (index, child) in enumerate(childs):
                if not child[0].has_key("type") or child[0]["type"] is None:
                    continue
                childitem = addItem(child[0], child[1], child[2], item,
                                    eventTarget)
                if childitem is None:
                    continue
                print "childitem", childitem
                item.addIndexedItem(child[0]["index"], childitem)
                if not "elements" in props:
                    props["elements"] = {}
                if not index in props["elements"]:
                    props["elements"][index] = {}

                elemprops = props['elements'][index]
                print "elemprops", childitem, item, elemprops
                item.setElementProperties(childitem, elemprops)

                # add child (by name) to item
                cname = child[0]["id"] 
                setattr(item, cname, childitem)

            # make the event target the recipient of all events
            if eventTarget is not None and props.has_key("events"):
                added_already = []
                #print props["events"]
                for listener_name, listener_fn in props["events"].items():
                    if listener_name in added_already or not listener_fn:
                        continue
                    args = {}
                    args[listener_name] = listener_fn
                    fname = eventListeners[listener_name][0]
                    listener = MultiListener(eventTarget, **args)
                    setattr(item, "_%sListener" % fname, listener)
                    #print "add listener", listener_name, fname
                    listen_add_fn = getattr(item, fname)
                    listen_add_fn(listener)
            return item

        for frame, props, childs in self.components:
            if frame["id"] != instancename:
                continue
            if index is not None:
                frame["index"] = index
            item = addItem(frame, props, childs, targetItem, eventTarget)
            #left = frame.get("left")
            #top = frame.get("top")
            #if left is not None and top is not None:
            #    item.applicationVO.frame.setPopupPosition(left, top)
            #if frame.get("visible", True):
            #    item.show()
            #else:
            #    item.hide()

            self.widget_instances[instancename] = widget_instances
            self.widgets_by_name[instancename] = widgets_by_name
            self.widgets_by_class[instancename] = widgets_by_class
            self.widget_order[instancename] = widget_order

            return item
        return None


class HTTPUILoader:
    def __init__(self, app):
        self.app = app

    def load(self, xml_file):
        HTTPRequest().asyncGet(xml_file, self)

    def onCompletion(self, text):
        self.app.onUILoaded(text)

    def onError(self, text, code):
        self.app.onUILoadError(text, code)

    def onTimeout(self, text):
        self.app.onUILoadingTimeout(text)


