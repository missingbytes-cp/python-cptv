from PIL import Image
from path import join
import cv2
import numpy as np


def process_frame_to_rgb(frame):
    a = np.zeros((120, 160))
    a = cv2.normalize(frame, a, 0, 65535, cv2.NORM_MINMAX)
    m1 = 0.25*65535
    m2 = 0.50*65535
    m3 = 0.75*65535
    b1 = np.where(a <=m1, 1, 0)
    b2 = np.where(np.bitwise_and(m1 < a, a <=m2), 1, 0)
    b3 = np.where(np.bitwise_and(m2 < a, a <=m3), 1, 0)
    b4 = np.where(m3 < a, 1, 0)
    rgb = np.zeros((120, 160, 3), 'uint8')
    rgb[..., 0] = ((a-0.5*65535)*255*4/65535.0*b3 + b4*255)
    rgb[..., 1] = (b2*255 + b3*255 + b1*255*a*4/65535.0 + b4*255*((65535.0-a)*4/65535.0))
    rgb[..., 2] = (b1*255 + b2*255*((0.5*65535.0-a)*4)/65535.0 )
    return rgb

def save_rgb_as_image(rgb, n, folder):
    im = Image.fromarray(rgb, "RGB")
    imName = str(n).zfill(6) + '.png'
    im.save(join(folder, imName))
