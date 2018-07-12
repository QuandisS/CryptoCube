import os, random

class Cube():

    def __init__(self):
        self.data = {'0.0.0': ' ', '0.1.0': ' ', '1.1.0': ' ',
                     '1.0.0': ' ', '0.0.1': ' ', '0.1.1': ' ',
                     '1.1.1': ' ', '1.0.1': ' '}

    def read(self):
        res = self.data['0.0.0'] + self.data['0.1.0'] + self.data['1.1.0'] + self.data['1.0.0'] + self.data['0.0.1'] + self.data['0.1.1'] + self.data['1.1.1'] + self.data['1.0.1']
        return res

    def rotate(self, way):
        #copy
        data000c = self.data['0.0.0']
        data010c = self.data['0.1.0']
        data110c = self.data['1.1.0']
        data100c = self.data['1.0.0']
        data001c = self.data['0.0.1']
        data011c = self.data['0.1.1']
        data111c = self.data['1.1.1']
        data101c = self.data['1.0.1']
        #copy end

        if way == "U":
            self.data['0.0.0'] = data001c
            self.data['0.1.0'] = data000c
            self.data['1.1.0'] = data100c
            self.data['1.0.0'] = data101c
            self.data['0.0.1'] = data011c
            self.data['0.1.1'] = data010c
            self.data['1.1.1'] = data110c
            self.data['1.0.1'] = data111c

        if way == "D":
            self.data['0.0.0'] = data010c
            self.data['0.1.0'] = data011c
            self.data['1.1.0'] = data111c
            self.data['1.0.0'] = data110c
            self.data['0.0.1'] = data000c
            self.data['0.1.1'] = data001c
            self.data['1.1.1'] = data101c
            self.data['1.0.1'] = data100c

        if way == "L":
            self.data['0.0.0'] = data100c
            self.data['0.1.0'] = data110c
            self.data['1.1.0'] = data111c
            self.data['1.0.0'] = data101c
            self.data['0.0.1'] = data000c
            self.data['0.1.1'] = data010c
            self.data['1.1.1'] = data011c
            self.data['1.0.1'] = data001c

        if way == "R":
            self.data['0.0.0'] = data001c
            self.data['0.1.0'] = data011c
            self.data['1.1.0'] = data010c
            self.data['1.0.0'] = data000c
            self.data['0.0.1'] = data101c
            self.data['0.1.1'] = data111c
            self.data['1.1.1'] = data110c
            self.data['1.0.1'] = data100c


    def return_data(self):
        return self.data

    def set_data(self, symb, pos):
        self.data.update({pos: symb})

def key_output_in_file(data, name):
    os.mkdir(name)

    f = open(name + '/' + name + '.cck', 'w')

    # .ccd = CryptoCubeData format #
    # .cck = CryptoCubeKey  format #

    if type(data) == list:
        f.writelines(data)
    else:
        print("[ERROR]data par. must be LIST type")

    f.close()

def msg_output_in_file(data, name):
    f = open(name + '/' + name + '.ccm', 'w')

    # .ccm = CryptoCubeMessage format #
    # .cck = CryptoCubeKey     format #

    if type(data) == list:
        f.writelines(data)
    else:
        print("[ERROR]data par. must be LIST type")

    f.close()

def encrypt(data, filename):
    print('\n'*2 + 'Encrypting...')
    ways = ['L', 'R', 'U', 'D']

    cubes_number = len(data)//8
    if len(data) % 8 != 0:
        cubes_number += 1

    print('Cubes number:', cubes_number)

    cubes = []

    msg_data = list(data)

    symb_number = 0

    for i in range(cubes_number):
        cube = Cube()

        for position in cube.return_data().keys():
            if symb_number == len(msg_data):
                break
            else:
                cube.set_data(msg_data[symb_number], position)
                print("Value:<" + msg_data[symb_number] +"> set at pos[" + position + '] at cube ' + str(i))
                symb_number += 1
        cubes.append(cube)

    print('Cubes in list:', len(cubes))
    print('Multiple rotation:', multiple_rotation)

    pre_read = ""

    for cu in cubes:
        pre_read += cu.read()

    print('Pre-read: ', pre_read)

    key = ''

    if not multiple_rotation:
        generations = random.randint(3, 10)
        key += 'A|'
        for i in range(generations):
            way_num = random.randint(0, 3)
            way = ways[way_num]
            if i == generations - 1:
                key += way
            else:
                key += way + ':'
            for cu in cubes:
                cu.rotate(way)

    print('Key:', key)

    key = list(key)

    post_read = ''
    for cu in cubes:
        post_read += cu.read()
    print('Ready msg:', post_read)

    key_output_in_file(key, filename)
    msg_output_in_file(list(post_read), filename)

    print('\n'*2)

def decrypt(filename, keyname):
    print('\n'*2 + 'Decrypting...')
    f = open(filename, 'r')
    msg = f.read()
    f.close()
    f = open(keyname, 'r')
    key = f.read()
    f.close()

    print('Msg='+str(msg))
    print('Key='+str(key))

    msg = str(msg)
    msg = list(msg)

    cubes_number = len(msg) // 8
    if len(msg) % 8 != 0:
        cubes_number += 1

    symb_number = 0
    cubes = []

    for i in range(cubes_number):
        cube = Cube()

        for position in cube.return_data().keys():
            if symb_number == len(msg):
                break
            else:
                cube.set_data(msg[symb_number], position)
                print("Value:<" + msg[symb_number] + "> set at pos[" + position + '] at cube ' + str(i))
                symb_number += 1
        cubes.append(cube)

    pre_read = ""

    for cu in cubes:
        pre_read += cu.read()

    print('Pre-read: ', pre_read)

    key = str(key)
    key = key.split('|')

    if key[0] == 'A':
        print('Using NO multiple rotation algorithm...')
        key.pop(0)
        key = key[0]
        key_commands = key.split(':')
        print('Key commands:', key_commands)
        decrypt_commands = []
        for bar in key_commands:
            if bar == 'U':
                decrypt_commands.append('D')
            if bar == 'D':
                decrypt_commands.append('U')
            if bar == 'L':
                decrypt_commands.append('R')
            if bar == 'R':
                decrypt_commands.append('L')

        print('Decrypt commands:', decrypt_commands)
        decrypt_commands.reverse()
        print('Reversed decrypt commands:', decrypt_commands)
        print('Rotating...')

        for foo in decrypt_commands:
            for cu in cubes:
                cu.rotate(foo)

        post_read = ''

        for cu in cubes:
            post_read += cu.read()

        print('\n' +"========")
        print('Decrypted message:', post_read)
        print("========" + '\n')

        print('\n'*2)
    pass


#data  = ['1', '2', '3']
#output_in_file(data, "test")


#####
multiple_rotation = False
#####



while True:

    user_input = input("Encrypt/Decrypt/Quit" + "\n" + "[E/D/Q]" + ">>")

    if user_input == "E" or user_input == "e":
        print("Please, enter your msg:")
        data = input(">>")
        print("Please, enter file name:")
        filename = input(">>")
        encrypt(data, filename)

    if user_input == 'd' or user_input == 'D':
        filename = input("Please, enter .ccm file full name>>")
        keyname = input("Please, enter .cck file full name>>")
        decrypt(filename, keyname)

    if user_input == 'Q' or user_input == 'q':
        break

    if user_input == 'dev' or user_input == 'DEV':
        while True:
            user_input = input('CC-Dev-console>>')

            if user_input == 'q' or user_input == 'Q':
                break

            if user_input == 'mr on':
                multiple_rotation = True
                print('Multiple rotation:', multiple_rotation)

            if user_input == 'mr off':
                multiple_rotation = False
                print('Multiple rotation:', multiple_rotation)