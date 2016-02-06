import hashlib

secret = b'X\xf1\x8dp\xf6g\xc9\xc7\x9e\xf7\xdeC[\xf0\xf9\xb1U;\xbbna\x81b\x12\xab\x80\xe5\xb0\xd3Q\xfb\xb1'


def parse_on_off(s):
    if s == 'on':
        return True
    else:
        return False


def create_message(url, value):
    j = '{"value":%s}' % (repr(value))

    remainder = len(j) % 16

    j = j + '\x00' * (16 - remainder)

    #print('URL: %s' % url)
    #print('JSON: %s' % j)

    msg = "PUT %s HTTP:/1.0\nContent-Type: application/json\nContent-Length: 25\nUser-Agent: NefitEasy\n\n\n\n%s\n" % (url, encode(j).decode('utf-8'))

    return msg


def get_md5(data):
    m = hashlib.md5()
    m.update(data)

    return m.digest()
