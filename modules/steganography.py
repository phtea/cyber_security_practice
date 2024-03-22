from PIL import Image
import chardet
import os

class LSBBytes:
    def __init__(self, image):
        self.pixels = image.load()
        self.width, self.height = image.size
        self.current_width, self.current_height = 0, 0
        self.color_channel = -1

    def __iter__(self):
        return self

    def __next__(self):
        x = 0x00
        for _ in range(4):
            self.color_channel += 1
            if (self.color_channel == 3):
                self.color_channel = 0
                self.current_width += 1
                if self.current_width == self.width:
                    self.current_width = 0
                    self.current_height += 1
                    if self.current_height == self.height:
                        raise StopIteration
            x = (x << 2) | (self.pixels[self.current_width, self.current_height][self.color_channel] & 0b11)
        if (x == 0x00):
            raise StopIteration
        return x

def decode_file(in_image_file):
    image = Image.open(in_image_file)
    bytes = bytearray()
    for byte in LSBBytes(image):
        bytes.append(byte)
    detector = chardet.universaldetector.UniversalDetector()
    detector.feed(bytes)
    detector.close()
    if detector.result['encoding']:
        return (bytes,detector.result['encoding'])
    else:
        return None

def bulk_decode(path_to_folder: str, output_folder: str):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    for file in os.listdir(path_to_folder):
        filename = os.fsdecode(file)
        print(filename, end=' ')
        decoded = decode_file(path_to_folder + "/" + filename)
        if decoded:
            outfile = open(output_folder + "/" + filename.split('.')[0]+".txt", "wb")
            outfile.write(decoded[0])
            outfile.close()
            print(decoded[1])
        else:
            print("None")

def main():
    folder_path = 'Stego_input'
    # path_to_image = folder_path + "/1019.png"
    # message = decode_file(path_to_image)
    # print(message[0].decode(message[1])) # decode message[0] using message[1] decoder
    bulk_decode(folder_path, 'Stego_output')

if __name__=="__main__":
    main()