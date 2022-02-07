'''Creating a web app that shows the pass maps for all players in the Euro 2020 Final'''
from statsbombpy import sb
import pandas as pd
from mplsoccer import Pitch
# from matplotlib import rcParams
# import matplotlib.pyplot as plt
# import numpy as np
import streamlit as st
# import pydeck as pdk

euro = sb.matches(competition_id = 55, season_id=43)
countries = list(set(euro['home_team']) & set(euro['away_team']))
country_input = st.sidebar.selectbox('Country Team', countries)
# st.sidebar.radio('Game Select',options=countries)
@st.cache(persist=True)
def load_games(country):
    '''loads the games after a country is selected'''
    filt = (euro['home_team'] == country) | (euro['away_team'] == country)
    games = euro[filt]
    return games

games_load = load_games(country_input)
game_input = st.sidebar.selectbox('Games',options=games_load['home_team'] + ' vs. '+ games_load['away_team'] + ' ' + games_load['match_id'].apply(str))

#find a way to get final_match_id from the specific game selected in game_input
final_match = game_input.split()
final_events = sb.events(match_id=final_match[-1], split=True, flatten_attrs=False)

# just get the key information from the passes
all_passes = final_events['passes'][['period','location','player','pass']].copy()
# split the start location into two columns for x and y
pass_start = pd.DataFrame(all_passes['location'].to_list(),columns=['x_start','y_start'])
# expand the pass column into a dataframe
pass_info = all_passes['pass'].apply(pd.Series)
# next two lines create a column with the recipient's name alone
recipient_name = pass_info['recipient'].apply(pd.Series)
recipient_name.rename(columns={'name':'recipient_name'},inplace=True)
# split the end location into two columns for x and y
pass_end = pd.DataFrame(pass_info['end_location'].to_list(),columns=['x_end','y_end'])
#create final dataframe which has all the info including the added columns we invented
df = pd.concat([all_passes,pass_start,pass_end, recipient_name,pass_info],axis=1)

# layout of the streamlit app
st.title('The Euro 2020 Final')
st.header("Comparing two player's pass maps")
# col1, col2, col3 = st.columns([8,1,8])

# creating the dropdown menus for each team based on the lineup,
# specifically excluding squad players who did not feature
team1_str = final_match[0]
team2_str = final_match[2]
team1_lineup = sb.lineups(final_match[-1])[team1_str]
team2_lineup = sb.lineups(final_match[-1])[team2_str]
team1_squad = list(set(team1_lineup['player_name']) & set(df['player']))
team2_squad = list(set(team2_lineup['player_name']) & set(df['player']))

player1_input = st.sidebar.selectbox(f'{team1_str} Player Name', team1_squad)
player2_input = st.sidebar.selectbox(f'{team2_str} Player Name', team2_squad)

# what data to load up
@st.cache(persist=True)
def load_data(playername):
    '''Take the player inputted and return the dataframe of their completed passes'''
    playerfilt = (df['player'] == playername)
    data_frame = df.loc[playerfilt]
    mask = data_frame.outcome.isnull()
    completed_passes = data_frame[mask]
    return completed_passes

with st.container():
    data = load_data(player1_input)

    pitch = Pitch(pitch_type='statsbomb', pitch_color='#22312b', line_color='#c7d5cc')
    fig, ax = pitch.draw(figsize=(14,9), constrained_layout=True, tight_layout=False)
    fig.set_facecolor('#22312b')
    # ax.set_title(f'{player_input} Completed Passes', fontsize=20, color='white')

    player_fig = pitch.arrows(data.x_start,data.y_start,data.x_end,data.y_end, width=2,
        headwidth=5,headlength=5,color='#ad993c', ax=ax, label='completed passes')
    st.caption(f"{player1_input}'s Completed Passes")

    st.pyplot(fig=fig)

with st.container():
    data = load_data(player2_input)

    pitch = Pitch(pitch_type='statsbomb', pitch_color='#22312b', line_color='#c7d5cc')
    fig, ax = pitch.draw(figsize=(14,9), constrained_layout=True, tight_layout=False)
    fig.set_facecolor('#22312b')
    # ax.set_title(f'{player_input} Completed Passes', fontsize=20, color='white')

    player_fig = pitch.arrows(data.x_start,data.y_start,data.x_end,data.y_end, width=2,
        headwidth=5,headlength=5,color='#ad993c', ax=ax, label='completed passes')

    st.caption(f"{player2_input}'s Completed Passes")

    st.pyplot(fig=fig)

if st.checkbox('Show Raw Data', False):
    st.subheader('Raw Data')
    st.write(data)
