import time
import json
import os
import streamlit as st
from streamlit_cookies_manager import EncryptedCookieManager

cookies = EncryptedCookieManager(
    prefix="fintrace_",
    password="fintrace_secret_key_123"
)

if not cookies.ready():
    st.stop()

TOKEN_FILE = "tokens.json"

if not os.path.exists(TOKEN_FILE):
    with open(TOKEN_FILE, "w") as f:
        json.dump({}, f)


def create_login(username):
    token = f"{username}_{int(time.time())}"

    # store expiry (3 days)
    expiry = time.time() + (3 * 24 * 60 * 60)

    with open(TOKEN_FILE, "r") as f:
        data = json.load(f)

    data[token] = {
        "username": username,
        "expiry": expiry
    }

    with open(TOKEN_FILE, "w") as f:
        json.dump(data, f)

    cookies["auth_token"] = token
    cookies.save()


def check_login():
    token = cookies.get("auth_token")

    if not token:
        return None

    try:
        with open(TOKEN_FILE, "r") as f:
            data = json.load(f)

        if token not in data:
            return None

        user_data = data[token]

        if time.time() > user_data["expiry"]:
            return None

        return user_data["username"]

    except:
        return None


def logout():
    token = cookies.get("auth_token")

    if token:
        with open(TOKEN_FILE, "r") as f:
            data = json.load(f)

        if token in data:
            del data[token]

        with open(TOKEN_FILE, "w") as f:
            json.dump(data, f)

    cookies["auth_token"] = ""
    cookies.save()