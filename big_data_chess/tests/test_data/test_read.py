import chess
import chess.pgn


def read_pgn_file(file_path):
    try:
        with open(file_path, 'r') as file:
            game = chess.pgn.read_game(file)

            if game is None:
                print("No valid PGN game found.")
                return

            print("\nGame Information:")
            print(game)

            # Print the moves
            print("\nMoves:")
            board = game.board()
            for move in game.mainline_moves():
                print(board.san(move))
                board.push(move)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Replace 'your_file.pgn' with the path to your PGN file
    read_pgn_file('test.pgn')
