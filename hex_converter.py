def hex_to_decimal(hex_value):
    try:
        hex_value = hex_value.strip().lstrip('0x').lstrip('0X')
        return int(hex_value, 16)
    except ValueError:
        return "Invalid Hex"


def decimal_to_hex(decimal_value):
    try:
        return hex(int(decimal_value))
    except ValueError:
        return "Invalid Decimal"


def display(hex_val, dec_val):
    print(f"\n{'='*40}\nHex: {hex_val}\nDec: {dec_val}\n{'='*40}\n")


def main():
    while True:
        print("1. Hex to Dec  2. Dec to Hex  3. Exit")
        choice = input("Choice: ").strip()
        
        if choice == '1':
            hex_in = input("Hex: ")
            display(hex_in, hex_to_decimal(hex_in))
        elif choice == '2':
            dec_in = input("Dec: ")
            display(decimal_to_hex(dec_in), dec_in)
        elif choice == '3':
            break
        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()