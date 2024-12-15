import cv2 as cv
import mediapipe as mp
from pynput.keyboard import Key, Controller
import math

keyboard = Controller()
mp_draw = mp.solutions.drawing_utils
mp_hand = mp.solutions.hands
fingerTipIds = [4, 8, 12, 16, 20]
video = cv.VideoCapture(0)
hands = mp_hand.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

def calculate_distance(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

def calculate_angle(a, b, c):
    ab = [b[0] - a[0], b[1] - a[1]]
    bc = [c[0] - b[0], c[1] - b[1]]
    dot_product = ab[0] * bc[0] + ab[1] * bc[1]
    mag_ab = math.sqrt(ab[0] ** 2 + ab[1] ** 2)
    mag_bc = math.sqrt(bc[0] ** 2 + bc[1] ** 2)
    if mag_ab * mag_bc == 0:
        return 0
    cos_angle = dot_product / (mag_ab * mag_bc)
    cos_angle = min(max(cos_angle, -1), 1)
    angle = math.acos(cos_angle)
    return math.degrees(angle)

def check_open_hand(landmarks):
    thumb_tip = landmarks[4][1:]
    distances = [calculate_distance(thumb_tip, [landmarks[tip][1], landmarks[tip][2]]) for tip in fingerTipIds[1:]]
    if all(dist > 60 for dist in distances):
        return True
    return False

def check_closed_fist(landmarks):
    thumb_tip = landmarks[4][1:]
    distances = [calculate_distance(thumb_tip, [landmarks[tip][1], landmarks[tip][2]]) for tip in fingerTipIds[1:]]
    if all(dist < 60 for dist in distances):
        return True
    return False

while True:
    success, image = video.read()
    if not success:
        print("Failed to capture image")
        break
    image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    image.flags.writeable = False
    results = hands.process(image)
    image.flags.writeable = True
    image = cv.cvtColor(image, cv.COLOR_RGB2BGR)
    landmarks_list = []
    if results.multi_hand_landmarks:
        hand_landmarks = results.multi_hand_landmarks[-1]
        for index, lm in enumerate(hand_landmarks.landmark):
            h, w, c = image.shape
            cx, cy = int(lm.x * w), int(lm.y * h)
            landmarks_list.append([index, cx, cy])
        mp_draw.draw_landmarks(image, hand_landmarks, mp_hand.HAND_CONNECTIONS)
    if landmarks_list:
        angles = []
        for i in range(1, 5):
            angle = calculate_angle(
                landmarks_list[i * 4 - 3][1:],
                landmarks_list[i * 4 - 2][1:],
                landmarks_list[i * 4 - 1][1:]
            )
            angles.append(angle)
        if check_open_hand(landmarks_list):
            gesture = "Open Hand"
            cv.putText(image, "Open Hand", (45, 375), cv.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 5)
            keyboard.press(Key.right)
            keyboard.release(Key.left)
        elif check_closed_fist(landmarks_list):
            gesture = "Closed Fist"
            cv.putText(image, "Closed Fist", (45, 375), cv.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 5)
            keyboard.press(Key.left)
            keyboard.release(Key.right)
        else:
            gesture = "No Gesture"
    cv.imshow("Gesture Recognition", image)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

video.release()
cv.destroyAllWindows()
