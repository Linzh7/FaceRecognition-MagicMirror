#%%
from deepface import DeepFace as df
import linzhutil as lu
from pathlib import Path
import os
from collections import defaultdict
import numpy as np
import paho.mqtt.client as mqtt
import random
import json
import time

PATH = './data/'
TEST_PATH = './data/test.jpg'
SERVER_ADDRESS = "192.168.85.224"
SERVER_PORT = 1883


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
                # print(f'Not match {key} with {dist}')
                match_score[key] += 1.5  # penalty
        match_score[key] /= len(values)
    return sorted(match_score.items(), key=lambda item: item[1])


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("$SYS/#")


def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))


def on_publish(client, userdata, result):
    print(f"data published, {result}")


#%%
# load data
face_dict = load_known_faces()

# %%

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish

client.connect(SERVER_ADDRESS, SERVER_PORT, 60)

print('Start detecting...')
while True:
    result_score = find_known_face(face_dict, TEST_PATH)
    # print(result_score)
    message_uid = random.randint(100000, 999999)
    workload_dict = {
        'uid': message_uid,
        'result': result_score,
        'timestamp': time.time()
    }
    message = json.dumps(workload_dict)
    client.publish('face/result', message)
    client.publish('face/result', message)
    print(message)
    time.sleep(5)
    break
# %%
