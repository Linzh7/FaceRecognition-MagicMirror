import sys
import os
import dlib
import numpy as np
import cv2
from pathlib import Path

model_list = [
    'models/shape_predictor_68_face_landmarks.dat',
    'models/dlib_face_recognition_resnet_model_v1.dat'
]

predictor_path = model_list[0]
face_rec_model_path = model_list[1]
faces_folder_path = './data'
output_folder_path = './output'

detector = dlib.get_frontal_face_detector()
sp = dlib.shape_predictor(predictor_path)
facerec = dlib.face_recognition_model_v1(face_rec_model_path)


def load_known_faces(path=faces_folder_path):
    known_dict = {}
    folders = os.listdir(path)
    for folder in folders:
        if '.' in folder:
            continue
        files = os.listdir(os.path.join(path, folder))
        face_desc = []
        for file in files:
            if os.path.splitext(file)[1] in ['.jpg', '.jpeg']:
                img = cv2.imread(os.path.join(path, folder, file))
                print("{}: {}*{}".format(file, img.shape[0], img.shape[1]))
                shape = sp(img, dlib.rectangle(0, 0, img.shape[0],
                                               img.shape[1]))
                face_descriptor = facerec.compute_face_descriptor(img, shape)
                face_desc.append(face_descriptor)
        known_dict[folder] = face_desc
    return known_dict


def find_known_face(face_dict, face, confidence=0.9):
    match_dict = {}
    for key, values in face_dict.items():
        confidence = 1.0
        for i, val in enumerate(values):
            diff = np.linalg.norm(np.array(face) - np.array(val))
            if diff < 1 - confidence and diff < confidence:
                confidence = diff
        match_dict[key] = confidence
    return sorted(match_dict.items(), key=lambda item: item[1])


if __name__ == '__main__':
    known_faces = load_known_faces()
    test_img = cv2.imread('./test.jpg')
    result = find_known_face(known_faces, test_img, 0.9)
    print(result)