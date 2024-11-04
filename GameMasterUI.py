import streamlit as st
from streamlit_gsheets import GSheetsConnection
import logging
import numpy as np
import pandas as pd
from GameSelection import pick_game
from Authenticator import first_load
from UI_Functions import *

#-------CONSTANTS---------
VOTES_PER_PLAYER = 5

def run_gamemaster_ui():
    conn = st.connection("gsheets", type=GSheetsConnection)
    number_of_players = st.number_input("How Many Players for the Game?",min_value=2, step=1, format="%d")

    if st.button("Start New Game Session"):
        update_games_played(conn, number_of_players)
        update_votes(conn)

    if st.button("Calculate Winner"):
        calculate_winner(conn)

def update_games_played(conn: GSheetsConnection, num_players: int):
    df_played = conn.read(worksheet="Games_Played")
    if not game_already_played(df_played):
        st.error("Most Recent Game not Played Yet. Calculate Winner of Current Game")
        st.stop()
    games_played = len(df_played.values)
    df_new = append_zero_row_to_df(df_played)
    df_new.values[-1,0] = num_players
    df_new.values[-1,1] = VOTES_PER_PLAYER
    df_played = conn.update(worksheet="Games_Played", data=df_new)
    st.toast(f"Game {games_played + 1} created!", icon='🎉')

def update_votes(conn: GSheetsConnection):
    df_votes = conn.read(worksheet="Votes")
    df_votes = conn.update(worksheet="Votes", 
                           data = append_zero_row_to_df(df_votes))
    st.toast("Votes Updated", icon='🎉')

def append_zero_row_to_df(df: pd.DataFrame) -> pd.DataFrame:
    zero_row = np.zeros((1, df.values.shape[1]))
    new_array = np.append(df.values, zero_row, axis=0)
    return pd.DataFrame(new_array, columns=df.columns)

def calculate_winner(conn: GSheetsConnection):
    df_votes = conn.read(worksheet="Votes")
    df_played = conn.read(worksheet="Games_Played")
    number_players = int(df_played.values[-1,0])
    num_votes_per_player = int(df_played.values[-1,1])
    if game_already_played(df_played):
        st.error("A Game was already played, start a new Game session")
        st.stop()
    enough_votes(df_votes, number_players, num_votes_per_player)
    winning_idx = pick_game(df_votes.values, df_played.values[:,2::])
    logging.info(f"Winning idx is {winning_idx}")
    df_played.values[-1,winning_idx + 2] = 1
    df_played = conn.update(worksheet="Games_Played", data=df_played)
    st.text(f"Winner is {df_votes.columns[winning_idx]}")

def enough_votes(df_votes: pd.DataFrame, num_players, num_votes):
    if np.sum(df_votes.values[-1,:]) != int(num_players*num_votes):
        st.error(f"The number of votes ({np.sum(df_votes.values[-1,:])}) does not equal the correct number of players ({num_players})")
        st.stop()

if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(funcName)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
        ]
    )
    first_load()
    run_gamemaster_ui()