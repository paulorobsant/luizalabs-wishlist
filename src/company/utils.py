import re


def get_email_suffix(email: str):
    domain = re.search("@[\\w.]+", email)
    return domain.group().replace("@", "")
