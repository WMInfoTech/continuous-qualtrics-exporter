import os

def secretsmanager(dir):
    secret_array = {}
    secretfiles = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]
    for secret in secretfiles:
        with open(os.path.join(dir, secret), 'r') as file:
            data = file.read().replace('\n', '').replace('\r', '')
            secret_array[secret] = data

    return secret_array


