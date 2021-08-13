import random
import string


def id_generator(size=3, chars=string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def incrementor():
    info = {"count": 100}

    def number():
        info["count"] += 1
        return info["count"]
    return number
