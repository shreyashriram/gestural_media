import json
from flask import Flask,render_template, Response, jsonify
import requests
import cv2
import mediapipe as mp


app=Flask(__name__)
camera=cv2.VideoCapture(0)

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

updated_label = "no gesture detected" 


def generate_frames():
    with mp_hands.Hands(model_complexity=0, min_detection_confidence=0.75, min_tracking_confidence=0.5, max_num_hands=1) as hands:
        while True:
            ## read the camera frame
            success,frame=camera.read()

            landmarks = []                #chloe added
            w, h, c = frame.shape 

            if not success:
                break
            
            else:
                # To improve performance, optionally mark the image as not writeable to
                # pass by reference.
                frame.flags.writeable = False
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = hands.process(frame)

                frame.flags.writeable = True
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

                global updated_label
                updated_label = "no gesture detected"

                if results.multi_hand_landmarks:
                    # draw anotations onto video feed
                    for hand_landmarks in results.multi_hand_landmarks:
                        for lm in hand_landmarks.landmark:
                            # print(id, lm)
                            lmx = int(lm.x * w)
                            lmy = int(lm.y * h)
                            landmarks.append([lmx, lmy])

                        gestureLabel(landmarks)
            
                        # mp_drawing.draw_landmarks(
                        #     frame,
                        #     hand_landmarks,
                        #     mp_hands.HAND_CONNECTIONS,
                        #     mp_drawing_styles.get_default_hand_landmarks_style(),
                        #     mp_drawing_styles.get_default_hand_connections_style())
                
                
                # # Flip the image horizontally for a selfie-view display.
                frame = cv2.flip(frame, 1)
                # cv2.putText(frame, updated_label, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2, cv2.LINE_AA)

                ret,buffer=cv2.imencode('.jpg',frame)
                frame=buffer.tobytes()

            yield(b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            
            # yield(label)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/fetchLabel', methods=['GET'])
def fetchLabel():
    return {'updated_label': updated_label}


def gestureLabel(landmarks):
    thumbOpen = False
    pointerOpen = False
    middleOpen = False
    ringOpen = False
    pinkyOpen = False
    x = 0
    y = 1
    label = "no gesture detected"
    orientation = True              # amrita added

    if (landmarks[5][x] < landmarks[17][x]):  # amrita added
          orientation = False                     # added

    if (orientation and landmarks[4][x] > landmarks[2][x] and landmarks[3][x] > landmarks[2][x]): # amrita added
        thumbOpen = True                                                                            # added

    if (not orientation and landmarks[4][x] < landmarks[2][x] and landmarks[3][x] < landmarks[2][x]):  # amrita added
        thumbOpen = True                                                                                 # added

    if (landmarks[8][y] < landmarks[6][y] and landmarks[7][y] < landmarks[6][y]):
        pointerOpen = True

    if (landmarks[12][y] < landmarks[10][y] and landmarks[11][y] < landmarks[10][y]):
        middleOpen = True
    
    if (landmarks[16][y] < landmarks[14][y] and landmarks[15][x] < landmarks[14][y]):
        ringOpen = True

    if (landmarks[20][y] < landmarks[18][y] and landmarks[19][y] < landmarks[18][y]):
        pinkyOpen = True

    if(thumbOpen and pointerOpen and middleOpen and ringOpen and pinkyOpen):
        label = "PAUSE"

    elif(thumbOpen and not pointerOpen and not middleOpen and not ringOpen and pinkyOpen):
        label = "PLAY"

    elif(landmarks[4][x] < landmarks[3][x] and landmarks[3][x] < landmarks[2][x] and not pointerOpen and not middleOpen and not ringOpen and not pinkyOpen):
        label = "NEXT TRACK"

    elif(thumbOpen and not pointerOpen and not middleOpen and not ringOpen and not pinkyOpen):
        label = "PREVIOUS TRACK"

    elif(landmarks[4][x] < landmarks[3][x] and landmarks[3][x] < landmarks[2][x] and pointerOpen and middleOpen and not ringOpen and not pinkyOpen):
        label = "FAST FORWARD 10 SEC"

    elif(thumbOpen and pointerOpen and middleOpen and not ringOpen and not pinkyOpen): # added elif instead of if
        label = "REWIND 10 SEC"
    
    else:
        label = "no gesture detected"

    global updated_label
    updated_label = label

if __name__ == "__main__":
    app.run(debug=True)