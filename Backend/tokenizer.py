import hashlib
import random
import string
import time


# local salt param
local_salt = 'VHFinder-the-best!'


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

