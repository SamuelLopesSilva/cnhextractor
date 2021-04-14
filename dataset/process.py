import random
import string

import numpy as np
from faker import Faker
from fordev.generators import cnh, people, uf
from PIL import Image, ImageDraw, ImageFont
from skimage.util import random_noise

FONT = 'fonts/Monob.ttf'
MODEL = 'models/cnh_model.jpg'


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
        self.first_cnh = Write(
            cords=(random.randint(526, 533), random.randint(465, 480)), value=infos['first_cnh']
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
        for name, write in self.infos.__dict__.items():
            if isinstance(write, Write):
                self.img = write_on_image(self.img, write)


def write_on_image(image: np.array, w_config: Write) -> np.array:
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(FONT, 17)
    draw.text(w_config.cords, w_config.value, w_config.color, font=font)
    return image


def add_random_noise_to_image(image: np.array) -> np.array:
    noise = random_noise(
        image, mode='s&p', amount=random.uniform(0.0051, 0.11))
    return np.array(255 * noise, dtype=np.uint8)


def generate_random_cnh(**kwargs) -> np.array:
    fake = Faker()
    ppl = people(uf_code=uf()[0])
    cnh_number = cnh()
    rnd_validity = fake.date_between(
        start_date='today', end_date='+5y').strftime("%m/%d/%Y")
    first_cnh = fake.date_between(
        start_date='-30y', end_date='-5y').strftime("%m/%d/%Y")
    rg = ppl['rg'].replace('.', '').replace('-', '')
    org_initials = ''.join(random.choice(string.ascii_uppercase)
                           for _ in range(3))
    infos = {
        'name': ppl['nome'].upper(),
        'validity': rnd_validity,
        'number': cnh_number,
        'birth_date': ppl['data_nasc'],
        'cpf': ppl['cpf'],
        'parents': f"{ppl['pai'].upper()}\n\n{ppl['mae'].upper()}",
        'rg_org_uf': f"{rg} {org_initials} {ppl['estado']}",
        'first_cnh': first_cnh
    }
    return FakeCNH(MODEL, CNHInfos(infos), **kwargs).create()
