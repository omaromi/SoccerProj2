import pandas as pd
from mplsoccer import Pitch, FontManager
from matplotlib import rcParams
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
import pydeck as pdk

DATA_URL = ('/Users/fsa168/Desktop/PythonPractice/SoccerProj2/ITAPassData.csv')

data_source = pd.read_csv(DATA_URL, index_col=0)

st.title('The Euro 2020 Final')
st.header("Comparing two player's pass maps")
col1, col2 = st.columns(2)

ITASquad = list(data_source['player'].value_counts().keys())
player1_input = st.sidebar.selectbox('Player 1 Name', ITASquad)
player2_input = st.sidebar.selectbox('Player 2 Name', ITASquad)


@st.cache(persist=True)
def load_data(playername):
    filt = (data_source['player'] == playername)
    data_frame = data_source.loc[filt]
    mask = data_frame.pass_outcome.isnull()
    completed_passes = data_frame[mask]
    return completed_passes

with col1:
    data = load_data(player1_input)

    pitch = Pitch(pitch_type='statsbomb', pitch_color='#22312b', line_color='#c7d5cc')
    fig, ax = pitch.draw(figsize=(7,4.8), constrained_layout=True, tight_layout=False)
    fig.set_facecolor('#22312b')
    # ax.set_title(f'{player_input} Completed Passes', fontsize=20, color='white')

    player_fig = pitch.arrows(data.x_start,data.y_start,data.x_end,data.y_end, width=2, headwidth=5,headlength=5,color='#ad993c', ax=ax, label='completed passes')
    st.subheader(f"{player1_input}'s Completed Passes")

    st.pyplot(fig=fig)

with col2:
    data = load_data(player2_input)

    pitch = Pitch(pitch_type='statsbomb', pitch_color='#22312b', line_color='#c7d5cc')
    fig, ax = pitch.draw(figsize=(7,4.8), constrained_layout=True, tight_layout=False)
    fig.set_facecolor('#22312b')
    # ax.set_title(f'{player_input} Completed Passes', fontsize=20, color='white')

    player_fig = pitch.arrows(data.x_start,data.y_start,data.x_end,data.y_end, width=2, headwidth=5,headlength=5,color='#ad993c', ax=ax, label='completed passes')
    
    st.subheader(f"{player2_input}'s Completed Passes")

    st.pyplot(fig=fig)

if st.checkbox('Show Raw Data', False):
    st.subheader('Raw Data')
    st.write(data)


