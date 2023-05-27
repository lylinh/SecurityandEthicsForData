import socket
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import os

class Master:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = None
        self.client_socket = None
        self.client_address = None

    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(1)
        print("Master listening on {}:{}".format(self.host, self.port))

        self.client_socket, self.client_address = self.server_socket.accept()
        print("Client connected from:", self.client_address)

    def send_message_encode(self, message):    
        self.client_socket.send(message)

    def send_message(self, message):
        print("data send before encrpy:",message)
        data = self.encode(bytes(message, 'utf-8'))
        print("data send:",data,"\n")
        self.client_socket.send(data)

    def receive_message(self):
        data = self.client_socket.recv(1024)
        print("data receive:",data)
        return self.decode(data).decode()

    def stop(self):
        self.client_socket.close()
        self.server_socket.close()
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
master = Master('localhost', 8000)
master.start()

key = os.urandom(32)
iv = os.urandom(16)
master.aes_cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend = default_backend())

print("key:",key)
print("iv:",iv)

master.send_message_encode(key)
master.send_message_encode(iv)


while True:
    message = input("You: ")
    master.send_message(message)

    if message.lower() == 'bye':
        break

    response = master.receive_message()
    print("Client:", response)

master.stop()