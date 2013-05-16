#!/usr/bin/env python2

def get_term_rgb(color):
	values = [0, 95, 135, 175, 215, 255]
	if color < 8:
		r, g, b = (color % 2) * 205, ((color / 2) % 2) * 205, (color / 4) * 205
	elif color == 8:
		r, g, b = 127, 127, 127
	elif color < 16:
		color -= 8
		r, g, b = (color % 2) * 255, ((color / 2) % 2) * 255, (color / 4) * 255
	elif color < 232:
		color -= 16
		r, g, b = values[color / 36], values[(color / 6) % 6], values[color % 6]
	elif color < 256:
		color -= 232
		r, g, b = color * 10 + 8, color * 10 + 8, color * 10 + 8
	else:
		r, g, b = 0, 0, 0
	return (r, g, b)

def get_term_code(colors, r, g, b):
	dist = -1
	code = 0
	for i in range(len(colors)):
		disttmp = (r - colors[i][0])**2 + (g - colors[i][1])**2 + (b - colors[i][2])**2
		if dist < 0 or disttmp < dist:
			dist = disttmp
			code = i
	return code

colors = []
for i in range(256):
	colors.append(get_term_rgb(i))

import sys
from os import write
from PIL import Image

try:
	img = Image.open(sys.argv[1])
except:
	print 'Usage : %s image' % (sys.argv[0])
	sys.exit(1)

w, h = img.size
WMAX = 140
step = max(w / WMAX, 1)
for y in range(0, h, 2 * step):
	for x in range(0, w, step):
		c = img.getpixel((x, y))
		i = get_term_code(colors, c[0], c[1], c[2])
		write(1, '\033[48;5;%dm \033[0m' % i)
	write(1, '\n')
