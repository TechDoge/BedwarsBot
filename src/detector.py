import numpy as np
import cv2
import mss
import scipy
class Detector:
 
    def __init__(self, window_x, window_y, window_width, window_height):
        self.x = window_x
        self.y = window_y
        self.width = window_width
        self.height = window_height
        self.location = [0, 0, 0]
        # self.tester = cv2.namedWindow("tester")
        # self.tester2 = cv2.namedWindow("tester2")
 
    def get_number(self, number):
 
        best_weight = -10000000000
        best_digit = -1
        all_weights=[]
        num_images = [f'../data/numbers/{i}.png' for i in range(10)] + ["../data/numbers/negative.png"]
        for i, img_name in enumerate(num_images):
            num_img = cv2.imread(img_name)
            from_game = cv2.cvtColor(number, cv2.COLOR_BGR2GRAY).astype(np.float64) - 128
            ref = cv2.cvtColor(num_img, cv2.COLOR_BGR2GRAY).astype(np.float64) - 128
            weight = np.max(scipy.signal.correlate2d(from_game, ref, mode='same', boundary='fill', fillvalue=0))

            all_weights.append(weight)
            if weight > best_weight:
                best_weight = weight
                best_digit = i
        average_weight = np.average(np.array(all_weights))
        # print(f'best_weight={best_weight}, avg_weight={average_weight}')
        avg_c = self.average_color(number)
        if best_weight <1500000 or avg_c[0] == 0 or avg_c[1] == 0 or avg_c[2] == 0 or avg_c[0] != avg_c[1] or avg_c[1] != avg_c[2]:
            return "empty"
        return best_digit
 
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
            # if i == 0:
            #     cv2.imshow("tester", portion)
            # elif i == 1:
            #     cv2.imshow("tester2", portion)
            string = str(self.get_number(portion))
            if string == "10":
                x_sign = -1
            elif string != "empty":
                x_num += string
            else:
                break

        if x_num != "":
            x_num = int(x_num)*x_sign
        else:
            x_num = 0

        y_num = ""
        y_nums_pos = [57, 82]
        y_sign = 1
 
        for i in range(20):
            portion = self.shot[y_nums_pos[1]:y_nums_pos[1]+height, y_nums_pos[0]+spacing*i:y_nums_pos[0]+width+spacing*i]
            # if i == 0:
            #     cv2.imshow("tester", cv2.resize(portion, (500, 500)))
            # elif i == 1:
            #     cv2.imshow("tester2", portion)
            string = str(self.get_number(portion))
            if string == "10":
                y_sign = -1
            elif string != "empty":
                y_num += string
            else:
                break

        if y_num != "":
            y_num = int(y_num)*y_sign
        else:
            y_num = 0

        z_num = ""
        z_nums_pos = [57, 109]
        z_sign = 1
        width = 11
        spacing = 15
        height = 16
 
        for i in range(20):
            portion = self.shot[z_nums_pos[1]:z_nums_pos[1]+height, z_nums_pos[0]+spacing*i:z_nums_pos[0]+width+spacing*i]
            # if i == 2:
            #     cv2.imshow("tester", cv2.resize(portion, (500, 500)))
            # elif i == 3:
            #     cv2.imshow("tester2", portion)
            string = str(self.get_number(portion))
            if string == "10":
                z_sign = -1
            elif string != "empty":
                z_num += string
            else:
                break

        if z_num != "":
            z_num = int(z_num)*z_sign
        else:
            z_num = 0


        location[0] = x_num
        location[1] = y_num
        location[2] = z_num
        return location

