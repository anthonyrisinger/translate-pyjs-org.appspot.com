# Copyright 2006 James Tauber and contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
    DOM implements the core of Pjamas-Desktop, providing access to
    and management of the DOM model of the PyWebkitGtk window.
"""

import pyjd

if pyjd.is_desktop:
    from pyjamas.Window import onResize, onClosing, onClosed
    from __pyjamas__ import JS, doc, get_main_frame, wnd

    currentEvent = None

sCaptureElem = None
sEventPreviewStack = []

listeners = {}

from pyjamas.ui import Event
from pyjamas.ui.Event import (
    ONBLUR,
    ONCHANGE,
    ONCLICK,
    ONCONTEXTMENU,
    ONDBLCLICK,
    ONERROR,
    ONFOCUS,
    ONKEYDOWN,
    ONKEYPRESS,
    ONKEYUP,
    ONLOAD,
    ONLOSECAPTURE,
    ONMOUSEDOWN,
    ONMOUSEMOVE,
    ONMOUSEOUT,
    ONMOUSEOVER,
    ONMOUSEUP,
    ONSCROLL,
    ONINPUT
)


def get_listener(item):
    if item is None:
        return None
    if hasattr(item, "__instance__"):
        ret = listeners.get(item.__instance__)
    else:
        ret = listeners.get(hash(item))
    return ret


def set_listener(item, listener):
    if hasattr(item, "__instance__"):
        listeners[item.__instance__] = listener
    elif listener is None:
        listeners.pop(hash(item))
    else:
        listeners[hash(item)] = listener

# ugh, *spew*, *hurl* http://code.google.com/p/pyjamas/issues/detail?id=213
hack_timer_workaround_bug_button = None


def init():
    mf = get_main_frame()
    mf._addWindowEventListener("click", browser_event_cb)
    mf._addWindowEventListener("change", browser_event_cb)
    mf._addWindowEventListener("mouseout", browser_event_cb)
    mf._addWindowEventListener("mousedown", browser_event_cb)
    mf._addWindowEventListener("mouseup", browser_event_cb)
    mf._addWindowEventListener("resize", browser_event_cb)
    mf._addWindowEventListener("keyup", browser_event_cb)
    mf._addWindowEventListener("keydown", browser_event_cb)
    mf._addWindowEventListener("keypress", browser_event_cb)
    mf._addWindowEventListener("mousewheel", browser_event_cb)

def _init_testing():
    body = doc().getElementsByTagName("body")[0]
    mf._addEventListener(body, "click", cb)
    mf._addEventListener(body, "change", cb)
    mf._addEventListener(body, "mouseout", cb)
    mf._addEventListener(body, "mousedown", cb)
    mf._addEventListener(body, "mouseup", cb)
    mf._addEventListener(body, "mousemove", cb)
    mf._addEventListener(body, "resize", cb)
    mf._addEventListener(body, "keyup", cb)
    mf._addEventListener(body, "keydown", cb)
    mf._addEventListener(body, "keypress", cb)

def _dispatchWindowEvent(sender, evt, useCap):
    pass


def _dispatchEvent(sender, evt, useCap):

    if evt is None:
        evt = wnd().event
    else:
        try:
            sender = get_main_frame().gobject_wrap(sender) # webkit HACK!
            evt = get_main_frame().gobject_wrap(evt) # webkit HACK!
        except:
            pass
    listener = None
    curElem = sender

    #print "_dispatchEvent", sender, evt, evt.type
    cap = getCaptureElement()
    listener = get_listener(cap)
    if cap and (listener is not None):
        #print "capture _dispatchEvent", cap, listener
        dispatchEvent(evt, cap, listener)
        evt.stopPropagation()
        return

    while curElem and (get_listener(curElem) is None):
        #print "no parent listener", curElem, getParent(curElem)
        curElem = getParent(curElem)
    if curElem and getNodeType(curElem) != 1:
        curElem = None

    listener = get_listener(curElem)
    if listener is not None:
        dispatchEvent(evt, curElem, listener)


def _dispatchCapturedMouseEvent(evt):

    #print "dcmsev"
    if not _dispatchCapturedEvent(evt):
        return
    cap = getCaptureElement()
    listener = get_listener(cap)
    if cap and (listener is not None):
        dispatchEvent(evt, cap, listener)
        #print "dcmsev, stop propagation"
        evt.stopPropagation()


def _dispatchCapturedMouseoutEvent(evt):
    cap = getCaptureElement()
    #print "cap", evt, cap
    if cap is None:
        return
    #print "cap", evt, cap
    if eventGetToElement(evt):
        return
    #print "synthesise", cap
    #When the mouse leaves the window during capture, release capture
    #and synthesize an 'onlosecapture' event.
    setCapture(None)
    listener = get_listener(cap)
    if listener is None:
        return
    # this should be interesting...
    #print "lose capture synthesised"
    lcEvent = doc().createEvent('UIEvent')
    lcEvent.initUIEvent('losecapture', False, False, wnd(), 0)
    dispatchEvent(lcEvent, cap, listener)


def browser_event_cb(view, event, from_window):

    global sCaptureElem
    #print "sCaptureElem", sCaptureElem
    if event is None:
        event = wnd().event
    else:
        try:
            event = get_main_frame().gobject_wrap(event) # webkit HACK!
        except:
            pass

    #print "browser_event_cb", event
    et = eventGetType(event)
    #print "browser_event_cb", event, et
    if et == "resize":
        onResize()
        return
    if et == 'mouseout':
        #print "mouse out", event
        _dispatchCapturedMouseoutEvent(event)
    if (et == 'keyup' or et == 'keydown' or
          et == 'keypress' or et == 'change'):
        return _dispatchCapturedEvent(event)
    else:
        return _dispatchCapturedMouseEvent(event)


def _dispatchCapturedEvent(event):

    if not previewEvent(event):
        #print "dce, stop propagation"
        event.stopPropagation()
        eventPreventDefault(event)
        return False
    return True


def addEventPreview(preview):
    sEventPreviewStack.append(preview)


def appendChild(parent, child):
    #print "appendChild", parent, child
    parent.appendChild(child)

def removeChild(parent, child):
    #print "removeChild", parent, child
    parent.removeChild(child)
    #print "after removeChild", parent, child

def replaceChild(parent, newChild, oldChild):
    parent.replaceChild(newChild, oldChild)


def buttonClick(element):
    evt = doc().createEvent('MouseEvents')
    evt.initMouseEvent("click", True, True, wnd(), 1, 0, 0, 0, 0, False,
                        False, False, False, 0, element)
    element.dispatchEvent(evt)


def compare(elem1, elem2):
    if hasattr(elem1, "isSameNode"):
        return elem1.isSameNode(elem2)
    return elem1 == elem2


def createAnchor():
    return createElement("A")


def createButton():
    return createElement("button")


def createCol():
    return createElement("col")


def createDiv():
    return createElement("div")


def createElement(tag):
    return doc().createElement(tag)


def createFieldSet():
    return createElement("fieldset")


def createForm():
    return createElement("form")


def createIFrame():
    return createElement("iframe")


def createImg():
    return createElement("img")


def createInputCheck():
    return createInputElement("checkbox")


def createInputElement(elementType):
    e = createElement("input")
    e.type = elementType
    return e


def createInputPassword():
    return createInputElement("password")


def createInputRadio(group):
    e = createInputElement('radio')
    e.name = group
    return e


def createInputText():
    return createInputElement("text")


def createLabel():
    return createElement("label")


def createLegend():
    return createElement("legend")


def createOptions():
    return createElement("options")


def createSelect():
    return createElement("select")


def createSpan():
    return createElement("span")


def createTable():
    return createElement("table")


def createTBody():
    return createElement("tbody")


def createTD():
    return createElement("td")


def createTextArea():
    return createElement("textarea")


def createTH():
    return createElement("th")


def createTR():
    return createElement("tr")


def eventStopPropagation(evt):
    evt.stopPropagation()


def eventCancelBubble(evt, cancel):
    evt.cancelBubble = cancel


def eventGetAltKey(evt):
    return evt.altKey


def eventGetButton(evt):
    return evt.button


def eventGetClientX(evt):
    return evt.clientX


def eventGetClientY(evt):
    return evt.clientY


def eventGetCtrlKey(evt):
    return evt.ctrlKey


def eventGetFromElement(evt):
    try:
        return evt.fromElement
    except:
        return None


def eventGetKeyCode(evt):
    return evt.which or evt.keyCode or 0


def eventGetRepeat(evt):
    return evt.repeat


def eventGetScreenX(evt):
    return evt.screenX


def eventGetScreenY(evt):
    return evt.screenY


def eventGetShiftKey(evt):
    return evt.shiftKey


def eventGetCurrentTarget(event):
    return event.currentTarget


def eventGetTarget(event):
    return event.target


def eventGetToElement(evt):
    type = eventGetType(evt)
    if type == 'mouseout':
        return evt.relatedTarget
    elif type == 'mouseover':
        return evt.target
    return None


def eventGetType(event):
    return event.type

def eventGetTypeInt(event):
    return Event.eventmap.get(str(event.type), 0)


def eventGetTypeString(event):
    return eventGetType(event)


def eventPreventDefault(evt):
    evt.preventDefault()


def eventSetKeyCode(evt, key):
    evt.keyCode = key


def eventToString(evt):
    return evt.toString()


def iframeGetSrc(elem):
    return elem.src


def getAbsoluteLeft(elem):
    left = 0
    curr = elem
    while curr.offsetParent:
        left -= curr.scrollLeft
        curr = curr.parentNode

    while elem:
        left += elem.offsetLeft - elem.scrollLeft
        elem = elem.offsetParent

    return left


def getAbsoluteTop(elem):
    top = 0
    curr = elem
    while curr.offsetParent:
        top -= curr.scrollTop
        curr = curr.parentNode

    while elem:
        top += elem.offsetTop - elem.scrollTop
        elem = elem.offsetParent

    return top


def getAttribute(elem, attr):
    attr = getattr(elem, attr)
    if attr is None:
        return None
    return str(attr)


def getElemAttribute(elem, attr):
    mf = get_main_frame()
    if not elem.hasAttribute(attr):
        return str(getattr(elem, mf.mash_attrib(attr)))
    return str(elem.getAttribute(attr))


def getBooleanAttribute(elem, attr):
    mf = get_main_frame()
    return bool(getattr(elem, mf.mash_attrib(attr)))


def getBooleanElemAttribute(elem, attr):
    if not elem.hasAttribute(attr):
        return None
    return bool(elem.getAttribute(attr))


def getCaptureElement():
    global sCaptureElem
    return sCaptureElem


def getChild(elem, index):
    """
    Get a child of the DOM element by specifying an index.
    """
    count = 0
    child = elem.firstChild
    while child:
        next = child.nextSibling
        if child.nodeType == 1:
            if index == count:
                return child
            count += 1
        child = next
    return None


def getChildCount(elem):
    """
    Calculate the number of children the given element has.  This loops
    over all the children of that element and counts them.
    """
    count = 0
    child = elem.firstChild
    while child:
        if child.nodeType == 1:
            count += 1
        child = child.nextSibling
    return count


def getChildIndex(parent, toFind):
    """
    Return the index of the given child in the given parent.

    This performs a linear search.
    """
    count = 0
    child = parent.firstChild
    while child:
        if child == toFind:
            return count
        if child.nodeType == 1:
            count += 1
        child = child.nextSibling

    return -1


def getElementById(id):
    """
    Return the element in the document's DOM tree with the given id.
    """
    return doc().getElementById(id)


def getEventListener(element):
    """
    See setEventListener() for more information.
    """
    return get_listener(element)

eventbitsmap = {}


def getEventsSunk(element):
    """
    Return which events are currently "sunk" for a given DOM node.  See
    sinkEvents() for more information.
    """
    return eventbitsmap.get(element, 0)


def getFirstChild(elem):
    child = elem and elem.firstChild
    while child and child.nodeType != 1:
        child = child.nextSibling
    return child


def getInnerHTML(element):
    try:
        return element and element.innerHtml # webkit. erk.
    except:
        return element and element.innerHTML # hulahop / xul.  yuk.


def getInnerText(element):
    # To mimic IE's 'innerText' property in the W3C DOM, we need to recursively
    # concatenate all child text nodes (depth first).
    text = ''
    child = element.firstChild
    while child:
        if child.nodeType == 1:
            text += getInnerText(child)
        elif child.nodeValue:
            text += child.nodeValue
        child = child.nextSibling
    return text


def getIntAttribute(elem, attr):
    return int(getattr(elem, attr))


def getIntElemAttribute(elem, attr):
    if not elem.hasAttribute(attr):
        return None
    return int(elem.getAttribute(attr))


def getIntStyleAttribute(elem, attr):
    return getIntAttribute(elem.style, attr)


def getNextSibling(elem):
    sib = elem.nextSibling
    while sib and sib.nodeType != 1:
        sib = sib.nextSibling
    return sib


def getNodeType(elem):
    return elem.nodeType


def getParent(elem):
    parent = elem.parentNode
    if parent is None:
        return None
    if getNodeType(parent) != 1:
        return None
    return parent


def getStyleAttribute(elem, attr):
    try:
        if hasattr(elem.style, 'getProperty'):
            return elem.style.getProperty(mash_name_for_glib(attr))
        return elem.style.getAttribute(attr)
    except AttributeError:
        return getattr(elem.style, attr, None)


def insertChild(parent, toAdd, index):
    count = 0
    child = parent.firstChild
    before = None
    while child:
        if child.nodeType == 1:
            if (count == index):
                before = child
                break

            count += 1
        child = child.nextSibling

    if before is None:
        parent.appendChild(toAdd)
    else:
        parent.insertBefore(toAdd, before)


class IterChildrenClass:

    def __init__(self, elem):
        self.parent = elem
        self.child = elem.firstChild
        self.lastChild = None

    def next(self):
        if not self.child:
            raise StopIteration
        self.lastChild = self.child
        self.child = getNextSibling(self.child)
        return self.lastChild

    def remove(self):
        self.parent.removeChild(self.lastChild)

    def __iter__(self):
        return self


def iterChildren(elem):
    """
    Returns an iterator over all the children of the given
    DOM node.
    """
    return IterChildrenClass(elem)


class IterWalkChildren:

    def __init__(self, elem):
        self.parent = elem
        self.child = getFirstChild(elem)
        self.lastChild = None
        self.stack = []

    def next(self):
        if not self.child:
            raise StopIteration
        self.lastChild = self.child
        firstChild = getFirstChild(self.child)
        nextSibling = getNextSibling(self.child)
        if firstChild is not None:
            if nextSibling is not None:
                self.stack.append((nextSibling, self.parent))
            self.parent = self.child
            self.child = firstChild
        elif nextSibling is not None:
            self.child = nextSibling
        elif len(self.stack) > 0:
            (self.child, self.parent) = self.stack.pop()
        else:
            self.child = None
        return self.lastChild

    def remove(self):
        self.parent.removeChild(self.lastChild)

    def __iter__(self):
        return self


def walkChildren(elem):
    """
    Walk an entire subtree of the DOM.  This returns an
    iterator/iterable which performs a pre-order traversal
    of all the children of the given element.
    """
    return IterWalkChildren(elem)


def isOrHasChild(parent, child):
    while child:
        if compare(parent, child):
            return True
        child = child.parentNode
        if not child:
            return False
        if child.nodeType != 1:
            child = None
    return False


def releaseCapture(elem):
    #print "releaseCapture", elem
    global sCaptureElem
    if sCaptureElem and compare(elem, sCaptureElem):
        sCaptureElem = None
        releaseCapture_impl(elem)
    return

# browser-specific overrides may implement this
def releaseCapture_impl(elem): pass

def removeEventPreview(preview):
    sEventPreviewStack.remove(preview)


def getOffsetHeight(elem):
    return elem.offsetHeight


def getOffsetWidth(elem):
    return elem.offsetWidth


def scrollIntoView(elem):
    left = elem.offsetLeft
    top = elem.offsetTop
    width = elem.offsetWidth
    height = elem.offsetHeight

    if elem.parentNode != elem.offsetParent:
        left -= elem.parentNode.offsetLeft
        top -= elem.parentNode.offsetTop

    cur = elem.parentNode
    while cur and cur.nodeType == 1:
        if hasattr(cur, 'style') and hasattr(cur.style, 'overflow') and \
           (cur.style.overflow == 'auto' or cur.style.overflow == 'scroll'):
            if left < cur.scrollLeft:
                cur.scrollLeft = left
            if left + width > cur.scrollLeft + cur.clientWidth:
                cur.scrollLeft = (left + width) - cur.clientWidth
            if top < cur.scrollTop:
                cur.scrollTop = top
            if top + height > cur.scrollTop + cur.clientHeight:
                cur.scrollTop = (top + height) - cur.clientHeight

        offsetLeft = cur.offsetLeft
        offsetTop = cur.offsetTop
        if cur.parentNode != cur.offsetParent:
            if hasattr(cur.parentNode, "offsetLeft"):
                offsetLeft -= cur.parentNode.offsetLeft
            if hasattr(cur.parentNode, "offsetTop"):
                offsetTop -= cur.parentNode.offsetTop

        left += offsetLeft - cur.scrollLeft
        top += offsetTop - cur.scrollTop
        cur = cur.parentNode


def mash_name_for_glib(name, joiner='-'):
    res = ''
    for c in name:
        if c.isupper():
            res += joiner + c.lower()
        else:
            res += c
    return res


def removeAttribute(element, attribute):
    element.removeAttribute(attribute)


def setAttribute(element, attribute, value):
    #print element, attribute, value
    setattr(element, attribute, value)


def setElemAttribute(element, attribute, value):
    element.setAttribute(attribute, value)


def setBooleanAttribute(elem, attr, value):
    mf = get_main_frame()
    setattr(elem, mf.mash_attrib(attr), value)


def setCapture(elem):
    global sCaptureElem
    sCaptureElem = elem
    #print "setCapture", sCaptureElem
    setCapture_impl(elem)

# browser-specific overrides may implement this
def setCapture_impl(elem): pass

def setEventListener(element, listener):
    """
    Register an object to receive event notifications for the given
    element.  The listener's onBrowserEvent() method will be called
    when a captured event occurs.  To set which events are captured,
    use sinkEvents().
    """
    set_listener(element, listener)


def createTextNode(txt):
    return doc().createTextNode(txt)


def setInnerHTML(element, html):
    try:
        element.innerHtml = html # webkit. yuk.
    except:
        element.innerHTML = html # hulahop / xul.  yukk.


def setInnerText(elem, text):
    #Remove all children first.
    while elem.firstChild is not None:
        elem.removeChild(elem.firstChild)
    elem.appendChild(createTextNode(text or ''))


def setIntElemAttribute(elem, attr, value):
    elem.setAttribute(attr, str(value))


def setIntAttribute(elem, attr, value):
    setattr(elem, attr, int(value))


def setIntStyleAttribute(elem, attr, value):
    mf = get_main_frame()
    if hasattr(elem.style, 'setProperty'):
        elem.style.setProperty(mf.mash_attrib(attr), str(value), "")
    else:
        elem.style.setAttribute(mf.mash_attrib(attr), str(value), "")


def setOptionText(select, text, index):
    option = select.options.item(index)
    option.textContent = text


def setStyleAttribute(element, name, value):
    if hasattr(element.style, 'setProperty'):
        element.style.setProperty(mash_name_for_glib(name), value, "")
    else:
        element.style.setAttribute(name, value, "")

def setStyleAttributes(element, **kwargs):
   """ 
   multi attr: setStyleAttributes(self, {attr1:val1, attr2:val2, ...})
   """ 
   for attr, val in kwargs.items():
        if hasattr(element.style, 'setProperty'):
                element.style.setProperty(mash_name_for_glib(attr), val, "")
        else:
                element.style.setAttribute(attr, val, "")

def sinkEvents(element, bits):
    """
    Set which events should be captured on a given element and passed to the
    registered listener.  To set the listener, use setEventListener().

    @param bits: A combination of bits; see ui.Event for bit values
    """
    mask = getEventsSunk(element) ^ bits
    eventbitsmap[element] = bits
    if not mask:
        return

    bits = mask

    if not bits:
        return
    mf = get_main_frame()
    if hasattr(mf, "_addEventListener"):
        aev = mf._addEventListener
    else:
        aev = mf.addEventListener
    #cb = lambda x,y,z: _dispatchEvent(y)
    cb = _dispatchEvent

    # mozilla stupidly has DOMMouseScroll...
    sinkEventsMozilla(element, bits)

    bit = 1
    while bits:
        if bit > bits:
            raise RuntimeError("sinkEvents: bit outruns bits")
        if (bits & bit):
            for event_name in Event.eventbits[bit][1]:
                aev(element, event_name, cb)
            bits ^= bit
        bit <<= 1

def sinkEventsMozilla(element, bits):
    pass

def toString(elem):
    temp = elem.cloneNode(True)
    tempDiv = createDiv()
    tempDiv.appendChild(temp)
    outer = getInnerHTML(tempDiv)
    setInnerHTML(temp, "")
    return outer


# TODO: missing dispatchEventAndCatch
def dispatchEvent(event, element, listener):
    dispatchEventImpl(event, element, listener)


def previewEvent(evt):
    #print "previewEvent", sEventPreviewStack
    if len(sEventPreviewStack) == 0:
        return True
    preview = sEventPreviewStack[-1]
    ret = preview.onEventPreview(evt)
    if ret:
        return True

    #print "previewEvent, cancel, prevent default"
    if evt:
        eventCancelBubble(evt, True)
        eventPreventDefault(evt)

    return ret


# TODO
def dispatchEventAndCatch(evt, elem, listener, handler):
    pass

currentEvent = None


def dispatchEventImpl(event, element, listener):
    global sCaptureElem
    global currentEvent
    if element == sCaptureElem:
        if eventGetType(event) == "losecapture":
            #print "lose capture"
            sCaptureElem = None
    #print "dispatchEventImpl", listener, eventGetType(event)
    prevCurrentEvent = currentEvent
    currentEvent = event
    listener.onBrowserEvent(event)
    currentEvent = prevCurrentEvent


def eventGetCurrentEvent():
    return currentEvent


def insertListItem(select, item, value, index):
    option = createElement("OPTION")
    setInnerText(option, item)
    if value is not None:
        setAttribute(option, "value", value)
    if index == -1:
        appendChild(select, option)
    else:
        insertChild(select, option, index)


def getBodyOffsetTop():
    return 0


def getBodyOffsetLeft():
    return 0

def eventGetMouseWheelVelocityY(evt):
    """ these are all different, across all platforms!
    """
    pass


if not pyjd.is_desktop:
    init()
