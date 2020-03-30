#!/usr/bin/env python

import sys

import qrcode
import inkyphat

class InkyQR(qrcode.image.base.BaseImage):
    def new_image(self, **kwargs):
        self.offset_x = kwargs.get("offset_x", None)
        self.offset_y = kwargs.get("offset_y", None)

        if self.pixel_size - (self.border * 2) > min(inkyphat.WIDTH, inkyphat.HEIGHT):
            print("QR code is too large for Inky pHAT, it probably wont scan! Try `box_size=1`")

        if self.offset_x is None:
            self.offset_x = (inkyphat.WIDTH // 2) - (self.pixel_size // 2)
        if self.offset_y is None:
            self.offset_y = (inkyphat.HEIGHT // 2) - (self.pixel_size // 2)

        box = (self.offset_x, self.offset_y, self.offset_x + self.pixel_size - 1, self.offset_y + self.pixel_size - 1)
        inkyphat.rectangle(box, fill=inkyphat.WHITE)

    def pixel_box(self, row, col):
        x = (col + self.border) * self.box_size
        y = (row + self.border) * self.box_size
        x += self.offset_x
        y += self.offset_y
        return [(x, y), (x + self.box_size - 1, y + self.box_size - 1)]

    def drawrect(self, row, col):
        box = self.pixel_box(row, col)
        inkyphat.rectangle(box, fill=inkyphat.BLACK)


qr = qrcode.QRCode(
    version=1,
    box_size=2,
    border=1,
    image_factory=InkyQR
)

def printQRcode(text):
	inkyphat.clear()
	qr.add_data("http://128.143.67.97:44104/link_your_id/"+text)
	qr.make(fit=True)
	qr.make_image()
	inkyphat.show()
