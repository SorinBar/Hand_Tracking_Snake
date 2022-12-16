import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands

class Hand:
    # Video resolution
    wCam = None
    hCam = None
    # Declaration of capture device
    cap = None
    # Hand tracker
    hand = None

    def __init__(self, device = 0, wCam = 640, hCam = 480):
        self.wCam = wCam
        self.hCam = hCam
        # Set capture device
        self.cap = cv2.VideoCapture(device)
        # Set resolution of the input video
        self.cap.set(3, wCam)
        self.cap.set(4, hCam)
        # Set hand tracker
        self.hand = mp_hands.Hands(max_num_hands=1,
                                    model_complexity=0,
                                    min_detection_confidence=0.5,
                                    min_tracking_confidence=0.5)

    def test(self):
        print(self.wCam)
        print(self.hCam)
        print(self.cap.isOpened())

        while self.cap.isOpened():
            success, img = self.cap.read()
            img.flags.writeable = False
            if not success:
                print("Capturing video error")
                break
            img = cv2.flip(img, 1)
            cv2.imshow("image", img)



            if cv2.waitKey(5) & 0xFF == 27:
                break
    
    def __del__(self):
        (self.cap).release()
        cv2.destroyAllWindows()
        