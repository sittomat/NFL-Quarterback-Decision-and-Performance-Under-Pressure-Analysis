import pandas as pd

def process_qb_pressure_data(games_file, player_play_file, players_file, plays_file, pressure=True):
    """
    Processes NFL game data to extract quarterback plays related to defensive pressure.
    
    Args:
        games_file (str): Path to games.csv
        player_play_file (str): Path to player_play.csv
        players_file (str): Path to players.csv
        plays_file (str): Path to plays.csv
        pressure (bool): Determines whether to create a dataset of QB plays with or without pressure
        
    Returns:
        pd.DataFrame: Cleaned DataFrame with quarterback plays related to pressure.
    """
    # Load datasets
    games_df = pd.read_csv(games_file)
    player_play_df = pd.read_csv(player_play_file)
    players_df = pd.read_csv(players_file)
    plays_df = pd.read_csv(plays_file)
    
    # Filter for quarterbacks
    quarterbacks_players = players_df[players_df['position'] == 'QB'].reset_index(drop=True)
    quarterback_ids = quarterbacks_players['nflId'].unique().tolist()
    
    # Create unique identifiers
    player_play_df['game_play_id'] = player_play_df['gameId'].astype(str) + ' ' + player_play_df['playId'].astype(str)
    player_play_df['game_play_nfl_id'] = player_play_df['game_play_id'] + ' ' + player_play_df['nflId'].astype(str)
    plays_df['game_play_id'] = plays_df['gameId'].astype(str) + ' ' + plays_df['playId'].astype(str)
    
    # Identify plays under pressure
    pressure_play_ids = player_play_df[player_play_df['causedPressure'] == True]['game_play_id'].unique().tolist()
    if pressure == True:
        pressure_player_play_df = player_play_df[player_play_df['game_play_id'].isin(pressure_play_ids)]
    else:
        pressure_player_play_df = player_play_df[~player_play_df['game_play_id'].isin(pressure_play_ids)]
    
    # Filter for quarterbacks under pressure
    qb_pressure_plays_df = pressure_player_play_df[pressure_player_play_df['nflId'].isin(quarterback_ids)]
    
    # Handle duplicate quarterback plays
    duplicate_qb_mask = qb_pressure_plays_df.duplicated(subset=['gameId', 'playId'], keep=False)
    duplicate_qb_plays_df = qb_pressure_plays_df[duplicate_qb_mask].reset_index(drop=True)
    
    keep_ids = []
    for _, row in duplicate_qb_plays_df.iterrows():
        game_play_id = row['game_play_id']
        for _, qb in quarterbacks_players.iterrows():
            if qb['displayName'].split()[-1] in str(plays_df[plays_df['game_play_id'] == game_play_id]['playDescription']):
                keep_ids.append(game_play_id + ' ' + str(qb['nflId']))
                break
    
    # Remove incorrect QB entries
    invalid_qb_ids = duplicate_qb_plays_df[~duplicate_qb_plays_df['game_play_nfl_id'].isin(keep_ids)]['game_play_nfl_id'].tolist()
    qb_pressure_plays_df = qb_pressure_plays_df[~qb_pressure_plays_df['game_play_nfl_id'].isin(invalid_qb_ids)]
    
    # Get valid plays
    plays_with_qb_pressure_df = plays_df[plays_df['game_play_id'].isin(qb_pressure_plays_df['game_play_id'].tolist())]
    
    # Merge data sets
    plays_with_qb_pressure_df = pd.merge(plays_with_qb_pressure_df, games_df, on=['gameId'])
    qb_plays_final_df = pd.merge(qb_pressure_plays_df, plays_with_qb_pressure_df, on=['game_play_id'])
    qb_plays_final_df = pd.merge(qb_plays_final_df, quarterbacks_players, on=['nflId'])
    
    # Final cleanup
    qb_plays_final_df.drop(columns=['gameId_y', 'playId_y', 'nflId'], inplace=True)
    qb_plays_final_df.rename(columns={'gameId_x': 'gameId', 'playId_x': 'playId'}, inplace=True)

    # Create scoreDelta column to find score differential in each play
    qb_plays_final_df['scoreDelta'] = qb_plays_final_df.apply(
        lambda row: row['preSnapHomeScore'] - row['preSnapVisitorScore']
        if row['teamAbbr'] == row['homeTeamAbbr']
        else row['preSnapVisitorScore'] - row['preSnapHomeScore'],
        axis=1
    )
    
    # Select final columns
    final_columns = [
        'gameId', 'playId', 'game_play_id', 'scoreDelta', 'displayName', 'down', 
        'yardsToGo', 'absoluteYardlineNumber', 'passResult', 'prePenaltyYardsGained', 
        'passLength', 'timeToThrow', 'timeInTackleBox', 'hadRushAttempt', 'rushingYards', 
        'qbSneak', 'qbKneel', 'qbSpike', 'passingYards']
    qb_plays_final_df = qb_plays_final_df[final_columns]
    

    return qb_plays_final_df

if __name__ == "__main__":
    # Example usage
    games_file = "games.csv"
    player_play_file = "player_play.csv"
    players_file = "players.csv"
    plays_file = "plays.csv"

    # Run function with pressure
    pressure = True
    qb_with_pressure_df = process_qb_pressure_data(games_file, player_play_file, players_file, plays_file, pressure)
    
    # Save results to CSV
    output_file = "qb_with_pressure_plays.csv"
    qb_with_pressure_df.to_csv(output_file, index=False)
    print(f"Processed QB pressure data saved to {output_file}")

    qb_with_pressure_df = process_qb_pressure_data(games_file, player_play_file, players_file, plays_file, pressure)

    # Run function without pressure
    pressure = False
    qb_without_pressure_df = process_qb_pressure_data(games_file, player_play_file, players_file, plays_file, pressure)

    # Save results to CSV
    output_file = "qb_without_pressure_plays.csv"
    qb_without_pressure_df.to_csv(output_file, index=False)
    print(f"Processed QB pressure data saved to {output_file}")
