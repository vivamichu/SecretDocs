import os
from cryptography.fernet import Fernet


def generate_key(output_directory):
    """Generates a secure Fernet key and stores it in a file."""
    key = Fernet.generate_key()
    key_filename = os.path.join(output_directory, "fernet_key.key")
    with open(key_filename, "wb") as key_file:
        key_file.write(key)
    print("Fernet key generated and saved to fernet_key.key")


def load_key(output_directory):
    """Loads the Fernet key from the file."""
    key_filename = os.path.join(output_directory, "fernet_key.key")
    try:
        with open(key_filename, "rb") as key_file:
            key = key_file.read()
        return Fernet(key)
    except FileNotFoundError:
        print("Fernet key file not found. Please generate a key first.")
        return None


def fernet_encryption(filename, output_directory):
    generate_key(output_directory)
    """Encrypts a file using Fernet."""
    f_key = load_key(output_directory)
    if not f_key:
        return
    try:
        with open(filename, "rb") as f:
            text = f.read()
            if not text:
                print("File is empty. Cannot encrypt.")
                return
        token = f_key.encrypt(text)
        output_filename = os.path.join(
            output_directory, f"token_{os.path.basename(filename)}")
        with open(output_filename, "wb") as f_out:
            f_out.write(token)
        print(f"File encrypted using Fernet: {output_filename}")
        return 1
    except FileNotFoundError:
        return f"A file: {filename} is not found!"
    except Exception as e:
        return f"Encryption failed: {e}"


def fernet_decryption(filename, output_directory):
    """Decrypts a file using Fernet."""
    f_key = load_key(output_directory)
    if not f_key:
        return
    try:
        with open(filename, "rb") as f:
            token = f.read()
            if not token:
                print("Token is empty. Cannot decrypt.")
                return
        message = f_key.decrypt(token)
        output_filepath = os.path.join(
            output_directory, f"fernet_decrypted_{os.path.splitext(os.path.basename(filename))[0]}")
        with open(output_filepath, "wb") as f_out:
            f_out.write(message)
        print(f"File decrypted using Fernet: {output_filepath}")
        return 1
    except FileNotFoundError:
        return f"A file: {filename} is not found!"
    except Exception as e:
        return f"Decryption failed: {e}"
