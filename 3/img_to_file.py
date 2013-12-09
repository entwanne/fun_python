#!/usr/bin/env python

import sfml as sf

filename = 'file_to_img.py.png'
bpp = 3
s = b''

im = sf.Image.from_file(filename)
for y in range(im.height):
    for x in range(im.width):
        s += bytes(im[x, y])[:bpp]

print(s.decode())
