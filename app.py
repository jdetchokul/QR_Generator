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

# Create header image
def header(output_path, width):
    image = Image.new("RGB", (width,45), "white")
    draw = ImageDraw.Draw(image)
    color = "red"
    x = 40
    y = 10
    text = 'Connect to ANCA CNC WIFI'
    font = ImageFont.truetype(r'filepath\..\Alef-Bold.ttf', size = 25)
    draw.text((x, y), text, font = font, fill = color)
    image.save(output_path)
    return image.size

def read_csv_to_list(filename,l1):
    with open(filename, 'r', newline ='') as file:
        reader = csv.reader(file, delimiter = '\n')
        for row in reader:
            l1.append(row[0])
    return l1    


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
    x = 80
    y = 3
    x1 = 40
    y2 = 375
    font = ImageFont.truetype(r'filepath\..\Alef-Bold.ttf', 30)
    font2 = ImageFont.truetype(r'filepath\..\Alef-Bold.ttf', 25)
    draw.text((x, y), text, font=font)
    draw.text((x1, y2), text2, font=font2)

    image.save(r'.\output\{}.png'.format(i))

    # optional parameters like optimize and quality
    # image.save('optimized.png', optimize=True, quality=50)
    
# Combine images
def append_images(images, direction='horizontal', bg_color=(255,255,255), aligment='center', widths=list(), heights=list()):

    """
    Appends images in horizontal/vertical direction.

    Args:
        images: List of PIL images
        direction: direction of concatenation, 'horizontal' or 'vertical'
        bg_color: Background color (default: white)
        aligment: alignment mode if images need padding;
           'left', 'right', 'top', 'bottom', or 'center'

    Returns:
        Concatenated image as a new PIL image object.
    """

    if direction=='horizontal':
        new_width = sum(widths)
        new_height = max(heights)
    else:
        new_width = max(widths)
        new_height = sum(heights)

    new_im = Image.new('RGB', (new_width, new_height), color=bg_color)


    offset = 0
    for im in images:
        if direction=='horizontal':
            y = 0
            if aligment == 'center':
                y = int((new_height - im.size[1])/2)
            elif aligment == 'bottom':
                y = new_height - im.size[1]
            new_im.paste(im, (offset, y))
            offset += im.size[0]
        else:
            x = 0
            if aligment == 'center':
                x = int((new_width - im.size[0])/2)
            elif aligment == 'right':
                x = new_width - im.size[0]
            new_im.paste(im, (x, offset))
            offset += im.size[1]

    return new_im

def main():    
    read_csv_to_list('library.csv',l1)    
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    widths = []
    heights = []

    ## Generate QR code out of actual range
    # : maximum generate = 60 items per 1 time
    # : must change every l1 in code below to l2

    #l2 = []
    #for i in range(31,91):
    #    number = "{:03d}".format(i)
    #    text = 'ETH' + number
    #    l2.append(text)


    for i in l1:
        qr.add_data(f'http://ws-ag-th-08.anca.com.au:5000/lib/{i}')
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img = qrcode.make(f'http://ws-ag-th-08.anca.com.au:5000/lib/{i}')
        type(img)  # qrcode.image.pil.PilImage

        # Add size of QR in list of wigths and heights
        if i == l1[0]:
            width_qr = img.size[0]
            height_qr = img.size[1]
            widths.append(width_qr)
            heights.append(height_qr)

            # Draw header
            (width_head, height_head) = header(r'.\output\header.png', width=width_qr)

            widths.append(width_head)
            heights.append(height_head)

        img.save(r'.\output\{}.png'.format(i))
        draw(r'.\output\{}.png'.format(i),i)

        # Combine header image and qr image
        combine_img = map(Image.open, [r'.\output\header.png', r'.\output\{}.png'.format(i)])
        combine = append_images(combine_img, direction='vertical', bg_color=(0, 0, 0), aligment='center', widths=widths, heights=heights)
        combine.save(r'.\output\{}.png'.format(i))


if __name__ == "__main__":
    main()
