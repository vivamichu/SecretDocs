from cx_Freeze import setup, Executable

base = None

executables = [Executable("test.py", base=base, icon="secretdocs.ico")]

setup(
    name="SecretDocs",
    version="1.0",
    description="Safe and Fast Encryption/Decryption",
    executables=executables
)
