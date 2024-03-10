import os
import cv2
import face_recognition
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

class Face:
    def __init__(self, bounding_box, cropped_face, name, feature_vector):
        self.bounding_box = bounding_box
        self.cropped_face = cropped_face
        self.name = name
        self.feature_vector = feature_vector

class Task_1:
    def __init__(self, image_path):
        self.image_path = image_path
        # Load the XML files for face, eye, and smile detection
        self.face_cascade = cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')
        self.eye_cascade = cv2.CascadeClassifier('data/haarcascade_eye.xml')
        self.smile_cascade = cv2.CascadeClassifier('data/haarcascade_smile.xml')  # Path to your smile cascade XML
        self.detect_face_eyes_smile()
        
    def detect_face_eyes_smile(self):

        image = cv2.imread(self.image_path)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        faces = self.face_cascade.detectMultiScale(gray_image, 1.3, 5)

        for (x,y,w,h) in faces:
            cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),2) # draw a rectangle

            # Define region of interest (ROI) for eyes within the face
            roi_gray = gray_image[y:y+h, x:x+w]
            roi_color = image[y:y+h, x:x+w]
            
            eyes = self.eye_cascade.detectMultiScale(roi_gray)
            for (ex,ey,ew,eh) in eyes:
                cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

            smiles = self.smile_cascade.detectMultiScale(roi_gray, scaleFactor=1.8, minNeighbors=20)
            for (sx,sy,sw,sh) in smiles:
                cv2.rectangle(roi_color,(sx,sy),(sx+sw,sy+sh),(0,0,255),2)

        # Display the final image
        cv2.imshow('Detected faces, eyes, and smiles', image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

class Task_2:
    def __init__(self, image_path, faces):
        self.faces = faces
        self.image_path = image_path
        self.execute()

    def load_image(self, path):
        image = cv2.imread(path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        return image

    def show_image(self, image):
        plt.imshow(image)
        plt.xticks([])
        plt.yticks([])
        plt.show()

    def draw_bounding_box(self, image_test, loc_test):
        top, right, bottom, left = loc_test
        line_color = (0, 255, 0)
        line_thickness = 2
        cv2.rectangle(image_test, (left, top), (right, bottom), line_color, line_thickness)
        return image_test

    def draw_name(self, image_test, loc_test, pred_name):
        top, right, bottom, left = loc_test
        font_style = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1.5
        font_color = (0, 0, 255)
        font_thickness = 3
        text_size, _ = cv2.getTextSize(pred_name, font_style, font_scale, font_thickness)
        bg_top_left = (left, top - text_size[1])
        bg_bottom_right = (left + text_size[0], top)
        line_color = (0, 255, 0)
        line_thickness = -1
        cv2.rectangle(image_test, bg_top_left, bg_bottom_right, line_color, line_thickness)
        cv2.putText(image_test, pred_name, (left, top), font_style, font_scale, font_color, font_thickness)
        return image_test

    def detect_faces(self, image_test, threshold=0.6):
        locs_test = face_recognition.face_locations(image_test, model='hog')
        vecs_test = face_recognition.face_encodings(image_test, locs_test, num_jitters=1)
        for loc_test, vec_test in zip(locs_test, vecs_test):
            distances = []
            for face in self.faces:
                distance = face_recognition.face_distance([vec_test], face.feature_vector)
                distances.append(distance)
            if np.min(distances) > threshold:
                pred_name = 'unknown'
            else:
                pred_index = np.argmin(distances)
                pred_name = self.faces[pred_index].name
            image_test = self.draw_bounding_box(image_test, loc_test)
            image_test = self.draw_name(image_test, loc_test, pred_name)
        return image_test

    def execute(self):
        image_test = self.load_image(self.image_path)
        result_image = self.detect_faces(image_test)
        self.show_image(result_image)

def create_database() -> list[object]:
    
    def get_filenames() -> list[str]:
        filenames = os.listdir('templates')
        filenames = [filename for filename in filenames if not filename.startswith('!')]
        return filenames
    filenames = get_filenames()

    def load_image(path):
        image = cv2.imread(path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        return image

    faces = []
    for filename in tqdm(filenames, total=len(filenames)):
        image = load_image(os.path.join('templates', filename))
        loc = face_recognition.face_locations(image, model='hog')[0]
        vec = face_recognition.face_encodings(image, [loc], num_jitters=20)[0]
        top, right, bottom, left = loc
        cropped_face = image[top:bottom, left:right]
        face = Face(bounding_box=loc, cropped_face=cropped_face, name=filename.split('.')[0], feature_vector=vec)
        faces.append(face)
    return faces

class VideoRecognition:
    def __init__(self, faces: list[object], video_path: str):
        self.faces = faces
        self.video_path = video_path

    def detect_faces(self, frame, threshold=0.6):
        print('yeeeeeeeeeeeeee')
        # Convert the frame from BGR to RGB
        rgb_frame = frame[:, :, ::-1]

        # Find all the face locations and encodings in the current frame
        locs = face_recognition.face_locations(rgb_frame, model='hog')
        vecs = face_recognition.face_encodings(rgb_frame, locs, num_jitters=1)
        
        # Process each detected face
        for loc, vec in zip(locs, vecs):
            distances = []
            for face in self.faces:
                distance = face_recognition.face_distance([vec], face.feature_vector)
                distances.append(distance)
            
            # Determine the predicted name for the face
            if np.min(distances) > threshold:
                pred_name = 'Unknown'
            else:
                pred_index = np.argmin(distances)
                pred_name = self.faces[pred_index].name
            
            # Draw bounding box and label on the frame
            top, right, bottom, left = loc
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, pred_name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 255), 1)
        
        return frame

    def detect_faces_in_video(self):
        video_capture = cv2.VideoCapture(self.video_path)
        if not video_capture.isOpened():
            raise ValueError("Unable to open video file")

        while True:
            ret, frame = video_capture.read()
            if not ret:
                break
            
            # Process the current frame to detect faces
            processed_frame = self.detect_faces(frame)

            # Display the resulting frame with bounding boxes and labels
            cv2.imshow('Video', processed_frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Release video capture and destroy OpenCV windows
        video_capture.release()
        cv2.destroyAllWindows()

def main():
    # Task_1(image_path="input/task1_test1.png")
    
    # faces = create_database()
    
    # Task_2(image_path="input/task2_test4.jpg", faces=faces)
    # Task_2(image_path="input/task2_test3.jpg", faces=faces)
    pass



if __name__ == "__main__":
    main()
