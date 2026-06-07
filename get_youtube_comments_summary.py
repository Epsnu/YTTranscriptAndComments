from utils import ensure_comments
from utils import ensure_comments_summary
from datetime import date
import streamlit as st

def get_comments_summary(comments, comments_summary, video_id):
    comments = ensure_comments(comments, video_id)

    comments_summary = ensure_comments_summary(comments, comments_summary)

    save_summary(comments_summary)

    print_summary(comments_summary)

    return comments, comments_summary

def print_summary(summary):
    st.write(summary)

def save_summary(summary):
    today = date.today()
    outFile = f"comments_summary_{today}.md"
    st.download_button(
        "Download Comments Summary",
        data=summary,
        file_name=outFile,
        key="download-comments-summary"
    )