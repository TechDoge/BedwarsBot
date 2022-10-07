import numpy as np
import cv2
import mss

class Detector:

    def __init__(self, window_x, window_y, window_width, window_height):
        self.x = window_x
        self.y = window_y
        self.width = window_width
        self.height = window_height
        self.location = [0, 0, 0]
        self.tester = cv2.namedWindow("tester")
        self.tester2 = cv2.namedWindow("tester2")

    def get_number(self, color, top_color, index):

        data = [
            [138.75, 138.75, 138.75],
            [72.5, 72.5, 72.5],
            [116.25, 116.25, 116.25],
            [103.75, 103.75, 103.75],
            [100, 100, 100],
            [126.25, 126.25, 126.25],
            [117.5, 117.5, 117.5],
            [91.25, 91.25, 91.25],
            [126.25, 126.25, 126.25],
            [111.25, 111.25, 111.25]
        ]

        top_data = [
            [143.4375, 143.4375, 143.4375],
            [53.125, 53.125, 53.125],
            [106.25, 106.25, 106.25],
            [106.25, 106.25, 106.25],
            [95.625, 95.625, 95.625],
            [170.0, 170.0, 170.0],
            [92.96875, 92.96875, 92.96875],
            [140.78125, 140.78125, 140.78125],
            [127.5, 127.5, 127.5],
            [132.8125, 132.8125, 132.8125]
        ]

        negative = [45.0, 45.0, 45.0]
        negative_top = [31.875, 31.875, 31.875]

        most_similar = 0
        value = 0
        for i in range(len(data)):
            curr_color = data[i]
            curr_2_color = top_data[i]
            s = self.similarity(curr_color, color)
            s2 = self.similarity(curr_2_color, top_color)
            if s+s2 > value:
                most_similar = i
                value = s+s2

        acc_needed = 0.9

        if self.similarity(color, negative) + self.similarity(top_color, negative_top) > value and self.similarity(color, negative) + self.similarity(top_color, negative_top) >= acc_needed*2:
            return "-"

        if value < acc_needed*2:
            return "empty"
        
        return most_similar

    def scan(self):
        self.shot = self.get_shot()
        self.location = self.get_location()

    def get_shot(self):
        with mss.mss() as sct:
            monitor = {"top": self.y, "left": self.x, "width": self.width, "height": self.height}
            img_array = np.array(sct.grab(monitor))
            return img_array

    def average_color(self, portion):
        return np.average(portion, axis=(0,1))

    def similarity(self, a, b):
        sim = 1-(abs(a[0]-b[0])/(a[0]/2+b[0]/2)+abs(a[1]-b[1])/(a[1]/2+b[1]/2)+abs(a[2]-b[2])/(a[2]/2+b[2]/2))/3
        return sim
        
    def get_location(self):

        location = [0, 0, 0]

        x_num = ""
        x_nums_pos = [57, 55]
        width = 12
        spacing = 15
        height = 17
        x_sign = 1
        for i in range(20):
            portion = self.shot[x_nums_pos[1]:x_nums_pos[1]+height, x_nums_pos[0]+spacing*i:x_nums_pos[0]+width+spacing*i]
            if i == 0:
                cv2.imshow("tester", cv2.resize(portion, (500, 500)))
            if i == 1:
                cv2.imshow("tester2", cv2.resize(portion, (500, 500)))
            top_portion = self.shot[x_nums_pos[1]:x_nums_pos[1]+height//2, x_nums_pos[0]+spacing*i:x_nums_pos[0]+width+spacing*i]
            avg_color = self.average_color(portion)
            avg_top_color = self.average_color(top_portion)
            print(avg_color, avg_top_color)
            string = str(self.get_number(avg_color, avg_top_color, i))
            if string == "-":
                x_sign = -1
            elif string != "empty":
                x_num += string
            else:
                break
        if x_num != "":
            x_num = int(x_num)*x_sign
        else:
            x_num = 0
        location[0] = x_num
        print(location)
        return location