import socket
import pygame as pg
import json
import client_network 
from screeninfo import get_monitors
import time

from game_logic import Board

black = (0,0,0)
red = (255,0,0)

def draw_map(screen, screen_dimensions, board, player, size_square):

    FOV_y = player["FOV_x"] * screen_dimensions[1] / screen_dimensions[0]

    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j]:
                x = ((i * size_square - player["position_x"]) / player["FOV_x"] + 1) * screen_dimensions[0] / 2
                y = ((j * size_square - player["position_y"]) / FOV_y + 1) * screen_dimensions[1] / 2
                square_size_to_display = (screen_dimensions[0] / 2) * (size_square / FOV_y) + 1
                pg.draw.rect(screen,red,(x,y,square_size_to_display,square_size_to_display))



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
    board = got["game_board"]
 

    print(got.keys())

    pg.init()

    size_square = 20 #get_monitors()[0].height // len(board)

    screen_width = 500
    screen_height = 500
    screen = pg.display.set_mode((screen_width,screen_height))

    running = True
    while running:
        recived = handler.get_data()

        players = recived["players"]

        print(players)
        player = players[0]

        print(recived.keys())

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        if pg.key.get_pressed()[pg.K_ESCAPE]:
            running = False

        screen.fill((255, 255, 255))
        draw_map(screen,(screen_width,screen_height),board,player,size_square)

        pg.display.flip()

    pg.quit()

    print(board)

if __name__ == "__main__":
    main()
     