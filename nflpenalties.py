#importing packages
import pandas as pd
import sportsdataverse as sdv
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(page_title='NFL Penalty Charting', layout="wide")
@st.cache_data()
def load_data():
  pbp = sdv.nfl.load_nfl_pbp((range(2020, 2024+1)), return_as_pandas=True)
  roster = sdv.nfl.load_nfl_rosters(range(2020, 2024+1), return_as_pandas=True)
  return pbp, roster
pbp, roster = load_data()

team_list = sorted(pbp['penalty_team'].unique().dropna().tolist())

team_filt = st.sidebar.selectbox('Choose team: ', team_list)
year_filt = st.slider('Year Details: ', 2020, 2024, 2024)
pbp_team_filt = pbp.loc[((pbp['home_team'] == team_filt) | (pbp['away_team'] == team_filt)) & (pbp['penalty_team'] == team_filt)]
pbp_filt = pbp.loc[((pbp['home_team'] == team_filt) | (pbp['away_team'] == team_filt))]

tab_yearspan, tab_types = st.tabs(['Team Penalties Timespan', 'Common Team Penalties'])
#tab_yearspan, tab_types, tab_player, tab_positions = st.tabs(['Team Penalties Timespan', 'Common Team Penalties', 'Top 20 Player Penalties', 'Position Penalties'])
with tab_yearspan:
  st.header('Team Penalties Timespan')
  team_pen = pbp_team_filt.groupby(['penalty_team', 'season']).agg({'penalty': ['count'],
                                                        }).reset_index()

  avg_pen = pbp_filt.groupby(['season']).agg({'penalty': ['count'],
                                                        }).reset_index()
  avg_pen['penalty'] = avg_pen['penalty'] / 32
  avg_pen = avg_pen.rename(columns={'penalty_team_': "penalty_team",
                                      'season_': "season"})

  team_pen.columns = list(map("_".join, team_pen.columns))
  team_pen = team_pen.rename(columns={'penalty_team_': "penalty_team",
                                      'season_': "season"})

  st.line_chart(data=team_pen, x='season', y='penalty_count', x_label='Season', y_label='Penalties', width="stretch", height="content", use_container_width=None)
with tab_types:
  st.header('Common Team Penalties')
  pen_person = pbp_team_filt.groupby(['penalty_player_name', 'penalty_player_id', 'season', 'penalty_team']).agg({'penalty': 'count'}).reset_index()
  pen_person = pen_person.loc[(pen_person['penalty_team'] == team_filt) & (pen_person['season'] == year_filt)]
  pen_person = pen_person.drop_duplicates(subset=['penalty_player_id'])
  pen_person = pen_person.sort_values(by="penalty", ascending=False).reset_index()
  pen_person_filt = pen_person.head(20)
  pen_person_filt = pen_person_filt[::-1]
  pen_person = pen_person.loc[(pen_person['penalty_player_id'].isin(roster['gsis_id']))]
  st.bar_chart(data=pen_person_filt, x='penalty_player_name', y='penalty', x_label='Total Penalties', y_label='Player', color=None, horizontal=True, sort=True, stack=None, width="stretch", height="content", use_container_width=None)
  pen_person_filt = pen_person_filt[::-1]
