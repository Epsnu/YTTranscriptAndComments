from utils import ensure_transcript
from datetime import date
import streamlit as st

def get_transcript(transcript, video_id):
    transcript = ensure_transcript(transcript, video_id)

    save_transcript(transcript)

    print_transcript(transcript)

    return transcript

def print_transcript(transcript):
    st.write(transcript)

def save_transcript(transcript):
    today = date.today()
    outFile = f"transcript_{today}.txt"
    st.download_button(
        "Download Transcript",
        data=transcript,
        file_name=outFile,
        key="download-transcript"
    )