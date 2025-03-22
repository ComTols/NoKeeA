import streamlit as st
from NoKeeA.utils.file_operations import save_note, delete_note, \
    load_note, list_notes
from NoKeeA.utils.session_state import initialize_session_state


def site_bar_note_name():
    """Zeigt das Eingabefeld für den Notiznamen und den Speichern-Button an."""
    # Ensure session state is initialized
    initialize_session_state()

    st.session_state["note_name"] = st.sidebar.text_input(
        "🔤 Notizname",
        st.session_state["loaded_note"] if st.session_state["loaded_note"]
        != "" else "Neue Notiz"
    )

    if st.sidebar.button("💾 Speichern"):
        if st.session_state["note_name"]:
            try:
                save_note(
                    st.session_state["note_name"],
                    # Sicherer Zugriff
                    st.session_state.get("editor_content", "")
                )
                st.session_state["loaded_note"] = st.session_state["note_name"]
                st.sidebar.success(
                    f"✅ Notiz '{st.session_state['note_name']}' gespeichert.")
            except Exception as e:
                st.sidebar.error(f"❌ Fehler beim Speichern: {str(e)}")
        else:
            st.sidebar.error("❌ Bitte gib einen Notiznamen ein.")


def site_bar_delete():
    """Zeigt den Löschen-Button an."""
    # Ensure session state is initialized
    initialize_session_state()

    if st.sidebar.button("🗑 Notiz löschen"):
        if st.session_state["loaded_note"]:
            if delete_note(st.session_state["loaded_note"]):
                st.sidebar.success(
                    f"✅ Notiz '{st.session_state['loaded_note']}' gelöscht.")
                # Zurücksetzen aller relevanten Session-State-Variablen
                st.session_state["editor_content"] = ""
                st.session_state["loaded_note"] = ""
                st.session_state["note_name"] = ""
                st.session_state["last_loaded_note"] = None
            else:
                st.sidebar.error("❌ Notiz konnte nicht gelöscht werden.")
        else:
            st.sidebar.error("❌ Keine Notiz zum Löschen ausgewählt.")


def site_bar_load_note():
    """Zeigt die Liste der verfügbaren Notizen zum Laden an."""
    # Ensure session state is initialized
    initialize_session_state()

    notes = list_notes()
    if notes:
        selected_note = st.sidebar.selectbox(
            "📝 Notiz laden",
            [""] + notes,
            index=0,
            key="note_selector"
        )

        # Lade die Notiz automatisch, wenn eine neue ausgewählt wurde
        if selected_note and selected_note != st.session_state.get(
            "last_loaded_note"
        ):
            try:
                note_data = load_note(selected_note)
                st.session_state["editor_content"] = note_data["content"]
                st.session_state["loaded_note"] = note_data["name"]
                st.session_state["note_name"] = note_data["name"]
                st.session_state["last_loaded_note"] = selected_note
                st.sidebar.success(f"✅ Notiz '{selected_note}' geladen.")
            except Exception as e:
                st.sidebar.error(f"❌ Fehler beim Laden: {str(e)}")


def render_sidebar():
    """Rendert die gesamte Sidebar."""
    # Ensure session state is initialized
    initialize_session_state()

    st.sidebar.title("📝 Notiz-Verwaltung")

    site_bar_note_name()
    st.sidebar.markdown("---")
    site_bar_load_note()
    st.sidebar.markdown("---")
    site_bar_delete()
