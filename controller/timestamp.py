from datetime import datetime
import re


def get_timestamp():
    return datetime.now().strftime("%d-%m-%Y-%H:%M")

def check_date(date):
    """
        Regex to check if a date is on the good format
    """
    date_find = re.findall(r"\d{2}/\d{2}/\d{2,4}", date)

    if date_find:
        return True
    else:
        return False

