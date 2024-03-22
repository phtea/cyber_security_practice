def diffie_hellman_protocol(p: int, g: int, bob_private_key: int, alice_private_key: int): 

    def calculate_shared_secret(public_key, private_key, p):
        return pow(public_key, private_key, p)
    
    def caesar_encrypt(message, key):
        encrypted_message = ""
        for char in message:
            if char.isalpha():
                shift = ord('A') if char.isupper() else ord('a')
                encrypted_char = chr((ord(char) - shift + key) % 26 + shift)
                encrypted_message += encrypted_char
            else:
                encrypted_message += char
        return encrypted_message
    
    def caesar_decrypt(encrypted_message, key):
        decrypted_message = ""
        for char in encrypted_message:
            if char.isalpha():
                shift = ord('A') if char.isupper() else ord('a')
                decrypted_char = chr((ord(char) - shift - key) % 26 + shift)
                decrypted_message += decrypted_char
            else:
                decrypted_message += char
        return decrypted_message

    bob_public_key = pow(g, bob_private_key, p)
    alice_public_key = pow(g, alice_private_key, p)

    bob_shared_secret = calculate_shared_secret(alice_public_key, bob_private_key, p)
    alice_shared_secret = calculate_shared_secret(bob_public_key, alice_private_key, p)

    assert bob_shared_secret == alice_shared_secret

    print("Общий секретный ключ:", bob_shared_secret)

    message = "HELLO"
    encrypted_message = caesar_encrypt(message, bob_shared_secret)
    print("Зашифрованное сообщение на стороне Боба:", encrypted_message)

    decrypted_message = caesar_decrypt(encrypted_message, alice_shared_secret)
    print("Расшифрованное сообщение на стороне Алисы:", decrypted_message)
    return decrypted_message