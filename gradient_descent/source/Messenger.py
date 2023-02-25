import os
from PIL import Image, ImageFont, ImageDraw


class Messenger:
    def __init__(self, path):
        self.path = path
        self.messages = []

    def pushMessage(self, message):
        self.messages.append(message)
        return self


    def dump(self, filename="times.png"):
        img = Image.new('RGB', (500, 200), color = (255,255,255))
        fnt = ImageFont.truetype("Pillow/Tests/fonts/FreeMono.ttf", 20)
        ImageDraw.Draw(img).text((10,10), "\n".join(self.messages), font=fnt, fill=(0,0,0))
        img.save(os.path.join(self.path, filename))

    def clear(self):
        self.messages.clear()

    def printLast(self):
        print(self.messages[-1])