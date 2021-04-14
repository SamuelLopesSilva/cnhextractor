import argparse
import random
from datetime import datetime
from os import getcwd
from pathlib import Path
from time import time

import numpy as np
from PIL import Image

from src.process import extract_information_from_cnh


def tot_time(start_time, end_time):
    return end_time - start_time


def formatted_time(tot_time):
    return f'{str(int((tot_time / 3600)))}h:{str(int(((tot_time % 3600) / 60)))}m:{str(int(((tot_time % 3600) % 60)))}s'


def main():
    start_time = time()

    in_arg = get_input_args()

    data = run(Path(in_arg.image))
    print_result(data)

    end_time = time()
    now = datetime.now()
    print(
        f"\n** Total Elapsed Runtime: {formatted_time(tot_time(start_time, end_time))} **"
    )


def get_input_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--image", required=True,
                        help="Path to the image")

    return parser.parse_args()


def run(image_path: Path) -> dict:
    print(f'Extracting information from {image_path}\n')
    image = np.array(Image.open(image_path))
    return extract_information_from_cnh(image)


def print_result(data: dict, repl_none: str = 'Não encontrado'):
    for key, value in data.items():
        print(f'{key.upper()}: {value if value else repl_none}')


if __name__ == "__main__":
    main()
