import cv2
import numpy as np
from camera import Camera


def is_same_contour(c1, c2, margin=5):
    return abs(c1[0] - c2[0]) < margin and abs(c1[1] - c2[1]) < margin and abs(c1[2] - c2[2]) < margin and abs(c1[3] - c2[3]) < margin


def is_pointer_inside(p1, p2, pointer):
    return (pointer[0] > p1[0] and pointer[1] > p1[1]) and (pointer[0] < p2[0] and pointer[1] < p2[1])


class Calibrator:

    def __init__(self, threshold1=255, threshold2=255):

        self.threshold1 = threshold1
        self.threshold2 = threshold2

    def find_contours(self, img):
        img_gray = Camera.to_gray(img)

        # Get thresholds from the sliders and apply to create final image
        # threshold1, threshold2 = cv2.getTrackbarPos(
        #    "Threshold1", "Parameters"), cv2.getTrackbarPos("Threshold2", "Parameters")

        img_canny = cv2.Canny(img_gray, self.threshold1, self.threshold2)

        # Dilate the image
        kernel = np.ones((5, 5))
        img_dil = cv2.dilate(img_canny, kernel, iterations=1)

        contours, hierarchy = cv2.findContours(
            img_dil, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

        return contours, img_dil

    def draw_shapes(self, img, contours, pointer_pos=(0, 0)):

        last_points = (0, 0, 0, 0)
        valid_contours = 0
        selected_contour = 0

        for contour in contours:

            area = cv2.contourArea(contour)
            perimeter = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)

            x1, y1, w, h = cv2.boundingRect(approx)
            x2 = x1+w
            y2 = y1+h

            if area > 5000 and area < 50000 and not is_same_contour((x1, x2, y1, y2), last_points, 7):

                valid_contours += 1

                if(is_pointer_inside((x1, y1), (x2, y2), pointer_pos)):
                    color = (255, 0, 0)
                    selected_contour = valid_contours
                else:
                    color = (0, 255, 0)

                #cv2.drawContours(img_out, contours, -1, (255, 0, 255), 7)
                cv2.rectangle(img, (x1, y1), (x2, y2), color, 3)

                last_points = (x1, x2, y1, y2)

        return img, selected_contour


def main():
    print("Calibrator Module")

    camera = Camera()
    calibrator = Calibrator()

    # Create window for Threshold bars
    cv2.namedWindow("Parameters")
    cv2.resizeWindow("Parameters", 640, 240)
    cv2.createTrackbar("Threshold1", "Parameters",
                       calibrator.threshold1, 255, lambda: None)
    cv2.createTrackbar("Threshold2", "Parameters",
                       calibrator.threshold2, 255, lambda: None)

    while True:

        img = camera.get_frame()

        contours, filtered_img = calibrator.find_contours(img)

        img, _ = calibrator.draw_shapes(img, contours)

        camera.show_image(filtered_img, "Filtered image")
        camera.show_image(img)


if __name__ == "__main__":
    main()
