import qrcode
from PIL import Image, ImageDraw, ImageFont


def make_qrc(data, caption, boxsize, color_text='black'):
    qr = qrcode.make(data, box_size=boxsize)
    width, height = qr.size
    bi = Image.new('RGBA', (width + 10, height + (height // 5)), 'white')
    bi.paste(qr, (5, 5, (width + 5), (height + 5)))
    fontsize = boxsize * (70/15)
    Imfont = ImageFont.truetype("arial.ttf", int(fontsize))
    w, h = Imfont.getsize(caption)
    draw = ImageDraw.Draw(bi)
    draw.text(((width - w) / 2, (height + ((height / 15) - h) / 2)), caption, font=Imfont, fill=color_text)

    return bi