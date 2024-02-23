import maes
import ubinascii
import time
from machine import UART

# Known key and IV
key = b"af445057fc183d72"


# Initialize UART
uart = UART(0, 9600, timeout=400)

# Wait until there's data available in UART buffer
while not uart.any():
    time.sleep(1)
    pass  # Do nothing, just wait

# Read the encrypted text and IV as hexadecimal strings from UART
received_encrypted_text_hex = uart.readline()
received_iv_hex = uart.readline()

if received_encrypted_text_hex is not None and received_iv_hex is not None:
    # Strip any leading/trailing whitespace
    received_encrypted_text_hex = received_encrypted_text_hex.strip()
    received_iv_hex = received_iv_hex.strip()

    # Convert the hexadecimal strings back to bytes
    received_encrypted_text = ubinascii.unhexlify(received_encrypted_text_hex)
    received_iv = ubinascii.unhexlify(received_iv_hex)

    # Decrypt the ciphertext using the known key and IV
    decryptor = maes.new(key, maes.MODE_CBC, IV=received_iv)
    decrypted_text = decryptor.decrypt(received_encrypted_text)

    # Print the decrypted text
    # Convert the list of integers to bytes
    encoded_bytes = bytes(decrypted_text)

    # Decode the bytes using UTF-8 encoding
    decoded_text = encoded_bytes.decode('utf-8')

    print(decoded_text)
else:
    print("Error: No data received from UART.")
