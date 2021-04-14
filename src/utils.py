import datetime
import re


def get_default_data():
    return {
        "nome": None,
        "cpf": None,
        "dt_nasc": None,
        "rg": None,
        "rg_emissor": None,
        "rg_uf": None,
        "numero": None,
        "validade": None
    }


def get_best_prediction(predictions):
    best = ''
    for pred in predictions:
        if len(pred) > len(best):
            best = pred
    return best


def clean_text(text):
    clean_text_pattern = r"[^A-Z0-9.,\-\s\/]"
    text = re.sub(clean_text_pattern, "", text)
    return text.strip()


def valid_date_string(date_text):
    try:
        return datetime.datetime.strptime(date_text, '%d/%m/%Y')
    except ValueError:
        print("Unable to parse this string to date: ", date_text)
