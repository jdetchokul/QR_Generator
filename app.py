import qrcode
import csv
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
from qrcode.image.styles.colormasks import RadialGradiantColorMask
# https://pypi.org/project/qrcode/

from PIL import Image, ImageDraw, ImageFont

# fonts_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'fonts')
# font = ImageFont.truetype(os.path.join(fonts_path, 'sans_serif.ttf'), 24)
l1 = []
def read_csv_to_list(filename,l1):
    # l1 = []
    with open(filename, 'r', newline ='') as file:
        reader = csv.reader(file, delimiter = '\n')
        for row in reader:
            l1.append(row[0])
    return l1    

read_csv_to_list('library.csv',l1)
def draw(filename,i):
    image = Image.open(filename)
    width, height = image.size 

    draw = ImageDraw.Draw(image)

    text = 'SCAN to borrow!'
    text2 = 'Property of ANCA Thailand'
    
    
    ## Locate the text location within the file
    # textwidth, textheight = draw.textsize(text)
    # margin = 100
    # # x = width - textwidth - margin
    # # y = height - textheight - margin
    x = 65
    y = 3
    x1 = 20
    y2 = 330
    font = ImageFont.truetype(r'filepath\..\Alef-Bold.ttf', 30)
    font2 = ImageFont.truetype(r'filepath\..\Alef-Bold.ttf', 25)
    draw.text((x, y), text, font=font)
    draw.text((x1, y2), text2, font=font2)

    image.save(r'.\output\{}.png'.format(i))

    # optional parameters like optimize and quality
    # image.save('optimized.png', optimize=True, quality=50)

qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)

for i in l1:
    qr.add_data(f'https://amtte.onrender.com/lib/{i}')
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img = qrcode.make(f'https://amtte.onrender.com/lib/{i}')
    type(img)  # qrcode.image.pil.PilImage
    img.save(r'.\output\{}.png'.format(i))
    draw(r'.\output\{}.png'.format(i),i)

