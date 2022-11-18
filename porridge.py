
import argparse
from porridge import Porridge
from timeit import timeit


parser = argparse.ArgumentParser(
    prog="Porridge Cli",
    description="A2"
)

parser.add_argument('cmd')
parser.add_argument('password')
parser.add_argument('key')
parser.add_argument('secret')

args = parser.parse_args()

STORE_PATH = './porridge.keys'

def store(password, key, secret):
    try:
        porridge = Porridge(key + ":" + secret)
        """
        Q.1.d test
        porridge = Porridge(key + ":" + secret, time_cost=4, memory_cost=1024, parallelism=16)
        porridge = Porridge(key + ":" + secret, time_cost=8, memory_cost=1024, parallelism=16)
        porridge = Porridge(key + ":" + secret, time_cost=16, memory_cost=1024, parallelism=16)
        porridge = Porridge(key + ":" + secret, time_cost=20, memory_cost=1024, parallelism=16)
        """
        boiled_password = porridge.boil(password)

        with open(STORE_PATH, 'a') as file:
            file.write(boiled_password)
            file.write('\n')
    except:
        print("Failed")
        exit(-1)

    print("Success", end='')


def verify(password, key, secret):
    try:
        porridge = Porridge(key + ":" + secret)
        """
        Q.1.d test
        porridge = Porridge(key + ":" + secret, time_cost=4, memory_cost=1024, parallelism=16)
        porridge = Porridge(key + ":" + secret, time_cost=8, memory_cost=1024, parallelism=16)
        porridge = Porridge(key + ":" + secret, time_cost=16, memory_cost=1024, parallelism=16)
        porridge = Porridge(key + ":" + secret, time_cost=20, memory_cost=1024, parallelism=16)
        """
        with open(STORE_PATH, 'r') as file:
            line = file.readline()

            match = ''
            while line:
                if line.find('keyid=' + key) != -1:
                    match = line
                    break

                line = file.readline()

            if match == '':
                print("Not Found", end='')
                exit(-1)

            if (porridge.verify(password, match)):
                print("Verified", end='')
            else:
                print("Not Valid")
    except Exception as e:
        print("Failed")
        exit(-1)

cmds = {
    "store": store,
    "verify": verify
}

cmds[args.cmd](args.password, args.key, args.secret)
# print(timeit.timeit('output = 10*5'))