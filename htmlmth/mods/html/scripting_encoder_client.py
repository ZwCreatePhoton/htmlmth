import sys

import requests


def encode(script, server, port):
    r = requests.post("http://{}:{}/encode".format(server, port), data={'script': script})
    encoded_script = r.text
    return encoded_script

if __name__ == '__main__':
    filepath = sys.argv[1]
    server = sys.argv[2]
    port = int(sys.argv[3])
    with open(filepath, "r") as f:
        script = f.read()
        encoded_script = encode(script, server, port)
        print(encoded_script)
