import json
from pathlib import Path

from crewai.tools import BaseTool

class KeywordSearchTool(BaseTool):
    name : str = "keyword_search"
    description : str = "Find model cards whose intended-use text contains the supplied keyword or phrase, ignoring letter case. Search one keyword or phrase at a time."
    models : dict = None

    def __init__(self):
        super().__init__()
        with open(Path(__file__).parent.parent.parent / "assets" / "models_with_description.json", 'r') as fd:
            self.models = json.load(fd)

    def _run(self, query: str) -> str:
        terms = [term.casefold() for term in query.split() if term]
        if not terms:
            return "No keyword provided."

        matches = []
        for model in self.models:
            intended_use = model.get("intendedUse", "").casefold()
            if all(term in intended_use for term in terms):
                matches.append(model.get("modelId", ""))
        return "\n".join(matches) or "No matching model cards found."
