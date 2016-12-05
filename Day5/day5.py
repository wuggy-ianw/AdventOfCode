import hashlib


def day5a_solver(room_id, checkpoint_test = None, password_update=lambda pwd,hsh: pwd + hsh[5]):
    index = 0
    password = ''

    while(len(password)<8 or '_' in password):
        tohash = (room_id + str(index))
        hsh = hashlib.md5(tohash.encode('ascii')).hexdigest()

        if hsh.startswith('00000'):
            password = password_update(password,hsh)

        if checkpoint_test:
            checkpoint_test(index, tohash, hsh, password)

        index += 1

    return password


def day5b_solver(room_id, checkpoint_test = None):
    def positional_password_updater(pwd,hsh):
        if pwd=='':
            pwd='________'
        pos = int(hsh[5],16)
        if pos<8 and pwd[pos]=='_':
            pwd = pwd[0:pos] + hsh[6] + pwd[pos+1:8]
        return pwd

    return day5a_solver(room_id, checkpoint_test, password_update=positional_password_updater)



if __name__ == '__main__':
    print(day5a_solver('uqwqemis'))
    print(day5b_solver('uqwqemis'))
