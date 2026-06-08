import gspread
import streamlit as st
from datetime import datetime


def get_sheet():
    creds = st.secrets["gcp_service_account"]
    gc = gspread.service_account_from_dict(creds)
    sheet = gc.open_by_key(st.secrets["sheets"]["sheet_id"]).sheet1
    return sheet


def submit_feedback(message):
    sheet = get_sheet()
    dt = datetime.now()
    row = [dt.strftime("%m/%d/%y"), message]
    sheet.append_row(row)

def get_feedback():
    sheet = get_sheet()
    rows =  sheet.get_all_records()
    rows.sort(key=lambda r: r["timestamp"], reverse=True)
    return rows
