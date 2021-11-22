import cv2
import numpy as np
from camera import Camera


class Calibrator:

    def __init__(self):

        print("init")

    def filter_image(self, img):
        img_gray = Camera.to_gray(img)

        # Get thresholds from the sliders and apply to create final image
        threshold1, threshold2 = cv2.getTrackbarPos(
            "Threshold1", "Parameters"), cv2.getTrackbarPos("Threshold2", "Parameters")

        img_canny = cv2.Canny(img_gray, threshold1, threshold2)

        # Dilate the image
        kernel = np.ones((5, 5))
        img_dil = cv2.dilate(img_canny, kernel, iterations=1)

        return img_dil

    def draw_shapes(self, output, source):

        contours, hierarchy = cv2.findContours(
            source, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

        for contour in contours:

            area = cv2.contourArea(contour)
            perimeter = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)

            x1, y1, w, h = cv2.boundingRect(approx)
            x2 = x1+w
            y2 = y1+h

            if area > 5000 and area < 50000:

                #cv2.drawContours(img_out, contours, -1, (255, 0, 255), 7)
                cv2.rectangle(output, (x1, y1), (x2, y2), (0, 255, 0), 5)

        return output


def main():
    print("Calibrator Module")

    camera = Camera()
    calibrator = Calibrator()

    # Create window for Threshold bars
    cv2.namedWindow("Parameters")
    cv2.resizeWindow("Parameters", 640, 240)
    cv2.createTrackbar("Threshold1", "Parameters", 150, 255, lambda: None)
    cv2.createTrackbar("Threshold2", "Parameters", 200, 255, lambda: None)

    while True:

        img = camera.get_frame()

        filtered_img = calibrator.filter_image(img)

        img = calibrator.draw_shapes(img, filtered_img)

        camera.show_image(filtered_img, "Filtered image")
        camera.show_image(img)


if __name__ == "__main__":
    main()
