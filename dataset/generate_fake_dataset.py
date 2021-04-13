from pathlib import Path
from os import getcwd
from utils import generate_random_cnh, add_random_noise_to_image
from PIL import Image
import cv2
import numpy as np
import random

DATASETLEN = 10
NOISE = True


if __name__ == "__main__":
    main_path = Path(getcwd())
    dataset_path = main_path / 'cnh_dataset'
    dataset_path.mkdir(exist_ok=True)

    for i in range(DATASETLEN):
        quality = random.randint(80, 100)
        random_cnh = generate_random_cnh()
        image = cv2.cvtColor(np.array(random_cnh), cv2.COLOR_RGB2BGR)
        if NOISE:
            image = add_random_noise_to_image(image)
        image = Image.fromarray(image)
        image.save(dataset_path / f'{i}.jpg', quality=quality)
