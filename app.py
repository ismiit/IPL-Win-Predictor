import streamlit as st
import pandas as pd
import numpy as np
import pickle
import time
from datetime import datetime
from sklearn.preprocessing import StandardScaler

st.title('IPL WINNER PREDICTOR')

teams = ['Chennai Super Kings', 'Delhi Capitals', 'Gujarat Lions', 'Kings XI Punjab', 'Kolkata Knight Riders', 'Mumbai Indians', 'Rajasthan Royals','Rising Pune Supergiants', 'Royal Challengers Bangalore','Sunrisers Hyderabad']
teams2 = ['Chennai Super Kings', 'Delhi Capitals', 'Gujarat Lions', 'Kings XI Punjab', 'Kolkata Knight Riders', 'Mumbai Indians', 'Rajasthan Royals','Rising Pune Supergiants', 'Royal Challengers Bangalore','Sunrisers Hyderabad']

col1,col2 = st.columns(2)
with col1:
    team1 = st.selectbox('Select TEAM 1',options=teams)
teams2.remove(team1)
with col2:
    team2 = st.selectbox('Select TEAM 2',options=teams2)

stadiums = ['Barabati Stadium','Brabourne Stadium','Buffalo Park','De Beers Diamond Oval','Dr DY Patil Sports Academy','Dr. Y.S. Rajasekhara Reddy ACA-VDCA Cricket Stadium','Dubai International Cricket Stadium','Eden Gardens','Feroz Shah Kotla','Green Park','Himachal Pradesh Cricket Association Stadium','Holkar Cricket Stadium', 'JSCA International Stadium Complex','Kingsmead','M.Chinnaswamy Stadium','MA Chidambaram Stadium, Chepauk','Maharashtra Cricket Association Stadium', 'Nehru Stadium','New Wanderers Stadium','Newlands', 'OUTsurance Oval','Punjab Cricket Association IS Bindra Stadium, Mohali','Punjab Cricket Association Stadium, Mohali','Rajiv Gandhi International Stadium, Uppal','Sardar Patel Stadium, Motera','Saurashtra Cricket Association Stadium','Sawai Mansingh Stadium','Shaheed Veer Narayan Singh International Stadium','Sharjah Cricket Stadium','Sheikh Zayed Stadium',"St George's Park",'Subrata Roy Sahara Stadium','SuperSport Park','Vidarbha Cricket Association Stadium, Jamtha','Wankhede Stadium']
ground = st.selectbox('Select the GROUND / venue',options=stadiums)

toss_teams = [team1,team2]
toss_winner = st.selectbox('Who won the toss ? ',options=toss_teams)

toss_choice = ['Elected To BAT first','Elected to FIELD First']
bat_field = st.selectbox('What did the winning team choose ? ',options=toss_choice)

col3,col4 = st.columns(2)
with col3:
    match_type = ['Eliminator','League']
    match_choice = st.selectbox('What type of match ? ',options=match_type)
with col4:
    year_input = st.number_input('Which year')

teams_dict = {'Chennai Super Kings':0,
              'Sunrisers Hyderabad':1,
              'Delhi Capitals':2,
              'Gujarat Lions':3,
              'Kings XI Punjab':4,
              'Kochi Tuskers Kerala':5,
              'Kolkata Knight Riders':6,
              'Mumbai Indians':7,
              'Rising Pune Supergiants':8,
              'Rajasthan Royals':9,
              'Royal Challengers Bangalore':10}

teamA = teams_dict[team1]
teamB = teams_dict[team2]

except_stadiums = ['Buffalo Park', 'De Beers Diamond Oval','Dubai International Cricket Stadium', 'Kingsmead','New Wanderers Stadium', 'Newlands', 'OUTsurance Oval','Sharjah Cricket Stadium', 'Sheikh Zayed Stadium',"St George's Park", 'SuperSport Park']

venue = 0
city = 0
if stadiums in except_stadiums:
    venue = 0
    city = 0
    neutral_venue = 1
else:
    venue = 1
    city = 1
    neutral_venue = 0



winner_toss = teams_dict[toss_winner]

toss_decision = 0
if bat_field == toss_choice[0]:
    toss_decision = 1
else:
    toss_decision = 0

eliminator = 0

if match_choice == match_type[0]:
    eliminator = 1
else:
    eliminator = 0

year = abs(2022 - year_input)


model = pickle.load(open('class_model.pkl','rb'))

if st.button('Predict'):
    result_margin = np.random.uniform(0.5,140.5)
    runs_wickets = np.random.randint(0,1)
    X_test = np.array([result_margin, city, venue, neutral_venue, toss_decision, runs_wickets, eliminator, teamA, teamB, winner_toss,year])
    scale = StandardScaler()
    X_test = X_test.reshape((1,-1))
    y_pred = model.predict(X_test)
    my_bar = st.progress(0)
    with st.spinner('Predicting'):
        time.sleep(2)
    probability = model.predict_proba(X_test)
    prob1 = (probability[0][y_pred][0])*100
    prob2 = 100 - prob1
    if prob1 > prob2:
        st.success('Winning Team is [ {} ] :::::: {}% '.format(team1,prob1))
        st.error('Losing Team is [ {} ] :::::: {}% '.format(team2,prob2))
    elif prob1 < prob2:
        st.success('Winning Team is [ {} ] :::::: {}%'.format(team2, prob2))
        st.error('Losing Team is [ {} ] :::::: {}%'.format(team1, prob1))
    else:
        st.success('Oh That is NEW! Both Team TIE !')