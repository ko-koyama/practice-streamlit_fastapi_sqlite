import streamlit as st

from views.view_users import view_users
from views.view_rooms import view_rooms
from views.view_booking import view_bookings

ROOT_ENDPOINT = "http://127.0.0.1:8000"

st.title("会議室予約アプリ")

page = st.sidebar.selectbox("Choose your page", ["users", "rooms", "bookings"])

if page == "users":
    view_users(ROOT_ENDPOINT)

elif page == "rooms":
    view_rooms(ROOT_ENDPOINT)

elif page == "bookings":
    view_bookings(ROOT_ENDPOINT)
