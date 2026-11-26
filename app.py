import streamlit as st

st.set_page_config(
    page_title="Cricket Live",
    page_icon="🏏",
    layout="wide"
)

# --------------------------
# APP HEADER
# --------------------------

st.title("🏏 CRICKET LIVE")
st.caption("Your cricket streaming and match centre")

st.markdown("""
Watch cricket, explore leagues, follow matches
and find officially available streaming sources.
""")

st.divider()

# --------------------------
# LEAGUES
# --------------------------

leagues = [
    "All Leagues",
    "Women's Big Bash League (WBBL)",
    "Big Bash League (BBL)",
    "Indian Premier League (IPL)",
    "Pakistan Super League (PSL)",
    "Caribbean Premier League (CPL)",
    "The Hundred",
    "International Cricket",
]

selected_league = st.selectbox(
    "🏆 Choose a league",
    leagues
)

# --------------------------
# DEMO MATCHES
# --------------------------

matches = [
    {
        "league": "Women's Big Bash League (WBBL)",
        "team1": "Hobart Hurricanes Women",
        "team2": "Adelaide Strikers Women",
        "status": "Demo match",
        "source": ""
    },
    {
        "league": "Big Bash League (BBL)",
        "team1": "Sydney Sixers",
        "team2": "Melbourne Stars",
        "status": "Demo match",
        "source": ""
    },
    {
        "league": "Indian Premier League (IPL)",
        "team1": "Mumbai Indians",
        "team2": "Chennai Super Kings",
        "status": "Demo match",
        "source": ""
    },
]

if selected_league == "All Leagues":
    filtered_matches = matches
else:
    filtered_matches = [
        m for m in matches
        if m["league"] == selected_league
    ]

# --------------------------
# MATCH CENTRE
# --------------------------

st.header("📺 Match Centre")

if filtered_matches:

    for match in filtered_matches:

        with st.container(border=True):

            st.subheader(
                f"{match['team1']} vs {match['team2']}"
            )

            st.caption(match["league"])

            st.info(match["status"])

            st.write(
                "Streaming availability depends on "
                "the match and your region."
            )

            st.link_button(
                "🌐 Find Official Streaming",
                "https://www.icc-cricket.com/"
            )

else:
    st.info("No matches found for this league.")

# --------------------------
# WATCH SECTION
# --------------------------

st.divider()

st.header("🎥 Watch Cricket")

st.markdown("""
Find authorised free streaming options through
official broadcasters and cricket organisations.
""")

st.link_button(
    "🌐 ICC Official Website",
    "https://www.icc-cricket.com/"
)

st.link_button(
    "▶ Official ICC YouTube",
    "https://www.youtube.com/@ICC"
)

# --------------------------
# FOOTER
# --------------------------

st.divider()

st.caption(
    "Cricket Live | Find cricket matches and authorised streams"
)
