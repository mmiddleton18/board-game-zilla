import streamlit as st
import pandas as pd
import numpy as np

def game_already_played(df_played: pd.DataFrame) -> bool:
    if np.sum(df_played.values[-1,2::]) > 0:
        return True
    return False

def first_load():
    if st.session_state.get("page_reloaded") is None:
        # This will be true only on the first load
        st.cache_data.clear()
        st.cache_resource.clear()
        st.session_state["page_reloaded"] = True  # Set a flag so it doesn’t clear cache again in this session