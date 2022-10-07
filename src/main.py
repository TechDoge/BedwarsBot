from player import Player
import cv2

player = Player()
window = cv2.namedWindow("BedwarsBot")

while True:
    player.act()
    screen = player.decisions.current_shot
    cv2.imshow("BedwarsBot", cv2.resize(screen, (192*4, 108*4)))

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break