from email.mime import image
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

def change_cordinate(screen_dimension,FOV,coordinate,player_coordinate):
    return ((coordinate - player_coordinate) / FOV + 1) * screen_dimension / 2

def login():
    '''
    To jest funkcja odpowiadajaca za logowanie gracza do gry. Zwracajaca nick i dane o grze.
    '''
    while True:
        try:
            print("Podaj nick: ")
            nick = input()
            handler = client_network.Network("localhost",8500)
            handler.send_data({"nick" : nick})
            message = handler.get_data()
            print(message["Wiadomosc"])
            got = handler.get_data()

            return nick,got["board"],got["square_size"], handler
        except:
            print("Ten nick jest juz w grze")
    



def main():

    screen_width = 1000
    screen_height = 1000
    screen = pg.display.set_mode((screen_width,screen_height))

    nick,board,square_size,handler = login()
    pg.init()

    img_player = pg.image.load("./images/player_img.png")

    running = True
    while running:

        recived = handler.get_data()
        players = recived["players"]
        bullets = recived["bullets"]
        player = players[nick]
        FOV_y = player["FOV_x"] * screen_height / screen_width

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
        # To jest funkcja rysujaca mape.
        draw_map(screen,(screen_width,screen_height),board,player,square_size)

        # Wyswietlamy pociski
        for bullet in bullets:
            pg.draw.circle(screen,green,(change_cordinate(screen_width,player["FOV_x"],bullet["position_x"],player["position_x"]),change_cordinate(screen_height,FOV_y,bullet["position_y"],player["position_y"])),10)
        print(len(bullets))

        # Wyswietlamy playerow
        for nick,i in players.items():
            screen.blit(img_player,(change_cordinate(screen_width,player["FOV_x"],i["position_x"],player["position_x"]) - img_player.get_width() / 2,change_cordinate(screen_width,FOV_y,i["position_y"],player["position_y"]) - img_player.get_height() / 2))

        pg.display.flip()

    pg.quit()

if __name__ == "__main__":
    main()
     