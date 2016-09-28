from hashlib import sha1
from uuid import uuid4

def generate_token(*data):
    salt = str(uuid4())
    print('^')
    return sha1('|'.join([salt]+list(data)).encode('utf8')).hexdigest()

if __name__ == '__main__':
    for i in range(10):
        t = generate_token()
        print(t)
