import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.asymmetric.padding import OAEP
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import (
    Encoding,
    PrivateFormat,
    PublicFormat,
    NoEncryption,
    load_pem_public_key,
    load_pem_private_key,
)


def generate_keys(output_directory):
    """Generates a secure RSA key pair and stores them in separate files in the specified output directory."""
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,  # Adjust key size as needed
    )
    public_key = private_key.public_key()

    private_key_filename = os.path.join(output_directory, "private_key.pem")
    public_key_filename = os.path.join(output_directory, "public_key.pem")

    pem = private_key.private_bytes(
        encoding=Encoding.PEM,
        format=PrivateFormat.PKCS8,
        encryption_algorithm=NoEncryption(),
    )
    with open(private_key_filename, "wb") as key_file:
        key_file.write(pem)

    pem = public_key.public_bytes(
        encoding=Encoding.PEM,
        format=PublicFormat.SubjectPublicKeyInfo,
    )
    with open(public_key_filename, "wb") as key_file:
        key_file.write(pem)

    print(
        f"RSA keys generated and saved to {private_key_filename} and {public_key_filename}")


def load_public_key(output_directory):
    """Loads the public key from the file in the specified output directory."""
    public_key_filename = os.path.join(output_directory, "public_key.pem")
    try:
        with open(public_key_filename, "rb") as key_file:
            pem = key_file.read()
            public_key = load_pem_public_key(pem)
        return public_key
    except FileNotFoundError:
        raise FileNotFoundError(
            "Public key file not found. Please generate keys first.")
    except Exception as e:
        raise Exception(f"Error loading public key: {e}")


def load_private_key(output_directory):
    """Loads the private key from the file in the specified output directory."""
    private_key_filename = os.path.join(output_directory, "private_key.pem")
    try:
        with open(private_key_filename, "rb") as key_file:
            pem = key_file.read()
            private_key = load_pem_private_key(pem, password=None)
        return private_key
    except FileNotFoundError:
        raise FileNotFoundError(
            "Private key file not found. Please generate keys first.")
    except Exception as e:
        raise Exception(f"Error loading private key: {e}")


def hybrid_encrypt(filename, output_directory):
    generate_keys(output_directory)
    """Encrypts a file using a hybrid approach of RSA and Fernet in the specified output directory."""
    public_key = load_public_key(output_directory)
    if not public_key:
        return
    try:
        with open(filename, "rb") as f:
            data = f.read()
        fernet_key = Fernet.generate_key()
        fernet = Fernet(fernet_key)
        encrypted_data = fernet.encrypt(data)
        ciphertext = public_key.encrypt(
            fernet_key,
            OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )
        output_filename_data = os.path.join(
            output_directory, f"{os.path.basename(filename)}.hybrid_token")
        with open(output_filename_data, "wb") as f:
            f.write(encrypted_data)
        output_filename_key = os.path.join(
            output_directory, f"{os.path.basename(filename)}.hybrid_encrypted_key")
        with open(output_filename_key, "wb") as f:
            f.write(ciphertext)
        print(
            f"File encrypted using hybrid RSA-Fernet: {output_filename_data}")
        return 1
    except Exception as e:
        return f"Encryption failed: {e}"


def hybrid_decrypt(data_filename, output_directory):
    """Decrypts a file encrypted with hybrid RSA-Fernet in the specified output directory."""
    private_key = load_private_key(output_directory)
    if not private_key:
        return
    try:
        key_filename = os.path.join(
            output_directory, f"{os.path.splitext(os.path.basename(data_filename))[0]}.hybrid_encrypted_key")
        with open(data_filename, "rb") as f:
            encrypted_data = f.read()
        with open(key_filename, "rb") as f:
            encrypted_key = f.read()
        decrypted_key = private_key.decrypt(
            encrypted_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        f_key = Fernet(decrypted_key)
        message = f_key.decrypt(encrypted_data)
        output_file = os.path.join(
            output_directory, f"hybrid_decrypted_{os.path.splitext(os.path.basename(data_filename))[0]}")
        with open(output_file, "wb") as f:
            f.write(message)
        print(f"File decrypted using hybrid RSA-Fernet: {output_file}")
        return 1
    except Exception as e:
        return f"Decryption failed: {e}"
