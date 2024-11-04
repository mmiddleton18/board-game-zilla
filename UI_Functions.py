import pandas as pd
import numpy as np

def game_already_played(df_played: pd.DataFrame) -> bool:
    if np.sum(df_played.values[-1,2::]) > 0:
        return True
    return False