import requests

import streamlit as st


def view_users(ROOT_ENDPOINT):
    st.write("## ユーザ登録画面")

    # 入力フォーム
    with st.form(key="user"):
        user_name = st.text_input("ユーザ名", max_chars=12)
        submit_button = st.form_submit_button(label="ユーザ登録")

    # ユーザ登録APIの呼び出し
    if submit_button:

        # 登録データの作成
        data = {"user_name": user_name}

        # APIの呼び出し
        url = f"{ROOT_ENDPOINT}/users"
        res = requests.post(url, json=data)
        if res.status_code == 200:
            st.success("ユーザ登録完了")
        else:
            st.error("ユーザ登録失敗")
