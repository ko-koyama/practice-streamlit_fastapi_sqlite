import requests

import streamlit as st


def view_rooms(ROOT_ENDPOINT):
    st.write("## 会議室登録画面")

    # 入力フォーム
    with st.form(key="room"):
        room_name = st.text_input("会議室名", max_chars=12)
        capacity = st.number_input("定員", step=1, min_value=1)
        submit_button = st.form_submit_button(label="会議室登録")

    # 会議室登録APIの呼び出し
    if submit_button:

        # 登録データの作成
        data = {"room_name": room_name, "capacity": capacity}

        # APIの呼び出し
        url = f"{ROOT_ENDPOINT}/rooms"
        res = requests.post(url, json=data)
        if res.status_code == 200:
            st.success("会議室登録完了")
        else:
            st.error("会議室登録失敗")
