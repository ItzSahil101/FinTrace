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

    expiry = time.time() + (3 * 24 * 60 * 60)

    try:
        with open(TOKEN_FILE, "r") as f:
            data = json.load(f)
    except:
        data = {}

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

    st.write("DEBUG TOKEN =", token)

    if not token:
        return None

    try:

        with open(TOKEN_FILE, "r") as f:
            data = json.load(f)

        if token not in data:
            return None

        user = data[token]

        if time.time() > user["expiry"]:

            del data[token]

            with open(TOKEN_FILE, "w") as f:
                json.dump(data, f)

            return None

        return user["username"]

    except:
        return None


def logout():

    token = cookies.get("auth_token")

    try:

        with open(TOKEN_FILE, "r") as f:
            data = json.load(f)

        if token in data:
            del data[token]

        with open(TOKEN_FILE, "w") as f:
            json.dump(data, f)

    except:
        pass

    try:
        del cookies["auth_token"]
    except:
        pass

    cookies.save()