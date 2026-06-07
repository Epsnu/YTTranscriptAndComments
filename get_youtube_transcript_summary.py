from utils import ensure_transcript
from utils import ensure_transcript_summary
from datetime import date
import streamlit as st

def get_transcript_summary(transcript, transcript_summary, video_id):
    transcript = ensure_transcript(transcript, video_id)

    transcript_summary = ensure_transcript_summary(transcript, transcript_summary)

    save_summary(transcript_summary)

    print_summary(transcript_summary)

    return transcript, transcript_summary

def print_summary(summary):
    st.write(summary)

def save_summary(summary):
    today = date.today()
    outFile = f"transcript_summary_{today}.md"
    st.download_button(
        "Download Summary",
        data=summary,
        file_name=outFile,
        key="download-transcript-summary"
    )