import os
import re
from datetime import datetime

def open_next_split_file(split_file_path, pgn_file_name, counter):
    print(counter, datetime.now())
    new_file_name = pgn_file_name.replace(".pgn", "_" + str(counter) + ".pgn")
    filename = os.path.join(split_file_path, new_file_name)
    return open(filename, 'w')

def split_pgn_file(pgn_file_path, pgn_file_name, split_file_path, games_per_file):
    
    event_pattern = re.compile(r'^\[Event ".*"\]')
    game_counter = 0
    file_counter = 1
    output_file = open_next_split_file(split_file_path, pgn_file_name, file_counter)

    with open(os.path.join(pgn_file_path, pgn_file_name), 'r') as pgn_file:
        for line in pgn_file:
            if event_pattern.match(line) and game_counter >= games_per_file:
                output_file.close()
                file_counter += 1
                output_file = open_next_split_file(split_file_path, pgn_file_name, file_counter)
                game_counter = 0

            output_file.write(line)
            
            # Increment the game counter when an [Event] line is found
            if event_pattern.match(line):
                game_counter += 1

    output_file.close()
    return file_counter  # Return the number of chunks created   
    
# Path to the PGN file
pgn_file_path = '/Volumes/BIGWD8/Datalake/chess/lichess_downloads/pgn'
pgn_file_name = "lichess_db_standard_rated_2024-10.pgn"
# Path to save the DataFrame
#split_file_path = '/Volumes/T1_Mini/BigDataChess/pgn_split/'
split_file_path = '/Volumes/BIGWD8/Datalake/chess/lichess_downloads/pgn_split/'

split_pgn_file(pgn_file_path, pgn_file_name, split_file_path, 1e5)
