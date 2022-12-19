import cv2
import mediapipe as mp
mp_hands = mp.solutions.hands

class Hand:
    # ERR codes
    ERR_CAPTURE_DEVICE_CLOSED = int(-1)
    ERR_NO_FRAME = int(-2)
    ERR_NO_HAND = int(-3)
    # Moves
    UP = int(1)
    DOWN = int(2)
    LEFT = int(3)
    RIGHT = int(4)
    # Video resolution
    wCam = int
    hCam = int
    # Capture device
    cap = None
    # Hand tracker
    hand = None
    # Image
    img = None
    # Last move
    move = int


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
        self.move = self.UP
        self.old_x = float(0)
        self.old_y = float(0)

    def __del__(self):
        (self.cap).release()
        cv2.destroyAllWindows()

  
    def position(self):
        if self.cap.isOpened():
            success, img = self.cap.read()
            if success:
                img.flags.writeable = False
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                results = self.hand.process(img)

                cv2.imshow("DEBUG", cv2.flip(img, 1))
                
                if results.multi_hand_landmarks:
                    # Detected hand
                    hand_landmarks = results.multi_hand_landmarks[0]
                    lm_array = list(enumerate(hand_landmarks.landmark))
                    # Point of reference MIDDDLE_FINGER_MCP 
                    lm = lm_array[9][1]

                    return (1 - lm.x, lm.y)
                else:
                    return self.ERR_NO_HAND
            else:
                return self.ERR_NO_FRAME
        else:
            return self.ERR_CAPTURE_DEVICE_CLOSED
    
    def get_move(self):
        pos = self.position()
        if pos == self.ERR_CAPTURE_DEVICE_CLOSED:
            exit(self.ERR_CAPTURE_DEVICE_CLOSED)
        if pos == self.ERR_NO_FRAME or pos == self.ERR_NO_HAND:
            return self.move
        # Choose the next move based on the last position
        
        x = pos[0]
        y = pos[1]

        # Over main diagonal
        if x >= y:
            # Over minor diagonal -> Up
            if x + y <= 1:
                self.move = self.UP
                return self.UP
            # Under minor diagonal -> Right
            else:
                self.move = self.RIGHT
                return self.RIGHT
        # Under main diagonal
        else:
            # Over minor diagonal -> Left
            if x + y <= 1:
                self.move = self.LEFT
                return self.LEFT
            # Under minor diagonal -> Down
            else:
                self.move = self.DOWN
                return self.DOWN
