import argparse
import random
from datetime import datetime
from os import getcwd
from pathlib import Path
from time import time

import numpy as np
from PIL import Image
from utils import add_random_noise_to_image, generate_random_cnh


def tot_time(start_time, end_time):
    return end_time - start_time


def formatted_time(tot_time):
    return f'{str(int((tot_time / 3600)))}h:{str(int(((tot_time % 3600) / 60)))}m:{str(int(((tot_time % 3600) % 60)))}s'


def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def main():
    start_time = time()

    in_arg = get_input_args()

    run(size=in_arg.size, noise=in_arg.noise)

    end_time = time()
    now = datetime.now()
    print(
        f"\n** Total Elapsed Runtime: {formatted_time(tot_time(start_time, end_time))} **"
    )


def get_input_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("-s", "--size", required=False, default=10, type=int,
                        help="Dataset size to be generated")
    parser.add_argument("-n", "--noise", required=False, type=str2bool, default=False,
                        help="Apply noise to images?")

    return parser.parse_args()


def run(size: int, noise: bool):
    main_path = Path(getcwd())
    dataset_path = main_path / 'cnh_dataset'
    print(f'Generating {size} images in {dataset_path}')
    dataset_path.mkdir(exist_ok=True)

    for i in range(size):
        quality = random.randint(80, 100)
        random_cnh = generate_random_cnh()
        image = np.array(random_cnh)
        if noise:
            image = add_random_noise_to_image(image)
        image = Image.fromarray(image)
        image.save(dataset_path / f'{i}.jpg', quality=quality)


if __name__ == "__main__":
    main()
