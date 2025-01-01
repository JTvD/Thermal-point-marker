# Example off how to show an image in openCV and mark points  with the mouse.
# The temperature of the specific pixels is than stored in a CSV.
import cv2
import numpy as np


class point_marker:
    """ Class wrapper"""
    def edit_image(self, img: np.ndarray, temp_values: np.ndarray):
        """ Edit an image by marking points on it.
            args:
                img: np.ndarray, image to edit
                temp_values: np.ndarray, temperature values of the image
        """
        self.img = img
        self.temp_values = temp_values
        cv2.imshow('Main', img)
        cv2.setMouseCallback('Main', self.mark_mouse_coords)
        # Wait for ESC key to exit
        pressedkey = None
        while pressedkey != 27:
            pressedkey = cv2.waitKey(0)
        cv2.destroyAllWindows()
        print("done")

    def mark_mouse_coords(self, event, x: int, y: int, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.mark_point(x, y)

    def mark_point(self, x: int, y: int):
        """ Mark a point on the image and print the temperature value.
            args:
                x: int, x coordinate of the point
                y: int, y coordinate of the point
        """
        # White point with a black border
        white_color = (255, 255, 255)
        black_color = (0, 0, 0)
        cv2.circle(self.img, (x, y), 1, white_color, -1)
        cv2.circle(self.img, (x, y), 2, black_color, 1)
        # Print the temperature value
        print(f"xy: {x}, {y}, temp:{self.temp_values[y][x]}")
        cv2.imshow("Main", self.img)


if __name__ == "__main__":
    """ Test code to process one image"""
    image_filename = "test_data/e8xt_falsecolor.png"
    csv_filename = "test_data/e8xt_thermal.csv"

    # Load image
    img = cv2.imread(image_filename)

    # load csv file
    temp_values = np.genfromtxt(csv_filename, delimiter=',')

    marker = point_marker()
    marker.edit_image(img, temp_values)
