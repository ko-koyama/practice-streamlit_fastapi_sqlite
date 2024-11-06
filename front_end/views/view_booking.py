import requests
import datetime

import streamlit as st
import pandas as pd


def view_bookings(ROOT_ENDPOINT):
    # ページ描画に必要なデータ処理（別ファイルに定義すべきか要件等）

    # ユーザ一覧取得
    url_users = f"{ROOT_ENDPOINT}/users"
    res = requests.get(url_users)
    users = res.json()

    # ユーザIDをキーにした辞書
    users_id = {}
    for user in users:
        users_id[user["user_id"]] = user["user_name"]
    # ユーザ名をキーにした辞書
    users_name = {}
    for user in users:
        users_name[user["user_name"]] = user["user_id"]

    # 会議室一覧取得
    url_rooms = f"{ROOT_ENDPOINT}/rooms"
    res = requests.get(url_rooms)
    rooms = res.json()

    # 会議室一覧のDataFrame
    df_rooms = pd.DataFrame(rooms)
    df_rooms_selected = df_rooms[["room_name", "capacity"]]
    df_rooms_selected.columns = ["会議室名", "定員"]

    # 会議室IDをキーにした辞書
    rooms_id = {}
    for room in rooms:
        rooms_id[room["room_id"]] = {
            "room_name": room["room_name"],
            "capacity": room["capacity"],
        }
    # 会議室名をキーにした辞書
    rooms_name = {}
    for room in rooms:
        rooms_name[room["room_name"]] = {
            "room_id": room["room_id"],
            "capacity": room["capacity"],
        }

    # 予約一覧取得
    url_bookings = f"{ROOT_ENDPOINT}/bookings"
    res = requests.get(url_bookings)
    bookings = res.json()

    # 予約一覧のDataFrame
    df_bookings = pd.DataFrame(bookings)
    df_bookings["user_name"] = df_bookings["user_id"].apply(lambda x: users_id[x])
    df_bookings["room_name"] = df_bookings["room_id"].apply(
        lambda x: rooms_id[x]["room_name"]
    )
    df_bookings["start_datetime"] = df_bookings["start_datetime"].apply(
        lambda x: datetime.datetime.fromisoformat(x).strftime("%Y/%m/%d %H:%M")
    )
    df_bookings["end_datetime"] = df_bookings["end_datetime"].apply(
        lambda x: datetime.datetime.fromisoformat(x).strftime("%Y/%m/%d %H:%M")
    )
    df_bookings_selected = df_bookings[
        ["user_name", "room_name", "booked_num", "start_datetime", "end_datetime"]
    ]
    df_bookings_selected.columns = [
        "予約者名",
        "会議室名",
        "利用人数",
        "開始日時",
        "終了日時",
    ]

    # ページ描画
    st.write("## 会議室予約画面")

    st.write("### 会議室一覧")
    st.table(df_rooms_selected)

    st.write("### 予約一覧")
    st.table(df_bookings_selected)

    # 入力フォーム
    with st.form(key="booking"):
        user_name = st.selectbox("予約者名", users_name.keys())
        room_name = st.selectbox("会議室名", rooms_name.keys())
        booked_num = st.number_input("予約人数", step=1, min_value=1)
        date = st.date_input("予約日付", min_value=datetime.date.today())
        start_time = st.time_input("開始時刻", value=datetime.time(hour=9, minute=0))
        end_time = st.time_input("終了時刻", value=datetime.time(hour=20, minute=0))

        submit_button = st.form_submit_button(label="リクエスト送信")

    # 予約登録APIの呼び出し
    if submit_button:

        # 登録データの作成
        user_id = users_name[user_name]
        room_id = rooms_name[room_name]["room_id"]
        capacity = rooms_name[room_name]["capacity"]
        data = {
            "user_id": user_id,
            "room_id": room_id,
            "booked_num": booked_num,
            "start_datetime": datetime.datetime(
                year=date.year,
                month=date.month,
                day=date.day,
                hour=start_time.hour,
                minute=start_time.minute,
            ).isoformat(),
            "end_datetime": datetime.datetime(
                year=date.year,
                month=date.month,
                day=date.day,
                hour=end_time.hour,
                minute=end_time.minute,
            ).isoformat(),
        }

        # 定員以下の場合、APIの呼び出し
        if booked_num <= capacity:
            url = f"{ROOT_ENDPOINT}/bookings"
            res = requests.post(url, json=data)
            if res.status_code == 200:
                st.success("予約完了")
            else:
                st.error("予約失敗")

        # 定員超過の場合、APIの呼び出しを棄却
        else:
            st.error("定員超過のため予約不可")
