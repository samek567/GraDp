from cgitb import handler
import server_network
import game_logic
import threading
import time

def main():
    game_board = game_logic.Board()
    handler = server_network.Network()

    accept_connection_thread = threading.Thread(target=handler.keep_accepting,args=(game_board,))
    accept_connection_thread.start()

    #handler.keep_accepting(game_board)

    running = True
    while running:
        handler.send_to_everyone(game_board.convert_to_dict())

        for data_recived in handler.get_from_everyone():
            print(data_recived)

        time.sleep(1/10)

if __name__ == "__main__":
    main()