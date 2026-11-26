import streamlit as st

st.set_page_config(
    page_title="Cricket Live",
    page_icon="🏏",
    layout="wide"
)

st.title("🏏 Cricket Live")
st.subheader("Your home for live cricket")

st.markdown("""
Welcome to Cricket Live!

Find live cricket matches, leagues, scores
and legally available free streaming links.
""")

st.divider()

st.header("🏆 Cricket Leagues")

leagues = [
    "Women's Big Bash League (WBBL)",
    "Big Bash League (BBL)",
    "Indian Premier League (IPL)",
    "Pakistan Super League (PSL)",
    "Caribbean Premier League (CPL)",
    "The Hundred",
    "International Cricket"
]

selected_league = st.selectbox(
    "Select a league",
    leagues
)

st.write("Selected league:", selected_league)

st.divider()

st.header("📺 Live Match Centre")

st.info("Match listings will be added in our next steps.")

st.header("🎥 Watch Cricket")

st.info("Authorised free streaming sources will appear here.")

st.divider()

st.caption("Cricket Live | Cricket streaming and match hub")
