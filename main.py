
def luhn_checksum(card_number):
    """Calculate the Luhn checksum."""
    digits = [int(digit) for digit in str(card_number)]
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    total = sum(odd_digits)
    for digit in even_digits:
        total += sum(divmod(digit * 2, 10))
    return total % 10

def find_valid_digits(card_number):
    """Find valid digits. Well, try at least duh"""
    for i in range(len(card_number)):
        original_digit = int(card_number[i])
        for new_digit in range(10):
            if new_digit != original_digit:
                test_card_number = card_number[:i] + str(new_digit) + card_number[i+1:]
                if luhn_checksum(test_card_number) == 0:
                    return test_card_number
    return None

def diffie_hellman_protocol(p: int, g: int, bob_private_key: int, alice_private_key: int): 
    # Вычисление публичных ключей
    bob_public_key = pow(g, bob_private_key, p)
    alice_public_key = pow(g, alice_private_key, p)

    # Вычисление общего секретного ключа
    bob_shared_secret = calculate_shared_secret(alice_public_key, bob_private_key, p)
    alice_shared_secret = calculate_shared_secret(bob_public_key, alice_private_key, p)

    # Проверка общего секретного ключа
    assert bob_shared_secret == alice_shared_secret

    # Вывод общего секретного ключа
    print("Общий секретный ключ:", bob_shared_secret)

    # Сообщение для шифрования
    message = "HELLO"

    # Шифрование сообщения на стороне Боба с использованием алгоритма Цезаря
    encrypted_message = caesar_encrypt(message, bob_shared_secret)

    # Вывод зашифрованного сообщения
    print("Зашифрованное сообщение на стороне Боба:", encrypted_message)

    # Дешифровка сообщения на стороне Алисы
    decrypted_message = caesar_decrypt(encrypted_message, alice_shared_secret)

    # Вывод расшифрованного сообщения
    print("Расшифрованное сообщение на стороне Алисы:", decrypted_message)

# Функция для вычисления общего секретного ключа
def calculate_shared_secret(public_key, private_key, p):
    return pow(public_key, private_key, p)

# Функция для шифрования сообщения с помощью алгоритма Цезаря
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

# Функция для дешифрования сообщения с помощью алгоритма Цезаря
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

if __name__ == "__main__":
    # Параметры протокола
    p = 13
    g = 6
    bob_private_key = 5
    alice_private_key = 4

    diffie_hellman_protocol(p, g, bob_private_key, alice_private_key)


