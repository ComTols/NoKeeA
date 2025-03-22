import streamlit as st
from streamlit_quill import st_quill


def content():
    st.subheader("📝 Notiz bearbeiten")
    st_quill(
        value=st.session_state.get("editor_content", ""),
        html=True,
        toolbar=[
            ["bold", "italic", "underline", "strike"],  # Text style
            ["blockquote", "code-block"],  # Blocks
            [{"header": 1}, {"header": 2}],  # Custom button values
            [{"list": "ordered"}, {"list": "bullet"}],  # Lists
            [{"script": "sub"}, {"script": "super"}],  # Superscript/Subscript
            [{"indent": "-1"}, {"indent": "+1"}],  # Indent
            [{"direction": "rtl"}],  # Text direction
            [{"size": ["small", False, "large", "huge"]}],  # Custom dropdown
            [{"header": [1, 2, 3, 4, 5, 6, False]}],  # Header dropdown
            [{"color": []}, {"background": []}],  # Dropdown with defaults
            [{"align": []}],  # Text align
            [{"font": [
                "sans-serif", "serif", "monospace", "Arial",
                "Courier New", "Georgia", "Times New Roman", "Verdana"
            ]}],  # Font family
            ["link", "image", "video", "formula"],  # Media
            ["clean"]  # Remove formatting
        ],
        # key=f"editor_{selected_note}"
    )
