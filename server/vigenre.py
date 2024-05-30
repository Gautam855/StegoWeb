def generate_vigenere_table():
    table = []
    for i in range(26):
        row = [(chr((i + j) % 26 + 65)) for j in range(26)]
        table.append(row)
    return table

def extend_key(message, key):
    key = key.upper()
    return (key * (len(message) // len(key)) + key[:len(message) % len(key)]).upper()

def encrypt_vigenere(message, key):
    table = generate_vigenere_table()
    message = message.upper()
    key = extend_key(message, key)
    
    encrypted_message = []
    for i, letter in enumerate(message):
        if letter.isalpha():
            row = ord(key[i]) - 65
            col = ord(letter) - 65
            encrypted_message.append(table[row][col])
        else:
            encrypted_message.append(letter)  # Non-alphabet characters are not encrypted

    return ''.join(encrypted_message)

def decrypt_vigenere(encrypted_message, key):
    table = generate_vigenere_table()
    encrypted_message = encrypted_message.upper()
    key = extend_key(encrypted_message, key)
    
    decrypted_message = []
    for i, letter in enumerate(encrypted_message):
        if letter.isalpha():
            row = ord(key[i]) - 65
            col = table[row].index(letter)
            decrypted_message.append(chr(col + 65))
        else:
            decrypted_message.append(letter)  # Non-alphabet characters are not decrypted

    return ''.join(decrypted_message)


