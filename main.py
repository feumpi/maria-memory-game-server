import keyboard
from calibrator import Calibrator
from camera import Camera
from hand_tracker import HandTracker
from udp_socket import UdpSocket


camera = Camera()
hand_tracker = HandTracker()
calibrator = Calibrator()

udp_socket = UdpSocket(udp_ip="127.0.0.1", send_port=8000, receive_port=8001,
                       enable_receive=True, suppress_warnings=False)

contours = []


def calibrate():
    print("Calibrating...")
    img = camera.get_frame()
    cont, filtered_img = calibrator.find_contours(img)
    return cont


# Initial calibration
contours = calibrate()

selected_index = 0

while True:

    # Recalibrate, if requested with 'c' key press
    if keyboard.is_pressed('c'):
        print("Recalibrating...")
        contours = calibrate()

    # Try to read data from the game
    data = udp_socket.read_received_data()

    if data != None:
        print(data)
        udp_socket.send_data("Sent from server")

    img = camera.get_frame()

    pointer_pos = (0, 0)

    hand_landmarks = hand_tracker.find_hand(img)

    if hand_landmarks:
        img, pointer_pos = hand_tracker.draw_hand(img, hand_landmarks)

    # Draw previously found contours
    img, index = calibrator.draw_shapes(img, contours, pointer_pos)

    if index != selected_index:
        selected_index = index
        print(selected_index)
        udp_socket.send_data(str(selected_index))

    camera.show_image(img)
