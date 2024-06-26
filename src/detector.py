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
        self.location_manager = Location()
        self.resource_manager = Resources()
        self.location = [0, 0, 0]

 
    def scan(self):
        self.shot = self.get_shot()
        self.location = self.location_manager.get_location(self.shot)
        self.resources = self.resource_manager.get_resources(self.shot)
 
    def get_shot(self):
        with mss.mss() as sct:
            monitor = {"top": self.y, "left": self.x, "width": self.width, "height": self.height}
            img_array = np.array(sct.grab(monitor))
            return img_array
       
    
class Location:

    def __init__(self):
        self.shot = None
        self.path = "data/location_numbers"

    def get_number(self, number):
        best_weight = -100
        best_digit = -1
        all_weights=[]
        num_images = [f'{self.path}/{i}.png' for i in range(10)] + [f"{self.path}/negative.png"]
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
        avg_c = np.average(number, axis=(0,1))
        if best_weight <500000 or avg_c[0] == 0 or avg_c[1] == 0 or avg_c[2] == 0 or avg_c[0] != avg_c[1] or avg_c[1] != avg_c[2]:
            return "empty"
        return best_digit

    def get_location(self, shot):
        self.shot = shot 
        location = [0, 0, 0]

        x_num = ""
        x_nums_pos = [57, 55]
        width = 12
        spacing = 15
        height = 17
        x_sign = 1

        for i in range(20):
            portion = self.shot[x_nums_pos[1]:x_nums_pos[1]+height, x_nums_pos[0]+spacing*i:x_nums_pos[0]+width+spacing*i]
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

class Resources:

    def __init__(self):
        self.shot = None
        self.path = "data/resource_numbers"

    def get_number(self, number):
        best_weight = -100
        best_digit = -1
        all_weights=[]
        num_images = [f'{self.path}/{i}.png' for i in range(10)]
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
        avg_c = np.average(number, axis=(0,1))
        if best_weight <500000 or avg_c[0] == 0 or avg_c[1] == 0 or avg_c[2] == 0 or avg_c[0] != avg_c[1] or avg_c[1] != avg_c[2]:
            return "empty"
        return best_digit

    def get_resources(self, shot):
        self.shot = shot 

        num_width = 10
        num_height = 14
        spacing = num_width+2

        iron_str = ""
        iron_pos = [86, 228]
        gold_str = ""
        gold_pos = [84, 248]
        diamond_str = ""
        diamond_pos = [130, 268]
        emerald_str = ""
        emerald_pos = [132, 288]
        result = [0, 0, 0, 0]

        acc = 6

        for i in range(acc):
            portion = self.shot[iron_pos[1]:iron_pos[1]+num_height, iron_pos[0]+spacing*i:iron_pos[0]+num_width+spacing*i]
            n = str(self.get_number(portion))
            if n == "empty":
                break
            iron_str += n

        for i in range(acc):
            portion = self.shot[gold_pos[1]:gold_pos[1]+num_height, gold_pos[0]+spacing*i:gold_pos[0]+num_width+spacing*i]
            n = str(self.get_number(portion))
            if n == "empty":
                break
            gold_str += n

        for i in range(acc):
            portion = self.shot[diamond_pos[1]:diamond_pos[1]+num_height, diamond_pos[0]+spacing*i:diamond_pos[0]+num_width+spacing*i]
            if n == "empty":
                break
            diamond_str += n

        for i in range(acc):
            portion = self.shot[emerald_pos[1]:emerald_pos[1]+num_height, emerald_pos[0]+spacing*i:emerald_pos[0]+num_width+spacing*i]
            if n == "empty":
                break
            emerald_str += n

        for i, s in enumerate([iron_str, gold_str, diamond_str, emerald_str]):
            result[i] = 0 if s == "" else int(s)

        return result
        

