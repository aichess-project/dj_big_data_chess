import re
import yaml
import os
import threading
from datetime import datetime

EVAL_PATTERN = "[%eval "
MIN_ELO = 2200
MIN_COMMENTED_ELO = 2000

# Create a lock object
file_lock = threading.Lock()

def clean_moves(moves):
    # Remove: [%clk 0:02:59]
    pattern = r"\[%clk (.*?)\]"
    updated_text = re.sub(pattern, "", moves)
    # Pattern to match "{<whitespaces>}"
    pattern = r"\{\s*\}"
    return re.sub(pattern, "", updated_text)

def eco_write(eco, base_folder, file_path, header_str, moves, part = None):
    if eco == "?":
        return
    outfile = eco
    if part is not None:
        outfile += "_" + str(part)
    outfile += ".pgn"
    filename = os.path.join(base_folder, file_path, outfile)
    with file_lock:
        with open(filename, 'a') as f:  # 'a' mode is for appending to the file
            f.write(header_str)
            f.write(clean_moves(moves)+"\n")

def create_eco_elo_dict(yaml_data):
    return {item['ECO-Code']: {'ELO_MIN_WHITE': item['ELO_MIN_WHITE'], 'ELO_MIN_BLACK': item['ELO_MIN_BLACK']} for item in yaml_data['ECO_pattern']}

def check_elo(eco_code, white_elo, black_elo, eco_elo_dict, commented = False):
    if eco_elo_dict is None:
        if commented:
            min_elo_white = MIN_COMMENTED_ELO
            min_elo_black = MIN_COMMENTED_ELO
        else:
            min_elo_white = MIN_ELO
            min_elo_black = MIN_ELO

    elif eco_code in eco_elo_dict:
        min_elo_white = eco_elo_dict[eco_code]['ELO_MIN_WHITE']
        min_elo_black = eco_elo_dict[eco_code]['ELO_MIN_BLACK']
    
    else:
        return False
    
    return white_elo >= min_elo_white and black_elo >= min_elo_black

def read_pgn(filename):
    try:
        with open(filename, 'r') as file:
            headers = {}
            headers_str = ""
            moves = ""
            reading_headers = True
            
            for line in file:
                line = line.strip()
                
                # Detect blank line, indicating end of headers and beginning of moves
                if line == "":
                    if reading_headers:
                        reading_headers = False  # Start reading moves
                    else:
                        # If we reach another blank line, the game is over
                        yield headers, headers_str, moves
                        # Reset for the next game
                        headers = {}
                        headers_str = ""
                        moves = ""
                        reading_headers = True
                elif reading_headers:
                    # Parse header line
                    if line.startswith('[') and line.endswith(']'):
                        key, value = line[1:-1].split(' ', 1)
                        headers[key] = value.strip('"')
                        headers_str += line+"\n"
                else:
                    # Append moves
                    moves += line + " "
            
            # Yield the last game if the file doesn't end with a blank line
            if headers and moves:
                yield headers, headers_str, moves
    except Exception as e:
        print(f"Error: {e}")

def ignore_event(event):
    if "BULLET" in event.upper():
        return True
    return False

def extract_eco_games(base_folder, split_folder, eco_folder, commented_folder, split_nr, eco_config_file):
    
    if eco_config_file is None:
        eco_dict = None
    else:
        try:
            with open(eco_config_file, 'r') as file:
                eco_pattern_data = yaml.safe_load(file)
                eco_dict = create_eco_elo_dict(eco_pattern_data)
        except Exception as e:
            print(f"Error: {e}")
            return
    pattern = re.compile(rf'.+_{str(split_nr)}\.pgn')
    # Find all matching files
    matching_files = [f for f in os.listdir(os.path.join(base_folder, split_folder)) if pattern.search(f)]
    # Print the matching files
    for file in matching_files:
        file_name = os.path.join(base_folder, split_folder, file)
        print(file_name, datetime.now())
        for headers, headers_str, moves in read_pgn(file_name):
            commented = False
            ignore = ignore_event(headers.get('Event', 'Not Available'))
            eco_code = headers.get('ECO', 'Not Available')
            elo_white = int(headers.get('WhiteElo', 0))
            elo_black = int(headers.get('BlackElo', 0))
            if EVAL_PATTERN in moves:
                commented = True
            if not ignore:
                if commented and commented_folder is not None:
                    if check_elo(eco_code, elo_white, elo_black, eco_elo_dict = None, commented = True):
                        eco_write(eco_code, base_folder, commented_folder, headers_str, moves, split_nr)
                if check_elo(eco_code, elo_white, elo_black, eco_dict):
                    eco_write(eco_code, base_folder, eco_folder, headers_str, moves, split_nr)

BASE_FOLDER = "/Volumes/BIGWD8/Datalake/chess/lichess_downloads"
#BASE_FOLDER = "/Volumes/T1_Mini/BigDataChess"
SPLIT_FOLDER = "pgn_split"
ECO_FOLDER = "eco"
COMMENTED_FOLDER = "eco_commented"
#ECO_CONFIG_FILE = "/Users/littlecapa/GIT/django/dj_big_data_chess/big_data_chess/tests/playground/ECO_pattern.yaml"
ECO_CONFIG_FILE = None

for i in range(1,999):
    print(datetime.now(), i, BASE_FOLDER)
    extract_eco_games(BASE_FOLDER, SPLIT_FOLDER, ECO_FOLDER, COMMENTED_FOLDER, i, ECO_CONFIG_FILE)
