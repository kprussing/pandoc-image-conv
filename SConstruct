#!/usr/bin/env python

import os

tools = ["default", "pandoc", "inkscape"]
env = Environment(ENV=os.environ, tools=tools)
env.AppendUnique(PANDOCFLAGS=["--filter", File("pandoc_image_conv.py")])

Export("env")
SConscript(os.path.join("example", "SConscript"))

