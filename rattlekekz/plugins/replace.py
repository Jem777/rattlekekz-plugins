#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

class plugin():
    def __init__(self,controller,model,view,time='true'):
        self.controller = controller
        self.model = model
        self.view = view
        #self.controller.botMsg("model",self.model.hiThere('replace',self)[2])
        self.controller.botMsg("view",self.view.hiThere('replace',self)[2])
        self.replacements=[]
        if os.path.exists(os.path.expanduser("~")+os.sep+".rattlekekz"+os.sep+"replace"):
            replace = open(os.path.expanduser("~")+os.sep+".rattlekekz"+os.sep+"replace","r")
            lines = replace.readlines()
            for line in lines:
                line = line.split(" ")
                self.replacements.append((line[0],line[1]))
            replace.close()
    
    def unload(self):
        self.dumpReplacements()
        self.view.outHere('replace',self)
        #self.model.outHere('replace',self)
    
    def sendStr(self,caller,channel,string):
        if string.startswith("/replace"):
            cmd = string[9:]
        else:
            cmd = False
        if not cmd:
            for i in self.replacements:
                string = string.replace(i[0],i[1])
            self.controller.sendStr(channel,string)
        else:
            if cmd.startswith("add"):
                cmd = cmd.split(" ")
                if len(cmd) > 2:
                    self.replacements.append((cmd[1],cmd[2]))
                    self.dumpReplacements()
                    self.controller.botMsg("[replace]","added")
                else:
                    self.controller.botMsg("[replace]","usage: /replace add string replacement (no whitespaces in the strings)")
            elif cmd.startswith("list"):
                for i in range(len(self.replacements)):
                    self.controller.botMsg("[replace]"," ".join([str(i),str(self.replacements[i])]))
            elif cmd.startswith("del"):
                try:
                    cmd = int(cmd[4:])
                except:
                    self.controller.botMsg("[replace]","del needs a number as argument")
                else:
                    try:
                        del self.replacements[cmd]
                    except:
                        self.controller.botMsg("[replace]","id out of range")
                    else:
                        self.dumpReplacements()
                        self.controller.botMsg("[replace]","deleted")
            else:
                self.controller.botMsg("[replace]","usage: /replace add string replacement (no whitespaces in the strings)")
        return "handled"

    def dumpReplacements(self):
        replace = open(os.path.expanduser("~")+os.sep+".rattlekekz"+os.sep+"replace","w")
        for i in self.replacements:
            replace.write(i[0]+" "+i[1]+" \n")
        replace.close()