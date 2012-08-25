#!/usr/bin/python

'''
    Copyright 2009, The Android Open Source Project

    Licensed under the Apache License, Version 2.0 (the "License"); 
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at 

        http://www.apache.org/licenses/LICENSE-2.0 

    Unless required by applicable law or agreed to in writing, software 
    distributed under the License is distributed on an "AS IS" BASIS, 
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. 
    See the License for the specific language governing permissions and 
    limitations under the License.
'''

# script to highlight adb logcat output for console
# written by jeff sharkey, http://jsharkey.org/
# piping detection and popen() added by other android team members
# 02 Nov 2009 - Adrian Vintu (www.adrianvintu.com) - added Windows compatibility - not a python programmer ;)


import os, sys, re, StringIO
import struct
import ctypes
import color_console as cons
from ctypes import byref

# unpack the current terminal width/height
csbi = cons.CONSOLE_SCREEN_BUFFER_INFO()
cons.GetConsoleScreenBufferInfo(cons.stdout_handle, byref(csbi))
WIDTH = csbi.dwSize.X
WIDTH = WIDTH - 1  #because of some extra space in output

BLACK, BLUE, GREEN, CYAN, RED, MAGENTA, YELLOW, GREY = range(8)

def indent_wrap(message, indent=0, width=80):
    wrap_area = width - indent
    messagebuf = StringIO.StringIO()
    current = 0
    while current < len(message):
        next = min(current + wrap_area, len(message))
        messagebuf.write(message[current:next])
        if next < len(message):
            messagebuf.write("%s " % (" " * indent))
        current = next
    return messagebuf.getvalue()


LAST_USED = [RED,GREEN,YELLOW,BLUE | cons.FOREGROUND_INTENSITY,MAGENTA,CYAN,GREY]
KNOWN_TAGS = {
    "dalvikvm": BLUE | cons.FOREGROUND_INTENSITY,
    "Process": BLUE | cons.FOREGROUND_INTENSITY,
    "ActivityManager": CYAN,
    "ActivityThread": CYAN,
}

def allocate_color(tag):
    # this will allocate a unique format for the given tag
    # since we dont have very many colors, we always keep track of the LRU
    if not tag in KNOWN_TAGS:
        KNOWN_TAGS[tag] = LAST_USED[0]
    color = KNOWN_TAGS[tag]
    LAST_USED.remove(color)
    LAST_USED.append(color)
    return color


TAGTYPE_WIDTH = 3
TAG_WIDTH = 20
PROCESS_WIDTH = 8 # 8 or -1
HEADER_SIZE = TAGTYPE_WIDTH + 1 + TAG_WIDTH + 1 + PROCESS_WIDTH + 1


retag = re.compile("^([A-Z])/([^\(]+)\(([^\)]+)\): (.*)$")

# to pick up -d or -e
adb_args = ' '.join(sys.argv[1:])

# if someone is piping in to us, use stdin as input.  if not, invoke adb logcat
if os.isatty(sys.stdin.fileno()):
    input = os.popen("adb %s logcat" % adb_args)
else:
    input = sys.stdin

default_colors = cons.get_text_attr()
default_bg = default_colors & 0x0070

while True:
    try:
        line = input.readline()
    except KeyboardInterrupt:
        break

    match = retag.match(line)
    if not match is None:
        tagtype, tag, owner, message = match.groups()
        linebuf = StringIO.StringIO()

        # center process info
        if PROCESS_WIDTH > 0:
            owner = owner.strip().center(PROCESS_WIDTH)
            cons.set_text_attr(cons.FOREGROUND_BLACK | cons.BACKGROUND_BLACK | cons.BACKGROUND_INTENSITY)
            print owner,
            cons.set_text_attr(default_colors)
            #linebuf.write("%s%s%s " % (format(fg=BLACK, bg=BLACK, bright=True), owner, format(reset=True)))

        # right-align tag title and allocate color if needed
        tag = tag.strip()
        color = allocate_color(tag)
        tag = tag[-TAG_WIDTH:].rjust(TAG_WIDTH)
        cons.set_text_attr(color)
        print tag,
        cons.set_text_attr(default_colors)

        print " ",
        #linebuf.write("%s%s %s" % (format(fg=color, dim=False), tag, format(reset=True)))

        # write out tagtype colored edge
        #if not tagtype in TAGTYPES: break
        #linebuf.write(TAGTYPES[tagtype])

        if tagtype == "V":
          cons.set_text_attr(cons.FOREGROUND_GREY | cons.BACKGROUND_BLACK)
        elif tagtype == "D":
          cons.set_text_attr(cons.FOREGROUND_BLACK | cons.BACKGROUND_BLUE | cons.BACKGROUND_INTENSITY)
        elif tagtype == "I":
          cons.set_text_attr(cons.FOREGROUND_BLACK | cons.BACKGROUND_GREEN)
        elif tagtype == "W":
          cons.set_text_attr(cons.FOREGROUND_BLACK | cons.BACKGROUND_YELLOW)
        elif tagtype == "E":
          cons.set_text_attr(cons.FOREGROUND_BLACK | cons.BACKGROUND_RED)
        else:
          break;

        print tagtype + " ",

        cons.set_text_attr(default_colors)
        #print tag

				#linebuf.write(TAGTYPES[tagtype])

        # insert line wrapping as needed
        message = indent_wrap(message, HEADER_SIZE, WIDTH)

        #linebuf.write(message)
        #line = linebuf.getvalue()
        print message

    #print line
    if len(line) == 0: break

cons.set_text_attr(default_colors)












