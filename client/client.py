import socket
import pygame as pg
import json
import client_network 
from screeninfo import get_monitors
import time
import math

black = (0,0,0)
red = (255,0,0)
green = (0,255,0)

def draw_map(screen, screen_dimensions, board, player, size_square):

    FOV_y = player["FOV_x"] * screen_dimensions[1] / screen_dimensions[0]

    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[j][i]:
                x = ((i * size_square - player["position_x"]) / player["FOV_x"] + 1) * screen_dimensions[0] / 2
                y = ((j * size_square - player["position_y"]) / FOV_y + 1) * screen_dimensions[1] / 2
                square_size_to_display = (screen_dimensions[0] / 2) * (size_square / FOV_y) + 1
                pg.draw.rect(screen,red,(x,y,square_size_to_display,square_size_to_display))


def normalize_vector(vector):
    # Vector typu krotka
    x,y = vector
    vector_lenght = math.sqrt(x*x + y*y)
    return (x / vector_lenght, y / vector_lenght)



def main():
    while True:
        try:
            print("Podaj nick: ")
            nick = input()
            handler = client_network.Network("localhost",8500)
            handler.send_data({"nick" : nick})
            message = handler.get_data()
            print(message["Wiadomosc"])
            break
        except:
            print("Ten nick jest juz w grze")

    got = handler.get_data()

    print(got.keys())

    board = got["board"]
    square_size = got["square_size"]

    img_player = pg.image.load("./images/player_img.png")


    pg.init()

    screen_width = 1000
    screen_height = 1000
    screen = pg.display.set_mode((screen_width,screen_height))

    running = True
    while running:


        recived = handler.get_data()

        players = recived["players"]
        bullets = recived["bullets"]

        #print(players)
        player = players[nick]

       # print(recived.keys())

        #print(f"Typ playera: {type(player)}" )

        keys_pressed = pg.key.get_pressed()


        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        if keys_pressed[pg.K_ESCAPE]:
            running = False

        x_mouse,y_mouse = pg.mouse.get_pos()
        direction = (x_mouse - screen_width / 2, y_mouse - screen_height / 2)
        direction = normalize_vector(direction)

        handler.send_data({
            "arrows_pressed": [keys_pressed[pg.K_UP],keys_pressed[pg.K_DOWN],keys_pressed[pg.K_LEFT],keys_pressed[pg.K_RIGHT]],
            "direction": direction,
            "mouse_pressed": pg.mouse.get_pressed(num_buttons=3),
            "extra_info": []
        })


        screen.fill((255, 255, 255))
        draw_map(screen,(screen_width,screen_height),board,player,square_size)
        #pg.draw.circle(screen,black,(screen_width / 2,screen_height / 2),player["hit_box_radius"])
        screen.blit(img_player,(screen_width / 2 - 200 / 2,screen_height / 2 - 200 / 2))

        for bullet in bullets:
            pg.draw.circle(screen,green,(bullet["position_x"],bullet["position_y"]),10)
        print(len(bullets))

        pg.display.flip()

    pg.quit()

    print(board)

if __name__ == "__main__":
    main()
     