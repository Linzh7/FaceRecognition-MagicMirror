#%%
from deepface import DeepFace as df
import linzhutil as lu
from pathlib import Path
import os
from collections import defaultdict
import numpy as np
import paho.mqtt.client as mqtt
import json
import time
import sys
from scipy import special as sps

PATH = './data/'
TEST_PATH = './data/test.jpg'

TEST_MODE = False

if TEST_MODE:
    SERVER_ADDRESS = "test.mosquitto.org"
    SERVER_PORT = 1883
else:
    SERVER_ADDRESS = sys.argv[1] if len(sys.argv) > 1 else "test.mosquitto.org"
    SERVER_PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 1883

THRESHOLD = 0.5
LABEL_LIST = '1 2 3 4'.split()


def load_known_faces(path=PATH, label_list=LABEL_LIST):
    print('Loading known faces...')
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
    match_score = defaultdict(list)
    result_score = defaultdict(int)
    try:
        face_descriptor = df.represent(img_path=test_face)[0]['embedding']
    except ValueError as e:
        print(e)
        return []
    for key, values in face_dict.items():
        for i in values:
            dist = np.linalg.norm(np.array(i) - np.array(face_descriptor))
            if dist < confidence:
                # print(f'Match {key} with {dist}')
                match_score[key] + dist
            else:
                # print(f'Not match {key} with {dist}')
                match_score[key] + [1.5]  # penalty
        result_score[key] = sps.softmax(match_score[key]) / len(values)
    return sorted(result_score.items(), key=lambda item: item[1])


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("$SYS/#")


def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))


def on_publish(client, userdata, result):
    print(f"data published, {result}")


#%%
# load data
if TEST_MODE:
    face_dict = load_known_faces()

# %%

if __name__ == '__main__':
    if not TEST_MODE:
        face_dict = load_known_faces()

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_publish = on_publish

    client.connect(SERVER_ADDRESS, SERVER_PORT, 60)

    print('Start detecting...')

    while True:
        result_score = find_known_face(face_dict, TEST_PATH)
        # print(result_score)
        # message_uid = random.randint(100000, 999999)
        if len(result_score) == 0:
            workload_dict = {'person_id': '', 'detected': False}
        else:
            workload_dict = {
                # 'uid': message_uid,
                'person_id':
                result_score[0][0] if result_score[0][1] < THRESHOLD else '',
                'detected':
                True
            }
        message = json.dumps(workload_dict)
        client.publish('magic-mirror/face-recognition', message)
        # time.sleep(0.1)
        # client.publish('face/result', message)
        print(message)
        time.sleep(1)
        # break
# %%

# TEST_PATH = './data/test.jpg'
# result_score = find_known_face(face_dict, TEST_PATH)
# print(result_score[0][0])
# %%
