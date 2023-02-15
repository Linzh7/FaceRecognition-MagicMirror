#%%
from deepface import DeepFace as df
import linzhutil as lu
from pathlib import Path
import os
from collections import defaultdict
import numpy as np

PATH = './data/'
TEST_PATH = './data/test.jpg'


def load_known_faces(path=PATH):
    print('Loading known faces...')
    label_list = ['obama', 'beongce', 'biden', 'marin']
    known_dict = defaultdict(list)
    for label in label_list:
        print(f'Loading {label}...')
        image_list = Path(os.path.join(path, label)).rglob('*.jp*')
        for file in image_list:
            embedding = df.represent(img_path=str(file))
            known_dict[label].append(embedding[0]['embedding'])
    print('Done')
    return known_dict


def find_known_face(face_dict, test_face, confidence=0.9):
    match_score = defaultdict(int)
    face_descriptor = df.represent(img_path=test_face)[0]['embedding']
    for key, values in face_dict.items():
        for i in values:
            dist = np.linalg.norm(np.array(i) - np.array(face_descriptor))
            if dist < confidence:
                # print(f'Match {key} with {dist}')
                match_score[key] += dist
            else:
                match_score[key] += 1.5  # penalty
    return sorted(match_score.items(), key=lambda item: item[1])


#%%
face_dict = load_known_faces()

#%%
result_score = find_known_face(face_dict, TEST_PATH)
print(result_score)
# %%
