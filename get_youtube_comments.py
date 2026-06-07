from utils import ensure_comments
from utils import comments_string
from datetime import date
import streamlit as st

def get_comments(comments, video_id):
    comments = ensure_comments(comments, video_id)

    save_comments(comments)

    print_comments(comments)

    return comments

def print_comments(comments):
    for comment in comments:
        st.divider()
        st.write(comment["text"].strip())
    st.divider()

def save_comments(comments):
    today = date.today()
    outFile = f"comments_{today}.txt"
    st.download_button(
        "Download Comments",
        data=comments_string(comments),
        file_name=outFile,
        key="download-comments"
    )