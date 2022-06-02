import cv2
import mediapipe as mp
from camera import Camera


class HandTracker:

    def __init__(self, static=False, detection_confidence=0.5, tracking_confidence=0.5):

        self.mp_hands = mp.solutions.hands

        self.hands = self.mp_hands.Hands()

        self.mp_draw = mp.solutions.drawing_utils

    def find_hand(self, img):

        img_rgb = Camera.to_rgb(img)
        results = self.hands.process(img_rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                return hand_landmarks

    def draw_hand(self, img, hand_landmarks):

        # Draw landmarks (points) and connections
        self.mp_draw.draw_landmarks(img, hand_landmarks,
                                    self.mp_hands.HAND_CONNECTIONS)

        index_pos = (0, 0)

        # For each landmark
        for id, lm in enumerate(hand_landmarks.landmark):

            # x and y coordinates in pixels
            h, w, c = img.shape
            cx, cy = int(lm.x*w), int(lm.y*h)

            # Draw a circle on landmark 8 (index finger tip)
            if(id == 8):
                index_pos = (cx, cy)
                cv2.circle(img, (cx, cy), 10,
                           (255, 0, 255), cv2.FILLED)

        return img, index_pos


def main():
    print("Hand Tracker Module")

    camera = Camera()
    hand_tracker = HandTracker()

    while True:

        img = camera.get_frame()

        hand_landmarks = hand_tracker.find_hand(img)

        if hand_landmarks:
            # print(hand_landmarks)
            img, _ = hand_tracker.draw_hand(img, hand_landmarks)

        camera.show_image(img)


if __name__ == "__main__":
    main()
