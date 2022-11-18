
from time import perf_counter
from statistics import median


dictionary = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ '
MAX_LENGTH_TO_ATTEMPT = 20
USER_PASSWORD = "password"


def verify_password(stored_pwd, entered_pwd):
    if len(stored_pwd) != len(entered_pwd):
        return False

    for i in range(0, len(stored_pwd)):
        if stored_pwd[i] != entered_pwd[i]:
            return False
            
    return True


def guess_size():
    buffer = []

    # Try every possible lengths of the password
    for i in range(1, MAX_LENGTH_TO_ATTEMPT + 1):
        entered_pwd = '0' * i

        t1 = perf_counter()

        for i in range(0, 1000):
            verify_password(USER_PASSWORD, entered_pwd)

        t2 = perf_counter()
        buffer.append(t2 - t1)

    # If the password length is correct, then the function will have the longest execution time
    longest = buffer.index(max(buffer)) + 1
    return longest

def guess_character(pre, length):
    medians = []
    for i in range(0, len(dictionary)):
        character = dictionary[i]

        buffer = []
        for i in range(0, 100000):
            t1 = perf_counter()
            guess_pwd = (pre + character).ljust(length, '_')

            verify_password(USER_PASSWORD, guess_pwd)
            t2 = perf_counter()
            buffer.append(t2 - t1)
        medians.append(median(buffer))

    longest = medians.index(max(medians))
    return dictionary[longest]

length = guess_size()
PREFIX = USER_PASSWORD[0]
pre = PREFIX

for i in range(1, length):
    guessed = guess_character(PREFIX, length)
    pre += guessed
    print(pre)