import re
import random
import string
import unicodedata

ALPHANUMERIC_CHARS = string.ascii_lowercase + string.digits
STRING_LENGTH = 6

def generate_random_string(chars=ALPHANUMERIC_CHARS, length=STRING_LENGTH):
    return "".join(random.choice(chars) for _ in range(length))

def slugify(title):
    title = unicodedata.normalize('NFKD', str(title)).encode(
        'ascii', 'ignore').decode('ascii')
    title = re.sub(r'[^\w\s-]', '', title).strip().lower()
    return re.sub(r'[-\s]+', '-', title)

