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
    return np.argmax(diff)

def get_accum(array: np.ndarray) -> np.ndarray:
    accum = np.zeros((1,array.shape[1]))
    for row in array:
        accum = FLEETING_INTEREST*accum + row
    return accum
    