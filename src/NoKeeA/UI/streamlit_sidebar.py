import streamlit as st
from NoKeeA.utils.file_operations import save_note, delete_note, \
    load_note, list_notes
from NoKeeA.utils.session_state import initialize_session_state


def render_sidebar():
    """Render the sidebar with controls"""
    initialize_session_state()

    st.sidebar.title("⚙️ Einstellungen")

    # Get list of available notes
    available_notes = list_notes()

    # Ensure there's at least one note
    if not available_notes:
        available_notes = ["Neue Notiz"]

    selected_note = st.sidebar.selectbox(
        "📝 Notiz laden",
        available_notes,
        index=0,
        key="note_selector"
    )

    # Load the note if a new one is selected
    if selected_note and selected_note \
            != st.session_state.get("last_loaded_note"):
        try:
            note_data = load_note(selected_note)
            st.session_state["editor_content"] = note_data["content"]
            st.session_state["loaded_note"] = note_data["name"]
            st.session_state["note_name"] = note_data["name"]
            st.session_state["last_loaded_note"] = selected_note
            st.sidebar.success(f"✅ Notiz '{selected_note}' geladen.")
        except Exception as e:
            st.sidebar.error(f"❌ Fehler beim Laden: {str(e)}")

    # Note name input
    st.session_state["note_name"] = st.sidebar.text_input(
        "🔤 Notizname",
        st.session_state["loaded_note"] if
        st.session_state["loaded_note"] != "" else "Neue Notiz"
    )

    # Save button
    if st.sidebar.button("💾 Speichern"):
        if st.session_state["note_name"]:
            try:
                save_note(
                    st.session_state["note_name"],
                    st.session_state.get("editor_content", "")
                )
                st.session_state["loaded_note"] = st.session_state["note_name"]
                st.sidebar.success(
                    f"✅ Notiz '{st.session_state['note_name']}' gespeichert.")
            except Exception as e:
                st.sidebar.error(f"❌ Fehler beim Speichern: {str(e)}")
        else:
            st.sidebar.error("❌ Bitte gib einen Notiznamen ein.")

    # Delete button
    if st.sidebar.button("🗑 Notiz löschen"):
        if st.session_state["loaded_note"]:
            if delete_note(st.session_state["loaded_note"]):
                st.sidebar.success(
                    f"✅ Notiz '{st.session_state['loaded_note']}' gelöscht.")
                # Reset all relevant session state variables
                st.session_state["editor_content"] = ""
                st.session_state["loaded_note"] = ""
                st.session_state["note_name"] = ""
                st.session_state["last_loaded_note"] = None
            else:
                st.sidebar.error("❌ Notiz konnte nicht gelöscht werden.")
        else:
            st.sidebar.error("❌ Keine Notiz zum Löschen ausgewählt.")

    # New note button
    if st.sidebar.button("📝 Neue Notiz"):
        new_note_name = f"Neue Notiz{len(available_notes) + 1}"
        st.session_state["note_name"] = new_note_name
        st.session_state["editor_content"] = ""
        st.session_state["loaded_note"] = ""
        st.session_state["last_loaded_note"] = None
