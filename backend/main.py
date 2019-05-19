import argparse
import os
from threading import Thread

import cv2
import cv2 as cv
import numpy as np
import requests
import tensorflow as tf

import api_main
import config
from description_updater import DescriptionUpdater
from picture_listener import PictureListener
from utilities.centroidtracker import CentroidTracker
from video_camera import VideoCamera


# choose which model you like to use


# # Read the graph.
def load_model():
    with tf.gfile.FastGFile(config.MODEL_PATH, 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        tf.import_graph_def(graph_def, name='')


def do_visualisation(out, frame, ct, camera_description, camera_index):
    font = cv.FONT_HERSHEY_SIMPLEX
    rows = frame.shape[0]
    cols = frame.shape[1]
    # Visualize detected bounding boxes.
    num_detections = int(out[0][0])
    rects = []
    detected = False
    for i in range(num_detections):
        class_id = int(out[3][0][i])
        score = float(out[1][0][i])
        bbox = [float(v) for v in out[2][0][i]]
        if score > 0.8:
            detected = True
            x = bbox[1] * cols
            y = bbox[0] * rows
            right = bbox[3] * cols
            bottom = bbox[2] * rows

            # update centroids
            box = [int(x), int(y), int(right), int(bottom)]
            rects.append(box)
            objects = ct.update(rects)

            if class_id == 1:
                label = 'Train'
            elif class_id == 2:
                label = 'Wagon'
            else:
                label = 'Unknown'
            # loop over the tracked objects
            id = ''
            for (object_id, centroid) in objects.items():
                id = object_id
            cv.putText(frame, "ID:{},L:{},S:{}%".format(id, label, int(score * 100)), (int(x), int(y) + 20), font, 1,
                       (255, 255, 255), 2,
                       cv.LINE_AA)
            cv.rectangle(frame, (int(x), int(y)), (int(right), int(bottom)), (125, 255, 51), thickness=2)
    cv.putText(frame, 'CAM: {},{}'.format(camera_index, camera_description), (15, 20), font, 0.5, (125, 255, 51), 2,
               cv.LINE_AA)
    return frame, detected


def get_output_model(frame, sess):
    # Run the model
    input1 = frame
    # BGR2RGB
    input1 = input1[:, :, [2, 1, 0]]

    output = sess.run([sess.graph.get_tensor_by_name('num_detections:0'),
                       sess.graph.get_tensor_by_name('detection_scores:0'),
                       sess.graph.get_tensor_by_name('detection_boxes:0'),
                       sess.graph.get_tensor_by_name('detection_classes:0')],
                      feed_dict={'image_tensor:0': input1.reshape(1, input1.shape[0], input1.shape[1], 3)})
    return output


def main():
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = config.GOOGLE_CREDENTIALS_PATH
    camera_list = []
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--number', required=True)
    parser.add_argument('-s', '--skip', required=False)
    args = parser.parse_args()

    if args.number:
        number = args.number

    if args.skip:
        skip_ids = int(args.skip)
    else:
        skip_ids = 0

        # on mac change 0 to 1
    for i in range(skip_ids, int(number) + skip_ids):
        try:
            camera_list.append(VideoCamera(i))
        except ValueError as error:
            print(error)

    if len(camera_list) == 0:
        raise Exception("Empty camera list.")

    listener = PictureListener(number)
    interval_thread = Thread(target=listener.start)
    interval_thread.start()

    updater = DescriptionUpdater(camera_list)
    update_thread = Thread(target=updater.start)
    update_thread.start()

    ct = CentroidTracker()
    load_model()

    # Start session
    with tf.Session() as sess:
        sess.graph.as_default()

        # get frame height
        frame_width = int(800 / len(camera_list))
        frame_height = int(800 / len(camera_list))
        while True:
            frames = []
            for camera in camera_list:
                frame = camera.get_frame()
                if frame is not None:
                    output = get_output_model(frame, sess)
                    frame, state = do_visualisation(output, frame, ct, camera.description, camera.index)
                    camera.update_state(state)
                    frame = cv.resize(frame, (frame_width, frame_height))
                    frames.append(frame)
            frame_in_one = frames.pop(0)
            for frame in frames:
                frame_in_one = np.vstack((frame_in_one, frame))
            cv2.imshow("Train detection", frame_in_one)
            if cv.waitKey(1) == 27:
                for c in camera_list:
                    c.stop()
                listener.shutdown()
                updater.shutdown()
                requests.get('http://127.0.0.1:5002/shutdown')
                cv2.destroyAllWindows()
                break


if __name__ == '__main__':
    try:
        # index = 0
        # arr = []
        # while True:
        #     cap = cv2.VideoCapture(index)
        #     if not cap.read()[0]:
        #         break
        #     else:
        #         arr.append(index)
        #     cap.release()
        #     index += 1
        # print(arr)

        api_main.main()
        main()
    except Exception as error:
        print(error)
        print('Closing...')
        requests.get('http://127.0.0.1:5002/shutdown')
