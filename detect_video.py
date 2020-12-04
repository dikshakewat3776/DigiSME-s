import os
import cv2
import numpy as np
from imutils.video import FPS
import csv


print(cv2.__version__)
vid_path = os.path.join(os.path.dirname(__file__),  'FoodMarketPeppersH264.mp4')

try:
    if vid_path:
        cap = cv2.VideoCapture(vid_path)
    else:
        cap = cv2.VideoCapture(0)
except Exception as e:
    print(e)
    cap = None

fps = cap.get(cv2.CAP_PROP_FPS)
print("Frames per second is: {0}".format(fps))

fps = FPS().start()

labelsPath = os.path.join(os.path.dirname(__file__),  'coco.names')
weightsPath = os.path.join(os.path.dirname(__file__),  'yolov4.weights')
configPath = os.path.join(os.path.dirname(__file__),  'yolov4.cfg')

LABELS = open(labelsPath).read().strip().split("\n")
COLORS = np.random.randint(0, 255, size=(len(LABELS), 3), dtype="uint8")


net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)
ln = net.getLayerNames()
ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]
FR = 0
(W, H) = (None, None)


# f = None
# with open("detections.txt", "a") as f:
#     f.write(str(det) + '\n')
columns = ['name', 'confidence', 'x_pred', 'y_pred', 'w_pred', 'h_pred']
d_filename = "detections.csv"

try:
    while True:
        (grabbed, frame) = cap.read()

        if not grabbed:
            break

        if W is None or H is None:
            (H, W) = frame.shape[:2]
            FW = W
            if (W < 1075):
                FW = 1075
            FR = np.zeros((H + 210, FW, 3), np.uint8)

            col = (255, 255, 255)
            FH = H + 210
        FR[:] = col

        blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416), swapRB=True, crop=False)
        net.setInput(blob)
        layerOutputs = net.forward(ln)
        boxes = []
        confidences = []
        classIDs = []

        for output in layerOutputs:
            for detection in output:
                scores = detection[5:]
                classID = np.argmax(scores)
                confidence = scores[classID]
                if LABELS[classID]:
                    if confidence > 0.5:
                        box = detection[0:4] * np.array([W, H, W, H])
                        (centerX, centerY, width, height) = box.astype("int")

                        x = int(centerX - (width / 2))
                        y = int(centerY - (height / 2))

                        boxes.append([x, y, int(width), int(height)])
                        confidences.append(float(confidence))
                        classIDs.append(classID)

        idxs = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.5)

        if len(idxs) > 0:
            for i in idxs.flatten():

                (x, y) = (boxes[i][0], boxes[i][1])
                (w, h) = (boxes[i][2], boxes[i][3])
                color = [int(c) for c in COLORS[classIDs[i]]]
                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 1, lineType=cv2.LINE_AA)
                text = "{}: {:.4f}".format(LABELS[classIDs[i]], confidences[i])
                # det_dict = {'name': str(LABELS[classIDs[i]]),
                #        'confidence': str(confidences[i]),
                #        'x_pred': str(x),
                #        'y_pred': str(y),
                #        'w_pred': str(w),
                #        'h_pred': str(h)}
                # import pandas as pd
                # output = pd.DataFrame()
                # output = output.append(det_dict, ignore_index=True)
                cv2.putText(frame, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX,0.5, color, 1, lineType=cv2.LINE_AA)
            cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        fps.update()

    cap.release()
    cv2.destroyAllWindows()
    fps.stop()
    print("Elasped time: {:.2f}".format(fps.elapsed()))
    print("Approx. FPS: {:.2f}".format(fps.fps()))
except Exception as e:
    print(e)


# import os
# a = os.system("darknet detector train data/obj.data cfg/custom-yolov4-tiny-detector.cfg yolov4-tiny.conv.29 -dont_show -map")
# print(a)

