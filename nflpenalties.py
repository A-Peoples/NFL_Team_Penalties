
#importing packages
import pandas as pd
import sportsdataverse as sdv
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(page_title='NFL Penalty Charting', layout="wide")
@st.cache_data()
def load_data():
  team_pen = pd.read_csv("https://raw.githubusercontent.com/A-Peoples/NFL_Team_Penalties/refs/heads/main/penalty_count.csv")
  pen_person = pd.read_csv("https://raw.githubusercontent.com/A-Peoples/NFL_Team_Penalties/refs/heads/main/pen_person.csv")
  pen_type = pd.read_csv("https://raw.githubusercontent.com/A-Peoples/NFL_Team_Penalties/refs/heads/main/pen_type.csv")
  colors = pd.read_csv("https://raw.githubusercontent.com/A-Peoples/NFL_Team_Penalties/refs/heads/main/colors.csv")
  return team_pen, pen_person, pen_type, colors
team_pen, pen_person, pen_type, colors = load_data()
team_list = team_pen['penalty_team'].dropna().unique().tolist()
team_filt = st.sidebar.selectbox('Choose team: ', team_list)
year_filt = st.slider('Year Details: ', 2016, 2024, 2024)
colors = colors.loc[colors['team_abbr'] == team_filt]
color_filt = colors['team_color'].iloc[0]
tab_yearspan, pen_yards, tab_types, tab_player = st.tabs(['Team Penalties Timespan', 'Penalty Yards Timespan', 'Common Team Penalties', 'Player Penalty Count'])
with tab_yearspan:
  st.header(team_filt + ' Team Penalties Timespan')
  
  team_pen = team_pen.loc[team_pen['penalty_team'] == team_filt]
  st.line_chart(data=team_pen, x='season', y='penalty', x_label='Season', y_label='Penalties', color=color_filt)
with pen_yards:
  st.header(team_filt + ' Penalty Yards Timespan')
  
  team_pen = team_pen.loc[team_pen['penalty_team'] == team_filt]
  st.line_chart(data=team_pen, x='season', y='penalty_yards', x_label='Season', y_label='Penalties', color=color_filt)
with tab_player:
  st.header(team_filt + ' Player Penalty Count')
  pen_person = pen_person.loc[(pen_person['season'] == year_filt) & (pen_person['penalty_team'] == team_filt)]
  st.bar_chart(data=pen_person, x='penalty_player_name', y='penalty', x_label='Total Penalties', y_label='Player', color=color_filt, horizontal=True, sort=True, stack=None, width="stretch", height="content", use_container_width=None)
with tab_types:
  st.header(team_filt + ' Common Team Penalties')
  pen_type = pen_type.loc[(pen_type['season'] == year_filt) & (pen_type['penalty_team'] == team_filt)]
  st.bar_chart(data=pen_type, x='penalty_type', y='penalty', x_label='Total Penalties', y_label='Penalty Type', color=color_filt, horizontal=True, sort=True, stack=None, width="stretch", height="content", use_container_width=None)
#with tab_positions:
  #st.header('Position Penalties')
  
  #pos_pen = pos_pen.sort_values(by="penalty", ascending=True).reset_index()
  #st.bar_chart(data=pos_pen, x='depth_chart_position', y='penalty', x_label='Total Penalties', y_label='Position', color=None, horizontal=True, sort=True, stack=None, width="stretch", height="content", use_container_width=None)

