import face_recogn as fr
import diffie_hellman
import luhn

def main():

    fr.Task_1(image_path="input/task1_test1.png")

    faces = fr.get_faces_database()
    
    fr.Task_2(image_path="input/task2_test4.jpg", faces=faces)
    fr.Task_2(image_path="input/task2_test2.jpg", faces=faces)
    fr.Task_2(image_path="input/task2_test3.jpg", faces=faces)

if __name__ == "__main__":
    main()