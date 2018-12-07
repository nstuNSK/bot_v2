def get_user():
    f = open('/home/Main/Project/git/bot_v2/system/base.txt')
    line = f.read(4)
    return line

def get_password():
    f = open('/home/Main/Project/git/bot_v2/system/base.txt')
    line = f.readline()
    line = f.read(10)
    return line

def get_token():
    f = open('/home/Main/Project/git/bot_v2/system/token.txt')
    line = f.readline()
    return line

def get_nstu_url():
    f = open('/home/Main/Project/git/bot_v2/system/api.nstu.txt')
    line = f.readline()
    return line
