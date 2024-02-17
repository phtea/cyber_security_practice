def luhn_checksum(card_number):
    """Calculate the Luhn checksum."""
    digits = [int(digit) for digit in str(card_number)]
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    total = sum(odd_digits)
    for digit in even_digits:
        total += sum(divmod(digit * 2, 10))
    return total % 10

def find_invalid_digit(card_number):
    valid_cards_list = []
    for i in range(len(card_number)):
        original_digit = int(card_number[i])
        for new_digit in range(10):
            if new_digit != original_digit:
                test_card_number = card_number[:i] + str(new_digit) + card_number[i+1:]
                if luhn_checksum(test_card_number) == 0:
                    valid_cards_list.append(test_card_number)
    return valid_cards_list if valid_cards_list else None

if __name__ == "__main__":
    card_number = input("Введите номер карты: ")
    invalid_card_number = find_invalid_digit(card_number)
    if invalid_card_number is not None:
        print(f"Номер карты неверен. Правильный номер карты где-то в этом списке: {invalid_card_number} \nРазвлекайтесь B)")
    else:
        print("Номер карты верен.")
