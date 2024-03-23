# Created by Ayaulym Raikhankyzy

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showerror, showinfo
from rsa import rsa_encryption, rsa_decryption
from fernet import fernet_encryption, fernet_decryption
from hybrid import hybrid_encrypt, hybrid_decrypt


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('SecretDocs')
        window_width = 600
        window_height = 400

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)

        self.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
        self.resizable(1, 0)
        self.attributes("-alpha", 0.97)
        self.create_widgets()

    def reset_application(self):
        self.destroy()
        self.__init__()

    def create_widgets(self):
        notebook = ttk.Notebook(self)
        notebook.pack(fill='both', expand=True)

        page1 = ttk.Frame(notebook)
        page1.rowconfigure(4)
        page1.columnconfigure(0, weight=1)
        page1.columnconfigure(1, weight=1)
        notebook.add(page1, text='Encryption')

        page2 = ttk.Frame(notebook)
        page2.rowconfigure(5)
        page2.columnconfigure(0, weight=1)
        page2.columnconfigure(1, weight=1)
        notebook.add(page2, text='Decryption')

        self.create_page1_widgets(page1)
        self.create_page2_widgets(page2)

    def create_page1_widgets(self, page):
        style = ttk.Style()
        style.configure("Sensitive.TButton", padding=5,
                        bordercolor='blue', borderwidth=2)

        title_label = ttk.Label(page, text="Encryption",
                                font=('Helvetica', 20))
        title_label.grid(row=0, columnspan=2, padx=20, pady=20)

        input_label = ttk.Label(page, text="Choose a file to encrypt")
        input_label.grid(row=1, column=0, sticky=tk.E, padx=5, pady=5)

        open_button = ttk.Button(
            page, text='Browse', command=lambda: get_input_file(input_label))
        open_button.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)

        output_label = ttk.Label(page, text="Choose an output directory")
        output_label.grid(row=2, column=0, sticky=tk.E, padx=5, pady=5)

        output_button = ttk.Button(
            page, text='Browse', command=lambda: get_output_directory(output_label))
        output_button.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)

        lf = ttk.Labelframe(page, text='Choose an encryption algorithm:')
        lf.grid(row=3, columnspan=2, padx=20, pady=20)

        encryption_type = tk.StringVar()
        encryption_types = ('RSA', 'Fernet', 'Hybrid')
        grid_column = 0
        for type in encryption_types:
            radio = ttk.Radiobutton(
                lf, text=type, value=type, variable=encryption_type)
            radio.grid(column=grid_column, row=3, ipadx=10, ipady=10)
            grid_column += 1

        encrypt_button = ttk.Button(page, text='Encrypt', command=lambda: encrypt_file(self,
                                                                                       input_filename, output_directory, encryption_type.get()))
        encrypt_button.grid(row=4, rowspan=2, columnspan=2, padx=10, pady=10)

    def create_page2_widgets(self, page):
        title_label = ttk.Label(page, text="Decryption",
                                font=('Helvetica', 20))
        title_label.grid(row=0, columnspan=2, padx=20, pady=20)

        input_label = ttk.Label(
            page, text="Choose an encrypted file (for RSA only)")
        input_label.grid(row=1, column=0, sticky=tk.E, padx=5, pady=5)

        open_button = ttk.Button(
            page, text='Browse', command=lambda: get_encrypted_file(input_label))
        open_button.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)

        output_label = ttk.Label(page, text="Choose a directory with keys")
        output_label.grid(row=2, column=0, sticky=tk.E, padx=5, pady=5)

        output_button = ttk.Button(
            page, text='Browse', command=lambda: get_output_directory(output_label))
        output_button.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)

        token_label = ttk.Label(
            page, text="Choose a token (for fernet/hybrid only)")
        token_label.grid(row=3, column=0, sticky=tk.E, padx=5, pady=5)

        token_button = ttk.Button(
            page, text='Browse', command=lambda: get_token(token_label))

        token_button.grid(row=3, column=1, sticky=tk.W, padx=5, pady=5)

        lf = ttk.Labelframe(page, text='Choose an encryption algorithm:')
        lf.grid(row=4, columnspan=2, padx=20, pady=20)

        encryption_type = tk.StringVar()
        encryption_types = ('RSA', 'Fernet', 'Hybrid')
        grid_column = 0
        for type in encryption_types:
            radio = ttk.Radiobutton(
                lf, text=type, value=type, variable=encryption_type)
            radio.grid(column=grid_column, row=3, ipadx=10, ipady=10)
            grid_column += 1

        encrypt_button = ttk.Button(page, text='Decrypt', command=lambda: decrypt_file(self,
                                                                                       output_directory, encryption_type.get(), encrypted_file=encrypted_file) if encryption_type.get() == "RSA" else decrypt_file(self, output_directory, encryption_type.get(), token=token_filename))
        encrypt_button.grid(row=5, rowspan=2, columnspan=2,
                            padx=10, pady=10, sticky=tk.N)


def get_input_file(input_label):
    filetypes = (('text files', '*.txt'), ('All files', '*.*'))
    global input_filename
    input_filename = fd.askopenfilename(
        title='Open a file', initialdir='/', filetypes=filetypes)
    input_label.config(text=input_filename)


def get_encrypted_file(encrypt_label):
    global encrypted_file
    encrypted_file = fd.askopenfilename(
        title='Open a file', initialdir='/')
    encrypt_label.config(text=encrypted_file)


def get_token(token_label):
    global token_filename
    token_filename = fd.askopenfilename(
        title='Open a file', initialdir='/'
    )
    token_label.config(text=token_filename)


def get_output_directory(output_label):
    global output_directory
    output_directory = fd.askdirectory(
        initialdir="/", title="Select Output Directory")
    output_label.config(text=output_directory)


def create_application():
    app = App()
    app.mainloop()


def encrypt_file(self, input_filename, output_directory, encryption_type):
    if not input_filename:
        showerror("Error", "Please choose an input file.")
        return
    if not output_directory:
        showerror("Error", "Please choose an output directory.")
        return
    if encryption_type == 'RSA':
        result = rsa_encryption(input_filename, output_directory)
        if result == 1:
            showinfo(title="Success!", message="File encrypted using RSA!")
        else:
            showinfo(title="Failed!", message=result)
    elif encryption_type == 'Fernet':
        result = fernet_encryption(input_filename, output_directory)
        if result == 1:
            showinfo(title="Success!", message="File encrypted using Fernet!")
        else:
            showinfo(title="Failed!", message=result)
    elif encryption_type == 'Hybrid':
        result = hybrid_encrypt(input_filename, output_directory)
        if result == 1:
            showinfo(title="Success!",
                     message="File encrypted using Hybrid mode!")
        else:
            showinfo(title="Failed!", message=result)
    self.reset_application()


def decrypt_file(self, dir_keys, encryption_type, encrypted_file=None, token=None):
    if not dir_keys:
        showerror("Error", "Please choose a directory with keys.")
        return
    if encryption_type == 'RSA':
        if not encrypted_file:
            showerror("Error", "Please choose an encrypted file.")
            return
        result = rsa_decryption(encrypted_file, dir_keys)
        if result == 1:
            showinfo(title="Success!", message="File decrypted using RSA!")
        else:
            showinfo(title="Failed!", message=result)
    elif encryption_type == "Fernet":
        if not token:
            showerror("Error", "Please choose a token file.")
            return
        result = fernet_decryption(token, dir_keys)
        if result == 1:
            showinfo(title="Success!", message="File decrypted using Fernet!")
        else:
            showinfo(title="Failed!", message=result)
    elif encryption_type == "Hybrid":
        if not token:
            showerror("Error", "Please choose a token file.")
            return
        result = hybrid_decrypt(token, dir_keys)
        if result == 1:
            showinfo(title="Success!", message="File decrypted using Hybrid!")
        else:
            showinfo(title="Failed!", message=result)

    self.reset_application()


if __name__ == "__main__":
    create_application()
