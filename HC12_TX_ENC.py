import maes
import ubinascii
from machine import UART
import time

def pad_to_multiple_of_16(input_string):
    while len(input_string) % 16 != 0:
        input_string += b' '  # Ensure input_string is in bytes
    return input_string

key = b"af445057fc183d72"
iv = b"1234567890abcdef"

# Input plaintext
input_text = b'This is a test! What could possibly go wrong?'

# Padding input string to ensure its length is a multiple of 16
padded_input_text = pad_to_multiple_of_16(input_text)

cryptor = maes.new(key, maes.MODE_CBC, IV=iv)
ciphertext = cryptor.encrypt(padded_input_text)

# Encode ciphertext and IV as hexadecimal strings
encoded_ciphertext = ubinascii.hexlify(ciphertext)
encoded_iv = ubinascii.hexlify(iv)

# Initialize UART
uart = UART(0, 9600, timeout=400)

# Transmit the encrypted text and IV over UART
uart.write(encoded_ciphertext + b'\n')
uart.write(encoded_iv + b'\n')

# Printing for verification (optional)
print("Encrypted Text:", encoded_ciphertext)
print("IV:", encoded_iv)


# Convert the hexadecimal strings back to bytes
received_encrypted_text = ubinascii.unhexlify(encoded_ciphertext)
received_iv = ubinascii.unhexlify(encoded_iv)

# Decrypt the ciphertext using the known key and IV
decryptor = maes.new(key, maes.MODE_CBC, IV=received_iv)
decrypted_text = decryptor.decrypt(received_encrypted_text)

# Print the decrypted text
# print("Decrypted Text:", decrypted_text)

# Convert the list of integers to bytes
encoded_bytes = bytes(decrypted_text)

# Decode the bytes using UTF-8 encoding
decoded_text = encoded_bytes.decode('utf-8')

print(decoded_text)