import wikipedia


# Set language to German
wikipedia.set_lang("de")

def get_wikipedia_summary(term: str, sentences: int = 3) -> dict:
    """
    Searches Wikipedia for a given term and returns a short summary.

    Args:
        term (str): The search term to look up on Wikipedia.
        sentences (int, optional): Number of sentences to include in the summary. Default is 3.

    Returns:
        dict: A dictionary containing either:
            - "summary" (str): The summary text of the article.
            - "url" (str): The full URL to the Wikipedia page.
            - "error" (str): An error message if the article could not be retrieved or the term is ambiguous.
    """
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
