import random

import numpy as np
from fordev.generators import cnh, people, uf
from PIL import Image, ImageDraw, ImageFont
from skimage.util import random_noise


# TODO - Terminar forma mais bonita pra versão final depois de estar tudo funcionando
class CNHInfos:
    def __init__(self, infos: dict):
        self.name = Write(
            cords=(random.randint(132, 135), random.randint(138, 140)), value=infos['name']
        )
        self.cpf = Write(
            cords=(random.randint(381, 383), random.randint(226, 238)), value=infos['cpf']
        )
        self.birth_date = Write(
            cords=(random.randint(569, 573), random.randint(226, 238)), value=infos['birth_date']
        )
        self.validity = Write(
            cords=(random.randint(369, 377), random.randint(462, 474)), value=infos['validity']
        )
        self.cnh_number = Write(
            cords=(random.randint(139, 141), random.randint(462, 474)), value=infos['number']
        )
        self.parents = Write(
            cords=(random.randint(386, 399), random.randint(291, 298)), value=infos['parents']
        )
        self.rg_org_uf = Write(
            cords=(random.randint(379, 391), random.randint(176, 185)), value=infos['rg_org_uf']
        )


class Write:
    def __init__(self, cords, value, color=(7, 9, 6, 255)):
        self.cords = cords
        self.value = value
        self.color = color


class FakeCNH:
    def __init__(self, model, infos: CNHInfos, front_and_back=False):
        self.img = Image.open(model)
        self.infos = infos
        self.front_and_back = front_and_back

    def create(self):
        self._fill_all()
        if not self.front_and_back:
            self.img = Image.fromarray(np.array(self.img)[6:505, 6:729, :])
        return self.img

    def _fill_all(self):
        # TODO - Resolver problema da cor do texto
        self.img = write_on_image(self.img, self.infos.name)


def write_on_image(img, w_config: Write):
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype('Monob.ttf', 17)
    draw.text(w_config.cords, w_config.value, color=w_config.color, font=font)
    return img


def write_text_on_image(img, text, cords, color=(7, 9, 6, 255)):
    #image = Image.open(img_model_path)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype('fonts/Monob.ttf', 17)
    draw.text(cords, text, color, font=font)
    return img


def write_name_cnh(img, name):
    cords = (random.randint(132, 135), random.randint(138, 140))
    return write_text_on_image(img, name, cords=cords, color=(0, 0, 0, 0))


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


def write_rg_org_uf_cnh(img, values):
    cords = (random.randint(379, 391), random.randint(176, 185))
    values = f"{values[0]} {values[1]} {values[2]}"
    return write_text_on_image(img, values, cords=cords)


def add_random_noise_to_image(image):
    noise = random_noise(
        image, mode='s&p', amount=random.uniform(0.0051, 0.11))
    return np.array(255 * noise, dtype=np.uint8)


def generate_random_cnh(front_and_back=False):
    ppl = people(uf_code=uf()[0])
    cnh_number = cnh()
    image = Image.open('models/cnh_model.jpg')
    image = write_name_cnh(image, ppl['nome'].upper())
    image = write_validity_cnh(image, '05/07/2024')
    image = write_cnh_number(image, cnh_number)
    image = write_birth_date_cnh(image, ppl['data_nasc'])
    image = write_cpf_cnh(image, ppl['cpf'])
    image = write_parents_cnh(image, (ppl['pai'].upper(), ppl['mae'].upper()))
    rg = ppl['rg'].replace('.', '').replace('-', '')
    image = write_rg_org_uf_cnh(image, (rg, 'TES', ppl['estado']))
    if not front_and_back:
        image = Image.fromarray(np.array(image)[6:505, 6:729, :])
    return image


def generate_random_cnh_v2(**kwargs):
    ppl = people(uf_code=uf()[0])
    cnh_number = cnh()
    rg = ppl['rg'].replace('.', '').replace('-', '')
    infos = {
        'name': ppl['nome'],
        'validity': '05/07/2024',
        'number': cnh_number,
        'birth_date': ppl['data_nasc'],
        'cpf': ppl['cpf'],
        'parents': f"{ppl['pai']}\n\n{ppl['mae']}",
        'rg_org_uf': f"{rg} TES {ppl['estado']}"
    }
    return FakeCNH('cnh_model.jpg', CNHInfos(infos), **kwargs).create()
