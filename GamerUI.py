import streamlit as st
from streamlit_gsheets import GSheetsConnection
import logging
from Authenticator import first_load
from UI_Functions import *

def run_gamer_ui():
    conn = st.connection("gsheets", type=GSheetsConnection)

    @st.cache_data
    def load_games_from_sheet():
        df_games = conn.read(worksheet="Games")
        df_played = conn.read(worksheet="Games_Played")
        st.text(f"Current Game Session: {len(df_played.values)}")
        if game_already_played(df_played):
            st.error("Game Session not ready. Have the Game Master set up a new Game Session")
            st.stop()
        num_players = int(df_played.values[-1,0])
        num_votes = int(df_played.values[-1,1])
        return df_games.values, [], num_players, num_votes

    games, game_votes, number_of_players, number_of_votes = load_games_from_sheet()


    for i in range(0,len(games)):
        min_players = games[i,1]
        max_players = games[i,2]
        if number_of_players >= min_players and number_of_players <= max_players:
            game_votes.append(st.number_input(str(games[i,0]), min_value=0, step=1, format="%d"))
        else:
            game_votes.append(0)

    if st.session_state.get("submit_btn_clicked") is None:
        st.session_state["submit_btn_clicked"] = False

    if st.button("Submit Results"):
        if st.session_state["submit_btn_clicked"]:
            st.toast("Your votes have already been submitted",icon='❌')
        elif sum(game_votes) != number_of_votes:
            st.toast(f"Please submit {int(number_of_votes)} votes",icon='❌')
        else:
            df_votes = conn.read(worksheet="Votes")
            logging.info(f"Current Votes: {df_votes.values[-1,:]}")
            df_votes.values[-1,:] += game_votes
            df_votes = conn.update(worksheet="Votes",data=df_votes)
            logging.info(f"New Votes: {df_votes.values[-1,:]}")
            st.session_state["submit_btn_clicked"] = True
            st.balloons()


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(funcName)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
        ]
    )
    first_load()
    run_gamer_ui()