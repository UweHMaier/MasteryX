import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import streamlit as st
import traceback


def connect_to_google_sheet(sheet_id: str, worksheet_name: str):
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    creds_dict = st.secrets["gcp_service_account"]

    for attempt in range(3):
        try:
            creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
            client = gspread.authorize(creds)
            sheet = client.open_by_key(sheet_id).worksheet(worksheet_name)
            return sheet
        except Exception as e:
            st.warning(f"Verbindungsversuch {attempt + 1}/3 fehlgeschlagen:")
            st.text(f"{type(e).__name__}: {e}")
            st.text(traceback.format_exc())
            time.sleep(2)

    st.error("❌ Verbindung nach mehreren Versuchen fehlgeschlagen.")
    st.stop()



# Speichern
def save_to_sheet(sheet, answer):
    data = [
        st.session_state["session_id"],
        answer,        
    ]
    try:
        sheet.append_row(data, value_input_option="RAW")
        row_number = len(sheet.get_all_values())
        return row_number
    except ConnectionError as e:
        st.error("Verbindung zum Google Sheet fehlgeschlagen. Bitte überprüfe die Internetverbindung.")
        st.stop()
    except Exception as e:
        st.error("❌ Fehler beim Speichern in Google Sheets.")
        st.exception(e)
        st.stop()
