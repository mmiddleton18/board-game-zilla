import numpy as np

#------CONSTANTS--------
FLEETING_INTEREST = 0.9

def pick_game(votes: np.ndarray, times_played: np.ndarray) -> int:
    votes_accum = get_accum(votes)
    played_accum = get_accum(times_played)
    proportional_votes = votes_accum/np.sum(votes_accum)
    proportinal_times_played = played_accum/np.sum(played_accum)
    if np.isnan(proportinal_times_played).any():
        return np.argmax(proportional_votes)
    diff = proportional_votes - proportinal_times_played
    diff = remove_non_voted_games(diff, votes[-1,:])
    return np.argmax(diff)

def get_accum(array: np.ndarray) -> np.ndarray:
    accum = np.zeros((1,array.shape[1]))
    for row in array:
        accum = FLEETING_INTEREST*accum + row
    return accum

def remove_non_voted_games(diff: np.ndarray, latest_vote: np.ndarray) -> np.ndarray:
    destroying_array = []
    for vote in latest_vote:
        if vote <= 0:
            destroying_array.append(-1000)
        else:
            destroying_array.append(1)
    return diff + np.array(destroying_array)

if __name__ == '__main__':
    votes = np.array([
        [0,1,2,100,4,5],
        [0,1,2,0,4,5]
    ])
    times_played = np.array([
        [0,0,0,0,0,1],
        [0,0,0,0,1,0]
    ])

    game_idx = pick_game(votes, times_played)
    print(game_idx)
    