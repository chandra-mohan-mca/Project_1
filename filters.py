import streamlit as st
import pymysql
import pandas as pd


st.markdown(
    "<div style='text-align: center; color: #DC143C; font-size: 35px;'>Interactive Filtering Functionality</div>",
    unsafe_allow_html=True,
)
st.markdown(
    """<hr style="height:2px;border:none;color:#DC143C;background-color:#DC143C;" />""",
    unsafe_allow_html=True,
)


def get_data_from_mysql():
    connection = pymysql.connect(
        host="localhost",
        user="root",
        password="Chandru$04",
        database="day_1"
    )
    query = "select Movie_Name, Ratings, Voting_Counts, Durations, Genre FROM imdb"
    data = pd.read_sql(query, connection)
    connection.close()
    return data

#load data
data = get_data_from_mysql()

duration_option = st.selectbox( "Durations", options=["Select Duration","< 120 Minus", "120–180 Minus", "> 180 Minus"],index=0,)

if duration_option == "< 120 Minus":
    duration_filter = (data["Durations"] < 120)
elif duration_option == "120–180 Minus":
    duration_filter = (data["Durations"] >= 120) & (data["Durations"] <= 180)
else:
    duration_filter = (data["Durations"] > 180)

#ratings filter
rating_filter = st.slider("Ratings", min_value=0.0, max_value=10.0, value=8.0, step=0.1)

# Votes filter
votes_filter = st.number_input("Voting_Counts", min_value=0, value=10000, step=1000)

# Genre filter
available_genres = list(set(genre for genres in data["Genre"] for genre in genres.split(", ")))
selected_genres = st.multiselect("Select Genres", available_genres, default=[])

# Apply filters
filtered_data = data[
    duration_filter & 
    (data["Ratings"] >= rating_filter) &
    (data["Voting_Counts"] >= votes_filter)
]

if selected_genres:
    filtered_data = filtered_data[
        filtered_data["Genre"].apply(lambda g: any(genre in g for genre in selected_genres))
    ]


agree = st.checkbox("I agree")
if agree:
    st.write("Great!")
# Display table format
    if st.button('Click Results',key='filter_button_1'):
        if not filtered_data.empty:
            st.success('Filtered Results....🎥',icon="✅")
            st.dataframe(filtered_data) 
            st.balloons()
        else:
            st.warning("No movies match the selected criteria.",icon="⚠️")

