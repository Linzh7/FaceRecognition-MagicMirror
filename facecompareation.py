from deepface import DeepFace as df
import linzhutil as lu
from pathlib import Path
import os

PATH = './data/'
TEST_PATH = './data/test.jpg'

label_list = ['obama', 'beongce', 'biden', 'marin']
for label in label_list:
    data_img = Path(os.path.join(PATH,label)).rglob('*.jp*')
    result_list = []
    for sample in data_img:
        print(f'Verifying {sample}...', end='\t')
        result = df.verify(img1_path = TEST_PATH, img2_path = str(sample))
        if result['verified'] == True:
            result_list.append([label, result['distance']])
            print(f'OK, distance: {result["distance"]}')
        else:
            print('NG')
        # print(result)
    print(result_list)