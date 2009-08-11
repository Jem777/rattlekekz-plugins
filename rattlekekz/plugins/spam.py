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
from twisted.internet import task

class plugin:
    def __init__(self,controller,model,view):
        self.name="Spam-Hack"
        self.controller = controller
        self.model = model
        self.view = view
        self.model.hiThere(self.name,self)
        self.controller.botMsg("[spam-plugin]",self.view.hiThere(self.name,self)[2])
        self.public = task.loopingCall(self.model.sendMsg("geeks", "A loooooooooooong cat"))
        self.private = task.LoopingCall(self.model.sendMsg("guest_jem", "A shoooooooooooooort cat"))

    def unload(self):
        self.view.outHere(self.name,self)
        self.model.outHere(self.name,self)

    def receivedMsg(self, caller, nick, room, message):
        if message.lower().startswith("done"):
            self.public.stop()
            self.private.stop()
        elif message.lower().startswith("start"):
            self.public.start(0.1)
            self.private.start(0.1)
