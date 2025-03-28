import pytest
from unittest.mock import patch, MagicMock, call
import streamlit as st

# Angenommen video2text kommt aus deiner App
from NoKeeA.UI.streamlit_content import video2text


@pytest.fixture
def mock_session_state():
    state = {
        "show_video2text_uploader": True,
        "video2text_file_content": MagicMock(name="UploadedFile"),
        "video2text_progress_bar_text": "Frames werden extrahiert.",
    }
    with patch.dict(st.session_state, state, clear=True):
        yield


def fake_video2text_generator(_file):
    # Simuliert die Rückgabe von Fortschritt und Erfolgsmeldungen
    yield "✅ Datei gespeichert"
    yield "✅ Audio extrahiert"
    yield "✅ Audio zu Text konvertiert"
    yield 1.0
    yield "✅ 41/125 Frames extrahiert"
    st.session_state["video2text_progress_bar_text"] = "Texte werden extrahiert."
    yield 1.0
    yield "✅ Text aus Frames extrahiert"
    yield "✅ Bilderkennung geladen"
    st.session_state["video2text_progress_bar_text"] = "Frames werden beschreiben. Das kann einige Zeit dauern."
    yield 1.0
    yield "✅ Frames beschrieben"
    return "summary"


@patch("NoKeeA.AI.video2text.video2text", side_effect=fake_video2text_generator)
@patch("streamlit.write")
@patch("streamlit.success")
@patch("streamlit.status")
@patch("streamlit.progress")
@patch("streamlit.file_uploader")
@patch("streamlit.button")
def test_video2text_workflow(mock_button, mock_file_uploader, mock_progress, mock_status, mock_success,
                             mock_write, mock_v2t, mock_session_state):
    # Reihenfolge: [🎞️ Video2Text, 📝 Convert]
    mock_button.side_effect = [False, True]
    mock_file_uploader.return_value = MagicMock(name="UploadedFile")

    mock_status_ctx = MagicMock()
    mock_status.return_value.__enter__.return_value = mock_status_ctx
    mock_progress_obj = MagicMock()
    mock_progress.return_value = mock_progress_obj

    video2text()

    expected_success_calls = [
        call("✅ Datei gespeichert"),
        call("✅ Audio extrahiert"),
        call("✅ Audio zu Text konvertiert"),
        call("✅ 41/125 Frames extrahiert"),
        call("✅ Text aus Frames extrahiert"),
        call("✅ Bilderkennung geladen"),
        call("✅ Frames beschrieben"),
        call("✅ Video zusammengefasst und Text eingefügt"),
    ]

    progress_calls = [
        call(1.0, "Frames werden extrahiert. ~ 100.00%"),
        call(1.0, "Texte werden extrahiert. ~ 100.00%"),
        call(1.0, "Frames werden beschreiben. Das kann einige Zeit dauern. ~ 100.00%"),
    ]

    # Die summary wird als write ausgegeben
    mock_write.assert_any_call("summary")
    mock_success.assert_has_calls(expected_success_calls, any_order=False)
    mock_progress_obj.progress.assert_has_calls(
        progress_calls, any_order=False)
    mock_status_ctx.update.assert_called_once_with(
        label="Video zusammengefasst!",
        state="complete",
        expanded=False,
    )
