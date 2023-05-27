import socket
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import os


class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_socket = None

    def connect(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))
        print("Connected to {}:{}".format(self.host, self.port))

    def send_message(self, message):
        print("data send before encrpy:",message)
        data = self.encode(bytes(message, 'utf-8'))
        print("data send:",data,"\n")
        self.client_socket.send(data)

    def receive_message_encode(self):
        data = self.client_socket.recv(1024)
        return data

    def receive_message(self):
        data = self.client_socket.recv(1024)
        print("data receive:",data)
        return self.decode(data).decode()

    def stop(self):
        self.client_socket.close()
        print("Connection closed.")


    def encode(self, encode_text):
        padder = padding.PKCS7(128).padder()
        padded_plaintext = padder.update(encode_text) + padder.finalize()
        encryptor = self.aes_cipher.encryptor()
        ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()
        return ciphertext

    def decode(self, decode_text):
        decryptor = self.aes_cipher.decryptor()
        decrypted_padded_text = decryptor.update(decode_text) + decryptor.finalize()
        unpadder = padding.PKCS7(128).unpadder()
        decrypted_text = unpadder.update(decrypted_padded_text) + unpadder.finalize()
        return decrypted_text

# Usage
client = Client('localhost', 8000)
client.connect()
key = client.receive_message_encode()
iv = client.receive_message_encode()
print("key:",key)
print("iv:",iv)

client.aes_cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend = default_backend())
while True:
    message = client.receive_message()
    print("Server message:", message)

    if message.lower() == 'bye':
        break

    user_input = input("Client message: ")
    client.send_message(user_input)

client.stop()