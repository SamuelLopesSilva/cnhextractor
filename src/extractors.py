import datetime
import re
from src.utils import valid_date_string


def extract_cnh_number(data: dict, text: str, ratio: float):
    if (5.1 <= ratio <= 7.1 and data['numero'] is None):
        numbers = re.findall(r"(\d{11})", text)
        for number in numbers:
            if (len(number) == 11):
                data['numero'] = number


def extract_cpf_cnh(data: dict, text: str, text_size: str, ratio: float):
    cpf_pattern = '[0-9]{3}\.[0-9]{3}\.[0-9]{3}\-[0-9]{2}'
    if (3.3 <= ratio <= 5) and (data["cpf"] is None) and (text_size > 12):
        text = text.replace(',', '.')
        cpf_search = re.findall(cpf_pattern, text)
        if cpf_search:
            data["cpf"] = cpf_search[0]


def extract_rg_cnh(data: dict, text: str, words: int, ratio: float):
    if (7.2 <= ratio <= 10):
        if (data["rg"] is None):
            if (words >= 1):
                rg_data = re.split(r"([\w\/]+)", text)
                for d in rg_data:
                    size = len(d)
                    if (size == 2):
                        data["rg_uf"] = d
                    elif (2 <= size <= 6):
                        data["rg_emissor"] = d
                    elif (size > 6):
                        data["rg"] = "".join(d.split())


def extract_dates_cnh(data: dict, text: str, text_size: int, ratio: float):
    if (3.3 <= ratio <= 5):
        if (text_size == 10 and text.find("/")):
            dateObj = valid_date_string(text.strip())
            if (isinstance(dateObj, datetime.datetime)):
                now = datetime.datetime.now()
                legalAge = datetime.datetime.now() - datetime.timedelta(days=365*18)
                if (data["dt_nasc"] is None and dateObj < legalAge):
                    data["dt_nasc"] = "".join(text.split())
                if (data["validade"] is None and dateObj > now):
                    data["validade"] = "".join(text.split())


def extract_name_cnh(data: dict, text: str, words: int, ratio: float):
    if (12.5 <= ratio <= 17) and (data["nome"] is None) and (words < 7 and words > 1):
        data["nome"] = text
