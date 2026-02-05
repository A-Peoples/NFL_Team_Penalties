
#importing packages
import pandas as pd
import sportsdataverse as sdv
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(page_title='NFL Penalty Charting', layout="wide")
@st.cache_data()


team_list = sorted(pbp['penalty_team'].unique().dropna().tolist())

team_filt = st.sidebar.selectbox('Choose team: ', team_list)
year_filt = st.slider('Year Details: ', 2023, 2024, 2024)
pbp_team_filt = pbp.loc[((pbp['home_team'] == team_filt) | (pbp['away_team'] == team_filt)) & (pbp['penalty_team'] == team_filt)]
pbp_filt = pbp.loc[((pbp['home_team'] == team_filt) | (pbp['away_team'] == team_filt))]

tab_yearspan, tab_types, tab_player, tab_positions = st.tabs(['Team Penalties Timespan', 'Common Team Penalties', 'Top 20 Player Penalties', 'Position Penalties'])
with tab_yearspan:
  st.header('Team Penalties Timespan')
  team_pen = pd.read_csv("https://raw.githubusercontent.com/A-Peoples/NFL_Team_Penalties/refs/heads/main/penalty_count.csv")
  team_pen = team_pen.loc[team_pen['team'] == "team_filt"]
  st.line_chart(data=team_pen, x='season', y='penalty_count', x_label='Season', y_label='Penalties', width="stretch", height="content", use_container_width=None)
with tab_player:
  st.header('Top 20 Player Penalties')
  pen_person = pbp_team_filt.groupby(['penalty_player_name', 'penalty_player_id', 'season', 'penalty_team']).agg({'penalty': 'count'}).reset_index()
  pen_person = pen_person.loc[(pen_person['penalty_team'] == team_filt) & (pen_person['season'] == year_filt)]
  pen_person = pen_person.drop_duplicates(subset=['penalty_player_id'])
  pen_person = pen_person.sort_values(by="penalty", ascending=False).reset_index()
  pen_person_filt = pen_person.head(20)
  pen_person_filt = pen_person_filt[::-1]
  pen_person = pen_person.loc[(pen_person['penalty_player_id'].isin(roster['gsis_id']))]
  st.bar_chart(data=pen_person_filt, x='penalty_player_name', y='penalty', x_label='Total Penalties', y_label='Player', color=None, horizontal=True, sort=True, stack=None, width="stretch", height="content", use_container_width=None)
  pen_person_filt = pen_person_filt[::-1]
with tab_types:
  st.header('Common Team Penalties')
  pen_type = pbp_team_filt.groupby(['penalty_team', 'season', 'penalty_type']).agg({'penalty': 'count'}).reset_index()

  st.bar_chart(data=pen_type, x='penalty_type', y='penalty', x_label='Total Penalties', y_label='Penalty Type', color=None, horizontal=True, sort=True, stack=None, width="stretch", height="content", use_container_width=None)

  plt.show()
with tab_positions:
  st.header('Position Penalties')
  player_lists = list(pen_person['penalty_player_id'])

  roster_filt = roster.loc[(roster['gsis_id'].isin(pen_person['penalty_player_id'])) & (roster['season'] == year_filt)]
  pen_person = pen_person.loc[(pen_person['penalty_player_id'].isin(roster['gsis_id']))]

  roster_filt = roster_filt[['gsis_id', 'position', 'depth_chart_position', 'headshot_url', 'full_name']]
  roster_filt = roster_filt.rename(columns={'gsis_id': 'penalty_player_id'})
  roster_filt_merge = pen_person.merge(roster_filt, on='penalty_player_id', how='left')
  pos_pen = roster_filt_merge.groupby(['depth_chart_position']).agg({'penalty': sum}).reset_index()
  pos_pen = pos_pen.sort_values(by="penalty", ascending=True).reset_index()
  st.bar_chart(data=pos_pen, x='depth_chart_position', y='penalty', x_label='Total Penalties', y_label='Position', color=None, horizontal=True, sort=True, stack=None, width="stretch", height="content", use_container_width=None)

