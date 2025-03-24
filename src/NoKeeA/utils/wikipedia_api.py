import wikipedia

# Sprache auf Deutsch setzen
wikipedia.set_lang("de")

def get_wikipedia_summary(term: str, sentences: int = 3) -> dict:
    try:
        summary = wikipedia.summary(term, sentences=sentences)
        page = wikipedia.page(term)
        return {
            "summary": summary,
            "url": page.url
        }
    except wikipedia.exceptions.DisambiguationError as e:
        return {"error": f"Mehrdeutiger Begriff. Beispiele: {', '.join(e.options[:3])}"}
    except wikipedia.exceptions.PageError:
        return {"error": "Kein Wikipedia-Eintrag gefunden."}
