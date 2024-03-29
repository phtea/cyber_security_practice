import modules.face_recogn as fr
import modules.diffie_hellman as diffie_hellman
import modules.luhn as luhn
import modules.steganography as steg

def main():
    folder_path = 'Stego_input'
    path_to_image = folder_path + "/1011.png"
    decoded = steg.decode_file(path_to_image)
    print(decoded[0]) # decode message[0] using message[1] decoder
    # steg.bulk_decode(folder_path, 'Stego_output')

if __name__ == "__main__":
    main()