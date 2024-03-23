
![Group 2493](https://github.com/vivamichu/SecretDocs/assets/92267183/46ca0dda-ac75-48e1-b8f2-895c18e31351)

# SecretDocs

This is a Python application that allows you to encrypt and decrypt documents securely. This README provides instructions on how to use the application and create an executable for easier usage.

## Usage

<img width="603" alt="image" src="https://github.com/vivamichu/SecretDocs/assets/92267183/ead982f0-f2f5-4911-bad6-03062ae41a88">
<img width="611" alt="image" src="https://github.com/vivamichu/SecretDocs/assets/92267183/3a942fd3-e515-4fa5-8b5d-dc92909952c0">


### Installation

1. Clone or download the SecretDocs repository to your local machine.

2. Install the required dependencies using pip:

   ```
   pip install -r requirements.txt
   ```

### Encryption

1. Run the `test.py` script:

   ```
   python test.py
   ```

2. Select the file, output directory for your encryption (we suggest using one folder per encrypted file).
3. There are 3 types of encryption algorithms provided: RSA, Fernet and Hybrid.

   RSA is an asymmetric cryptographic algorithm used to encrypt small sized documents. 
   Fernet is a symmetric encryption algorithm. It uses the same key for both encryption and decryption. It is suitable for large sized files, but less secure.
   Hybrid is a mode that combines both RSA and Fernet, making it the most secure encryption algorithm. It is also suitable for large sized files.

5. Once completed, the encrypted file will be saved with the relevant encryption type extension.

### Decryption

1. Run the `test.py` script:

   ```
   python test.py
   ```

2. Open the Decryption Page
3. Follow the instructions and choose relevant files, directories. 

4. Once completed, the decrypted file will be saved in the original directoty.

### Creating Executable

1. Install PyInstaller if you haven't already:

   ```
   pip install pyinstaller
   ```

2. Use PyInstaller to create an executable for the application:

   For Windows:

   ```
   pyinstaller --onefile --windowed --icon=icon.ico encrypt.py
   pyinstaller --onefile --windowed --icon=icon.ico decrypt.py
   ```

   For Linux:

   ```
   pyinstaller --onefile --windowed --icon=icon.ico encrypt.py
   pyinstaller --onefile --windowed --icon=icon.ico decrypt.py
   ```

   Replace `icon.ico` with the path to your custom icon file.

3. The executable will be created in the `dist` directory.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.



