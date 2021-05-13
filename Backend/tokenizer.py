import hashlib
import random
import string
import time


# local salt param
local_salt = 'VHFinder-the-best!'


def check_password_security(password):
    if len(password) < 8:
        return '3'
    if password.upper() == password:
        return '4'
    if len(set(password)) < 5:
        return '5'
    if len(set(password).intersection({'1', '2', '3', '4', '5', '6', '7', '8', '9'})) == 0:
        return '6'
    return '0'


def gen_salt(n):
    chars = list(string.ascii_uppercase + string.digits)
    return ''.join(random.choice(chars) for i in range(n))


def get_hash(password, salt):
    hash_str = password + salt + local_salt
    return hashlib.sha512(hash_str.encode('utf-8')).hexdigest()


def generate_token(n):
    chars = list(string.ascii_uppercase + string.digits)
    token = ''.join(random.choice(chars) for i in range(n)) + str(time.time())
    return hashlib.sha512(token.encode('utf-8')).hexdigest()
