import streamlit as st
from streamlit_gsheets import GSheetsConnection
import logging
from Authenticator import check_password, get_user
from GamerUI import run_gamer_ui
from GameMasterUI import run_gamemaster_ui
from UI_Functions import *

#----- CONFIGURE LOGGER ----------
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(funcName)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
    ]
)

#--------APP START----------
# Clear cache on page reload
first_load()

st.title("Board Game Voting")

if not check_password():
    st.stop()

if get_user() == "Gamer":
    run_gamer_ui()
elif get_user() == "GameMaster":
    run_gamemaster_ui()



