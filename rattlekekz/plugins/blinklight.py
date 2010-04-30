#!/usr/bin/env python
# -*- coding: utf-8 -*-

copyright = """
    Copyright 2008, 2009 Moritz Doll and Christian Scharkus

    This file is part of rattlekekz.

    rattlekekz is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    rattlekekz is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with rattlekekz.  If not, see <http://www.gnu.org/licenses/>.
"""

import os
from twisted.internet import reactor

class plugin:
    def __init__(self,controller,model,view):
        self.name="blinklight"
        self.controller = controller
        self.model = model
        self.view = view
        self.model.hiThere(self.name,self)
        self.controller.botMsg("[blinklight-plugin]",self.view.hiThere(self.name,self)[2])
        self.lightpath = "/proc/acpi/ibm/light"
        try:
            self.lighthandle = open(self.lightpath, "r+")
        except:
            self.controller.botMsg("[blinklight-plugin]", "Could not load plugin, no thinklight device found")
            self.unload()
        
    def unload(self):
        try:
            self.lighthandle.close()
        except:
            pass
        self.view.outHere(self.name,self)
        self.model.outHere(self.name,self)
        self.controller.botMsg("[blinklight-plugin]", "plugin unloaded")

    def receivedMsg(self, caller, nick, room, message):
        if (self.controller.nickpattern.search(message) is not None) and (self.controller.nickname != nick):
            self.blinklight()

    def privMsg(self, caller, nick, message):
        if self.controller.nickname != nick:
            self.blinklight()

    def blinklight(self):
        on = self.is_on()
        self.blink(not on, 3)

    def is_on(self):
        self.lighthandle.seek(0) 
        lines = self.lighthandle.readlines()
        for line in lines:
            if line.startswith("status"):
                if line.split()[1] == "on":
                    return True
                else:
                    return False
        return False

    def blink(self, on = True, times = 0):
        if on:
            x = "on"
        else:
            x = "off"
        self.lighthandle.write(x)
        self.lighthandle.flush()
        if times > 0:
            reactor.callLater(0.1, lambda: self.blink(not on, times-1))
