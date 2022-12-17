import cv2
import mediapipe as mp
mp_hands = mp.solutions.hands

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

class Hand:
    # Video resolution
    wCam = None
    hCam = None
    # Capture device
    cap = None
    # Hand tracker
    hand = None

    def __init__(self, device=0, wCam=640, hCam=480):
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
        print(self.wCam, end="x")
        print(self.hCam)
        print(self.cap.isOpened())

        while self.cap.isOpened():
            success, img = self.cap.read()
            if not success:
                print("Empty camera frame")
                break

            img.flags.writeable = False
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = cv2.flip(img, 1)
            results = self.hand.process(img)

            img.flags.writeable = True
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(
                        img,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS,
                        mp_drawing_styles.get_default_hand_landmarks_style(),
                        mp_drawing_styles.get_default_hand_connections_style())

            print("start")
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    lm_array = list(enumerate(hand_landmarks.landmark))

                    #print(lm_array[0])
                    id, lm = lm_array[9]
                    print("X: ", end="")
                    print(lm.x)
                    print("Y: ", end="")
                    print(lm.y)
                    continue
                    for id, lm in enumerate(hand_landmarks.landmark):
                        cx = int(lm.x * self.wCam)
                        cy = int(lm.y * self.hCam)
                        print(id, cx, cy)

            print("stop")
            cv2.imshow("image", img)

            if cv2.waitKey(5) & 0xFF == 27:
                break
    
    def __del__(self):
        (self.cap).release()
        cv2.destroyAllWindows()
        