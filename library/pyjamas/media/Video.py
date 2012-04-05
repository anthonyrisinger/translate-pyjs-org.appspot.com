"""
* Copyright 2009 Mark Renouf
*
* Licensed under the Apache License, Version 2.0 (the "License"); you may not
* use this file except in compliance with the License. You may obtain a copy of
* the License at
*
* http:#www.apache.org/licenses/LICENSE-2.0
*
* Unless required by applicable law or agreed to in writing, software
* distributed under the License is distributed on an "AS IS" BASIS, WITHDIR
* WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
* License for the specific language governing permissions and limitations under
* the License.
"""

from __pyjamas__ import get_main_frame
from pyjamas.media.Media import Media
from pyjamas import DOM

"""*
* An HTML5 VIDEO element
"""
class Video(Media):
    
    def __init__(self, src=None, **kwargs):
        self.setElement(DOM.createElement("video"))
        if src:
            self.setSrc(src)

        Media.__init__(self, **kwargs)

    def setSrc(self, src):
        Media.setSrc(self, src)

    def setControls(self, controls):
        Media.setControls(self, controls)

    def setStatusbar(self, statusbar):
        Media.setStatusbar(self, statusbar)

    def setLoop(self, autorewind):
        Media.setLoop(self, autorewind)

    def setAutoplay(self, autostart):
        Media.setAutoplay(self, autostart)

    def setWidth(self, width):
        Media.setWidth(self, width)

    def setHeight(self, height):
        Media.setHeight(self, height)

    def getVideoWidth(self):
        return self.getElement().videoWidth
    
    def getVideoHeight(self):
        return self.getElement().videoHeight
    

