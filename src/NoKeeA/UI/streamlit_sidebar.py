import streamlit as st
from NoKeeA.utils.wikipedia_api import get_wikipedia_summary
from NoKeeA.utils.file_operations import save_note, delete_note, \
    load_note, list_notes
from NoKeeA.utils.session_state import initialize_session_state
from NoKeeA.utils.file_import_export import import_file, export_file, \
    get_supported_extensions
import os


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
        st.session_state["loaded_note"] = new_note_name
        st.session_state["last_loaded_note"] = new_note_name

        # Save the empty note immediately
        try:
            save_note(new_note_name, "")
            st.sidebar.success(f"✅ Neue Notiz '{new_note_name}' erstellt.")
        except Exception as e:
            st.sidebar.error(f"❌ Fehler beim Erstellen der Notiz: {str(e)}")
            # Reset state if save failed
            st.session_state["note_name"] = ""
            st.session_state["loaded_note"] = ""
            st.session_state["last_loaded_note"] = None

    # Import/Export section
    st.sidebar.markdown("---")
    st.sidebar.subheader("📤 Import/Export")

    # Import file
    uploaded_file = st.sidebar.file_uploader(
        "📥 Datei importieren",
        type=get_supported_extensions(),
        key="file_uploader"
    )

    if uploaded_file is not None:
        try:
            # Save uploaded file temporarily
            with open(uploaded_file.name, "wb") as f:
                f.write(uploaded_file.getvalue())

            # Import the file
            result = import_file(uploaded_file.name)
            if result:
                # Ask user how to import
                import_option = st.sidebar.radio(
                    "Import-Option",
                    ["Als neue Notiz", "In aktuelle Notiz einfügen"],
                    key="import_option"
                )

                if import_option == "Als neue Notiz":
                    st.session_state["editor_content"] = result["content"]
                    st.session_state["note_name"] = result["name"]
                    st.session_state["loaded_note"] = ""
                    st.session_state["last_loaded_note"] = None
                    st.sidebar.success(
                        f"✅ Datei '{uploaded_file.name}' importiert.")
                else:
                    # Append to current content with a separator
                    current_content = st.session_state.get(
                        "editor_content", "")
                    separator = "\n\n---\n\n" if current_content else ""
                    st.session_state["editor_content"] = current_content + \
                        separator + result["content"]
                    st.sidebar.success(
                        f"✅ Datei '{uploaded_file.name}' importiert."
                    )
            else:
                st.sidebar.error(
                    f"❌ Fehler beim Importieren von '{uploaded_file.name}'.")

            # Clean up temporary file
            os.remove(uploaded_file.name)
        except Exception as e:
            st.sidebar.error(f"❌ Fehler beim Importieren: {str(e)}")

    # Export file
    if st.session_state.get("editor_content"):
        export_format = st.sidebar.selectbox(
            "📤 Export-Format",
            get_supported_extensions(),
            format_func=lambda x: x[1:].upper()  # Remove dot and capitalize
        )

        # Create export filename
        export_name = f"{st.session_state['note_name']}{export_format}"

        # Get content for export
        export_content = export_file(
            st.session_state["editor_content"], export_name)

        if export_content is not None:
            # Create download button with correct MIME type
            mime_type = {
                ".txt": "text/plain",
                ".md": "text/markdown",
                ".pdf": "application/pdf"
            }.get(export_format, "text/plain")

            st.sidebar.download_button(
                label="📥 Exportieren",
                data=export_content,
                file_name=export_name,
                mime=mime_type
            )
        else:
            st.sidebar.error("❌ Fehler beim Vorbereiten des Exports.")
        
    # Wikipedia Lookup Section
    st.sidebar.markdown("---")
    st.sidebar.subheader("📚 Wikipedia-Suche")

    wiki_term = st.sidebar.text_input("🔍 Begriff eingeben")

    if st.sidebar.button("🔎 Nachschlagen"):
        if wiki_term:
            result = get_wikipedia_summary(wiki_term)
            if "summary" in result:
                st.sidebar.success(result["summary"])
                st.sidebar.markdown(f"[🔗 Zum Artikel]({result['url']})", unsafe_allow_html=True)
            else:
                st.sidebar.error(result["error"])
        else:
            st.sidebar.info("Bitte gib einen Begriff ein.")

    else:
        st.sidebar.info("ℹ️ Keine Notiz zum Exportieren vorhanden.")
