import streamlit as st
import requests

st.set_page_config(
    page_title="Cricket Live",
    page_icon="🏏",
    layout="wide"
)

# API connection
@st.cache_data(ttl=60)
def fetch_matches():
    api_key = st.secrets["CRICKET_API_KEY"]

    url = "https://api.cricapi.com/v1/currentMatches"

    params = {
        "apikey": api_key,
        "offset": 0
    }

    response = requests.get(url, params=params, timeout=20)
    response.raise_for_status()

    result = response.json()

    if result.get("status") != "success":
        raise Exception(result.get("message", "API request failed"))

    return result.get("data", [])


# Header
st.title("🏏 CRICKET LIVE")
st.caption("Your cricket streaming and match centre")

st.markdown("""
Follow cricket matches, check live scores and explore
official streaming options.
""")

st.divider()

# Navigation
page = st.sidebar.radio(
    "Navigation",
    ["Home", "Live Matches", "Upcoming Matches", "All Matches"]
)

# League filters
leagues = [
    "All Leagues",
    "Women's Big Bash League (WBBL)",
    "Big Bash League (BBL)",
    "Indian Premier League (IPL)",
    "Pakistan Super League (PSL)",
    "Caribbean Premier League (CPL)",
    "The Hundred",
    "International Cricket"
]

selected_league = st.sidebar.selectbox(
    "Choose a league",
    leagues
)

# Refresh button
if st.sidebar.button("🔄 Refresh Matches"):
    st.cache_data.clear()

# Load matches
try:
    matches = fetch_matches()

except Exception as e:
    st.error("Unable to load match data.")
    st.caption(str(e))
    st.stop()


# Match filtering
@st.cache_data(ttl=60)
def fetch_scorecard(match_id):
    api_key = st.secrets["CRICKET_API_KEY"]

    url = "https://api.cricapi.com/v1/match_scorecard"

    params = {
        "apikey": api_key,
        "id": match_id
    }

    response = requests.get(url, params=params, timeout=20)
    response.raise_for_status()

    result = response.json()

    if result.get("status") != "success":
        raise Exception(result.get("message", "Scorecard request failed"))

    return result.get("data", {})


def is_live(match):
    return (
        match.get("matchStarted") is True
        and match.get("matchEnded") is not True
    )

def show_match(match):
    teams = match.get("teams", [])
    scores = match.get("score", [])

    match_title = " 🏏 vs ".join(teams) if teams else "Cricket Match"

    with st.expander(match_title, expanded=False):

        if scores:
            for score in scores:
                st.write(
                    f"**{score.get('inning', '')}** "
                    f"{score.get('r', '')}/{score.get('w', '')} "
                    f"({score.get('o', '')} overs)"
                )

        st.write("📍", match.get("venue", "Venue unavailable"))
        st.write("📅", match.get("date", "Date unavailable"))
        st.write("📢", match.get("status", "Status unavailable"))

        match_id = match.get("id")

        if match_id:
            if st.button("📊 Fetch Detailed Scorecard", key=f"score_{match_id}"):
                try:
                    scorecard = fetch_scorecard(match_id)
                    st.subheader("📊 Detailed Scorecard")
                    st.json(scorecard)

                except Exception as e:
                    st.error("Scorecard could not be loaded.")
                    st.caption(str(e))

        st.markdown(
            "[Find official streaming options](https://www.google.com/search?q=official+live+cricket+streaming)"
        )


# HOME
if page == "Home":

    st.subheader("🏠 Home")

    st.write("Welcome to Cricket Live.")

    st.write(f"Matches available in the feed: **{len(matches)}**")

    live_matches = [m for m in matches if is_live(m)]

    st.metric("Live Matches", len(live_matches))

    for match in live_matches:
        show_match(match)


# LIVE MATCHES
elif page == "Live Matches":

    st.subheader("🔴 Live Matches")

    live_matches = [m for m in matches if is_live(m)]

    if not live_matches:
        st.info("No live matches found right now.")

    else:
        for match in live_matches:
            show_match(match)


# ALL MATCHES
elif page == "Upcoming Matches":
    upcoming_matches = [
        match for match in matches
        if is_upcoming(match)
    ]

    st.subheader("📅 Upcoming Cricket Matches")

    if upcoming_matches:
        for match in upcoming_matches:
            show_match(match)
    else:
        st.info("No upcoming matches available right now.")
elif page == "All Matches":

    st.subheader("🏏 All Matches")

    search_text = st.text_input(
        "🔍 Search matches or teams",
        placeholder="Type a team name, league or venue..."
    )

    if selected_league == "All Leagues":
        filtered_matches = matches
    else:
        league_keyword = selected_league.split("(")[0].strip().lower()

        filtered_matches = [
            m for m in matches
            if league_keyword in str(m.get("name", "")).lower()
            or league_keyword in str(m.get("teams", "")).lower()
        ]

    if search_text:
        filtered_matches = [
            m for m in filtered_matches
            if search_text.lower() in str(m.get("name", "")).lower()
            or search_text.lower() in str(m.get("teams", "")).lower()
            or search_text.lower() in str(m.get("venue", "")).lower()
            or search_text.lower() in str(m.get("status", "")).lower()
        ]

    st.write(f"Matches found: {len(filtered_matches)}")

    if not filtered_matches:
        st.info("No matches found.")

    else:
        for match in filtered_matches:
            show_match(match)

st.divider()

st.caption(
    "Cricket Live | Match data provided through CricketData API"
)
