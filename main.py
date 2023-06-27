import threading
import cv2
import imutils
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume
import webbrowser
import random

# camera setup
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW) # access camera

# camera dimentions
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

ret, start_frame = cap.read()
start_frame = imutils.resize(start_frame, width = 500)
start_frame = cv2.cvtColor(start_frame, cv2.COLOR_BGR2GRAY) # converting color to gray to make movement stand out
start_frame = cv2.GaussianBlur(start_frame, (21, 21), 0) # smoothen the image give it a blur

alarm = False
alarm_mode = False
alarm_counter = 0

# educational sites arr
sites = ['https://www.teamunify.com/team/ilghsd225/controller/cms/admin/index?team=ilghsd225#/res-128576',
 'https://lichess.org/training', 
 'https://www.act.org/content/act/en/products-and-services/the-act/test-preparation/math-practice-test-questions.html?page=0&chapter=0']

# volume and mute func
def set_volume_and_mute(volume_level, mute_state):
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        volume = session.SimpleAudioVolume
        volume.SetMasterVolume(volume_level, None)
        volume.SetMute(mute_state, None)

# open educational tab func
def open_url(url):
    webbrowser.open(url)

# func called when an alarm is occured
def trigger_alarm():
    global alarm
    for i in range(1):
        if not alarm_mode:
            break
        set_volume_and_mute(0.0, True) # set volume to 0 and mute
        url = random.choice(sites)
        open_url(url)
        # print("ALARM")
    # alarm = False

while True:
    ret, frame = cap.read()
    frame = imutils.resize(frame, width = 500)

    if alarm_mode:
        # black and white frame
        frame_bw = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame_bw = cv2.GaussianBlur(frame_bw, (5, 5), 0)

        difference = cv2.absdiff(frame_bw, start_frame) # find difference in frames (motion)
        threshold = cv2.threshold(difference, 25, 255, cv2.THRESH_BINARY)[1] 
        start_frame = frame_bw

        # movement sensitivity
        if threshold.sum() > 1000:
            print(threshold.sum())
            alarm_counter += 1
        else:
            if alarm_counter > 0:
                alarm_counter -= 1
        cv2.imshow("Camera", threshold)
    
    else:
        cv2.imshow("Camera", frame)

    if alarm_counter > 20:
        if not alarm:
            alarm = True
            threading.Thread(target=trigger_alarm).start()

    key_pressed = cv2.waitKey(30)

    # reset setting
    if key_pressed == ord('r'):
        alarm_mode = not alarm_mode
        alarm_counter = 0
    if key_pressed == ord('q'):
        alarm_mode = False
        break
    if key_pressed == ord('a'):
        alarm_mode = True
        trigger_alarm()
    if key_pressed == ord('v'):
        set_volume_and_mute(1.0, False)

cap.release()
cv2.destroyAllWindows()
