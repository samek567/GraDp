import server_network
import game_logic_board
import threading
import time

def main():
    game_board = game_logic_board.Board()
    handler = server_network.Network(game_board)

    accept_connection_thread = threading.Thread(target=handler.keep_accepting)
    accept_connection_thread.start()

    #handler.keep_accepting(game_board)

    running = True
    old_t = time.time()
    while running:
        dt = time.time() - old_t
        old_t = time.time()
        #print(dt)
        handler.send_to_everyone(game_board.convert_to_dict())

        handler.game_board.update(handler.get_from_everyone(),dt)

        time.sleep(1/40)

if __name__ == "__main__":
    main()