import cv2


class Camera:

    # Initializes the camera at a specific index with the desired resolution, or with default values
    def __init__(self, index=0, width=1280, height=720):
        self.cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)
        self.cap.set(3, width)
        self.cap.set(4, height)

    # Blurs an image
    @staticmethod
    def to_blur(img):
        return cv2.GaussianBlur(img, (7, 7), 1)

    # Converts an image to gray scale
    @staticmethod
    def to_gray(img):
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Converts an image to RGB
    @staticmethod
    def to_rgb(img):
        return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Returns the image from the current frame (flipped)
    def get_frame(self):
        success, img = self.cap.read()
        img = cv2.flip(img, -1)
        return img

    # Displays an image on a window
    def show_image(self, img, window="Camera"):
        cv2.imshow(window, img)
        cv2.waitKey(1)


def main():
    print("Camera Module")

    camera = Camera()

    while True:

        img = camera.get_frame()
        camera.show_image(img)


if __name__ == "__main__":
    main()
