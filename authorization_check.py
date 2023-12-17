import re
import string


def CheckMail(text):
    template_employee = re.compile(r'^[\w\.-]+@nnvid\.ru$')
    template_user = re.compile(r'^[\w\.-]+@\w+\.\w+$')

    match_user = re.match(template_user, text)
    match_employee = re.match(template_employee, text)

    if match_employee:
        return True, True    # Access/Is employee
    elif match_user:
        return True, False  # Access/Not employee
    else:
        return False, False


def ChangeReg(text):
    cyrillic_lower_letters = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    cyrillic_letters = cyrillic_lower_letters + cyrillic_lower_letters.upper()
    symbs = string.ascii_letters + cyrillic_letters
    flag = True
    for i in text:
        if i not in symbs:
            flag = False
            break
    if flag:
        return True, text[0].upper() + text[1:].lower()
    else:
        return False, ''


def CheckPasswdLength(text):
    if len(text) >= 8:
        return True
    else:
        return False
