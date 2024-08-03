import streamlit as st
import pickle
import pandas as pd
import base64

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style", unsafe_allow_html=True)
teams = [
    "Sunrisers Hyderabad",
    "Mumbai Indians",
    "Royal Challengers Bangalore",
    "Kolkata Knight Riders",
    "Chennai Super Kings",
    "Rajasthan Royals",
    "Delhi Capitals",
    "Gujarat Titans",
    "Punjab Kings",
    "Lucknow Super Giants",
]
cities = [
    "M Chinnaswamy Stadium, Bengaluru",
    "Punjab Cricket Association IS Bindra Stadium, Mohali",
    "Eden Gardens, Kolkata",
    "Wankhede Stadium, Mumbai",
    "Sawai Mansingh Stadium, Jaipur",
    "Rajiv Gandhi International Stadium, Uppal",
    "MA Chidambaram Stadium, Chepauk",
    "Dr DY Patil Sports Academy, Mumbai",
    "Newlands",
    "St George's Park",
    "Kingsmead",
    "SuperSport Park",
    "Buffalo Park",
    "New Wanderers Stadium",
    "De Beers Diamond Oval",
    "OUTsurance Oval",
    "Brabourne Stadium, Mumbai",
    "Barabati Stadium",
    "Vidarbha Cricket Association Stadium, Jamtha",
    "Himachal Pradesh Cricket Association Stadium, Dharamsala",
    "Dr. Y.S. Rajasekhara Reddy ACA-VDCA Cricket Stadium, Visakhapatnam",
    "Subrata Roy Sahara Stadium",
    "Shaheed Veer Narayan Singh International Stadium",
    "JSCA International Stadium Complex",
    "Zayed Cricket Stadium, Abu Dhabi",
    "Sharjah Cricket Stadium",
    "Dubai International Cricket Stadium",
    "Maharashtra Cricket Association Stadium, Pune",
    "Saurashtra Cricket Association Stadium",
    "Green Park",
    "Holkar Cricket Stadium",
    "Narendra Modi Stadium, AhmedabadArun Jaitley Stadium, Delhi",
    "Bharat Ratna Shri Atal Bihari Vajpayee Ekana Cricket Stadium, Lucknow",
    "Barsapara Cricket Stadium, Guwahati",
    "Maharaja Yadavindra Singh International Cricket Stadium, Mullanpur",
]


pipe = pickle.load(open("pipe.pkl", "rb"))
st.title("IPL Match Winning Prediction System")


col1, col2, col3 = st.columns(3)

with col1:
    batting_team = st.selectbox("Select the batting team", sorted(teams))
with col2:
    bowling_team = st.selectbox("Select the bowling team", sorted(teams))
with col3:
    Match_Date = st.date_input(
        "Match Date",
        value="default_value_today",
        min_value=None,
        max_value=None,
        key=None,
        help=None,
        on_change=None,
        args=None,
        kwargs=None,
        format="DD/MM/YYYY",
        disabled=False,
        label_visibility="visible",
    )

selected_city = st.selectbox("Select host city", sorted(cities))


target = st.number_input(
    "Target Score In Second Innings", min_value=0, max_value=300, value=0, step=1
)


col3, col4, col5 = st.columns(3)

with col3:
    score = st.number_input("Current Score", step=1)
with col4:
    wickets = st.number_input("Wickets Fall", step=1, max_value=10, min_value=0)

with col5:
    overs = st.number_input("Overs completed", step=1, max_value=20, min_value=0)

if st.button("Predict Probability"):
    runs_left = target - score
    balls_left = 120 - (overs * 6)
    wickets = 10 - wickets
    crr = score / overs
    rrr = (runs_left * 6) / balls_left if balls_left > 0 else 100

    input_df = pd.DataFrame(
        {
            "batting_team": [batting_team],
            "bowling_team": [bowling_team],
            "venue": [selected_city],
            "runs_left": [runs_left],
            "over": [overs],
            "balls_left": [balls_left],
            "wickets_left": [wickets],
            "target": [target],
            "crr": [crr],
            "rrr": [rrr],
        }
    )

    result = pipe.predict_proba(input_df)
    loss = result[0][0]
    win = result[0][1]
    if runs_left != 0 and (balls_left == 0 or wickets == 0):
        st.header(batting_team + "- " + " 0.0%")
        st.header(bowling_team + "- " + " 100.0%")
    else:
        st.header(batting_team + "- " + str(round((win * 100), 2)) + " %")
        st.header(bowling_team + "- " + str(round((loss * 100), 2)) + " %")
