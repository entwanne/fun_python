#!/usr/bin/env python

import sfml as sf
class DataImage:
    class Overflow(BaseException):
        pass

    def __init__(self, width, height, bpp=3):
        self.width, self.height, self.bpp = width, height, bpp
        self.off_x, self.off_y = 0, 0
        self.im = sf.Image.create(self.width, self.height)
        self.buff = []
        self.valid = True
    def save(self, filename):
        self.im.to_file(filename)

    def write(self, s):
        for c in s:
            self.buff.append(c)
            if len(self.buff) >= self.bpp:
                self._writebuff()
    def end(self):
        self._writebuff()
        self.valid = False

    def _writebuff(self):
        if not self.valid:
            raise self.Overflow
        self.im[self.off_x, self.off_y] = sf.Color(*self.buff)
        self.buff = []
        self.off_x += 1
        if self.off_x >= self.width:
            self.off_x = 0
            self.off_y += 1
            if self.off_y >= self.height:
                self.valid = False

if __name__ == '__main__':
    import os

    def readchunk(f, size):
        while True:
            c = f.read(size)
            if c:
                yield c
            else:
                break

    filename = 'file_to_img.py'
    width = 10
    bpp = 3
    linewidth = width * bpp
    size = os.stat(filename).st_size
    height = size // linewidth + 1
    with open(filename, 'rb') as src:
        im = DataImage(width, height, bpp)
        for s in readchunk(src, linewidth):
            im.write(s)
        im.end()
        im.save(filename + '.png')
