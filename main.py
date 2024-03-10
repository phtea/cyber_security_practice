import face_recogn as fr
import diffie_hellman
import luhn

def main():
    # diffie_hellman.diffie_hellman_protocol(13, 6, 5, 4)
    # fr.Task_1(image_path="input/task1_test1.png")
    faces = fr.create_database()
    fr.Task_2(image_path="input/task2_test4.jpg", faces=faces)
    fr.Task_2(image_path="input/task2_test2.jpg", faces=faces)
    fr.Task_2(image_path="input/task2_test3.jpg", faces=faces)
    # vr = fr.VideoRecognition(faces=faces, video_path="input/video_test1.mp4")
    # vr.detect_faces_in_video()

if __name__ == "__main__":
    main()