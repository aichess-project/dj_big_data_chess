import chess.pgn
import pandas as pd
import os

def extract_headers(pgn_file_path, output_file_path):
    # Initialize an empty list to store the data
    data = []
    game_count = 0
    
    try:
        # Open and read the PGN file
        with open(pgn_file_path, 'r') as pgn_file:
            # Create a PGN reader
            pgn = chess.pgn.read_game(pgn_file)
            
            while pgn:
                try:
                    # Extract header information for the current game
                    headers = pgn.headers
                    # Convert headers to a dictionary with default values if keys are missing
                    game_data = {
                        'Event': headers.get('Event', ''),
                        'Site': headers.get('Site', ''),
                        'Date': headers.get('Date', ''),
                        'Round': headers.get('Round', ''),
                        'White': headers.get('White', ''),
                        'Black': headers.get('Black', ''),
                        'Result': headers.get('Result', ''),
                        'WhiteElo': headers.get('WhiteElo', ''),
                        'BlackElo': headers.get('BlackElo', ''),
                        'Opening': headers.get('Opening', ''),
                        'Variation': headers.get('Variation', ''),
                        'Annotator': headers.get('Annotator', '')
                    }
                    # Append the game data to the list
                    data.append(game_data)
                    game_count += 1
                    
                    # Print progress every 1000 games
                    if game_count % 1000 == 0:
                        print(f"Processed {game_count} games...")
                    
                    # Read the next game
                    pgn = chess.pgn.read_game(pgn_file)
                
                except Exception as e:
                    # Handle errors reading individual games
                    print(f"Error processing game {game_count + 1}: {e}")
                    # Save current progress
                    if data:
                        df = pd.DataFrame(data)
                        df.to_csv(f"{output_file_path}_partial_{game_count}.csv", index=False)
                    
                    # Skip to the next game
                    pgn = chess.pgn.read_game(pgn_file)
    
    except Exception as e:
        print(f"Error reading PGN file: {e}")
    
    # Final save after processing all games
    if data:
        df = pd.DataFrame(data)
        df.to_csv(output_file_path, index=False)
        print(f"DataFrame saved to {output_file_path}")
# Path to the PGN file
pgn_file_path = '/Volumes/BIGWD8/Datalake/chess/lichess_downloads/pgn/lichess_db_standard_rated_2024-07.pgn'
# Path to save the DataFrame
output_file_path = '/Volumes/BIGWD8/Datalake/chess/lichess_downloads/stats/stats_24_07.csv'

# Extract headers and save to CSV
# Extract headers and save to CSV
extract_headers(pgn_file_path, output_file_path)
