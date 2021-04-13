from fordev.generators import people, cnh
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from skimage.util import random_noise
import numpy as np
import random


def write_text_on_image(img, text, cords, color=(7, 9, 6, 255)):
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype('fonts/Monob.ttf', 17)
    draw.text(cords, text, color, font=font)
    return img


def write_name_cnh(img, name):
    cords = (random.randint(132, 135), random.randint(138, 140))
    return write_text_on_image(img, name, cords=cords)


def write_cpf_cnh(img, cpf):
    cords = (random.randint(381, 383), random.randint(226, 238))
    return write_text_on_image(img, cpf, cords=cords)


def write_birth_date_cnh(img, date):
    cords = (random.randint(569, 573), random.randint(226, 238))
    return write_text_on_image(img, date, cords=cords)


def write_validity_cnh(img, validity):
    cords = (random.randint(369, 377), random.randint(462, 474))
    return write_text_on_image(img, validity, cords=cords)


def write_cnh_number(img, number):
    cords = (random.randint(139, 141), random.randint(462, 474))
    return write_text_on_image(img, number, cords=cords)


def write_parents_cnh(img, parents):
    cords = (random.randint(386, 399), random.randint(291, 298))
    parents = f"{parents[0]}\n\n{parents[1]}"
    return write_text_on_image(img, parents, cords=cords)


def add_random_noise_to_image(image):
    noise = random_noise(
        image, mode='s&p', amount=random.uniform(0.0051, 0.11))
    return np.array(255 * noise, dtype=np.uint8)


def generate_random_cnh():
    ppl = people()
    cnh_number = cnh()
    image = Image.open('models/cnh_model.jpg')
    image = write_name_cnh(image, ppl['nome'])
    image = write_validity_cnh(image, '05/07/2024')
    image = write_cnh_number(image, cnh_number)
    image = write_birth_date_cnh(image, ppl['data_nasc'])
    image = write_cpf_cnh(image, ppl['cpf'])
    image = write_parents_cnh(image, (ppl['pai'], ppl['mae']))
    return image
