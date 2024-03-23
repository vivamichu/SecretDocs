import os
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization


def generate_keys(output_directory):
    """Generates a secure RSA key pair and stores them in separate files."""
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=4096  # Adjust key size as needed
    )
    public_key = private_key.public_key()

    private_key_path = os.path.join(output_directory, "private_key.pem")
    public_key_path = os.path.join(output_directory, "public_key.pem")

    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    with open(private_key_path, "wb") as key_file:
        key_file.write(pem)

    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    with open(public_key_path, "wb") as key_file:
        key_file.write(pem)

    print(
        f"RSA keys generated and saved to {private_key_path} and {public_key_path}")


def load_public_key(output_directory):
    """Loads the public key from the file."""
    try:
        with open(os.path.join(output_directory, "public_key.pem"), "rb") as key_file:
            pem = key_file.read()
            public_key = serialization.load_pem_public_key(pem)
        return public_key
    except FileNotFoundError:
        print("Public key file not found. Please generate keys first.")
        return None


def load_private_key(output_directory):
    """Loads the private key from the file."""
    try:
        with open(os.path.join(output_directory, "private_key.pem"), "rb") as key_file:
            pem = key_file.read()
            private_key = serialization.load_pem_private_key(
                pem, password=None)
        return private_key
    except FileNotFoundError:
        print("Private key file not found. Please generate keys first.")
        return None


def rsa_encryption(filename, output_directory):
    generate_keys(output_directory)
    """Encrypts a file using RSA."""
    public_key = load_public_key(output_directory)
    if not public_key:
        return
    try:
        with open(filename, "rb") as f:
            text = f.read()
        ciphertext = public_key.encrypt(
            text,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        output_filename = os.path.join(
            output_directory, f"{os.path.basename(filename)}.rsa_encrypted")
        with open(output_filename, "wb") as f:
            f.write(ciphertext)
        print(f"File encrypted using RSA: {output_filename}")
        return 1
    except FileNotFoundError:
        return f"A file: {filename} is not found!"
    except ValueError as e:  # Catch input too large for RSA
        return f"File is too big, choose different encryption type!"
    except Exception as e:
        return f"Encryption failed: {e}"


def rsa_decryption(filename, output_directory):
    """Decrypts a file using RSA."""
    private_key = load_private_key(output_directory)
    if not private_key:
        return
    try:
        with open(filename, "rb") as f:
            binary_data = f.read()
        try:
            plaintext = private_key.decrypt(
                binary_data,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            output_filename = os.path.join(
                output_directory, f"rsa_decrypted_{os.path.splitext(os.path.basename(filename))[0]}")
            with open(output_filename, "wb") as f:
                f.write(plaintext)
            print(f"File decrypted using RSA: {output_filename}")
            return 1
        except ValueError as e:  # Catch input too large for RSA
            return f"Decryption failed: {e}"
        except Exception as e:
            return f"Decryption failed: {e}"
    except FileNotFoundError:
        return f"A file: {filename} is not found!"
