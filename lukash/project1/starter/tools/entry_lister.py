import json
from pathlib import Path

from crewai.tools import BaseTool


class ListEntriesTool(BaseTool):
    name: str = "get_all_entries"
    description: str = "List all available model card IDs and their titles."
    models: list[dict] = []

    def __init__(self):
        super().__init__()
        with open(Path(__file__).parent.parent.parent / "assets" / "models_with_description.json", encoding="utf-8") as fd:
            self.models = json.load(fd)

    def _run(self) -> str:
        return "\n".join(
            f"{model.get('modelId', '')}: {model.get('name', '')}"
            for model in self.models
        )


class ModelDetailsTool(BaseTool):
    name: str = "get_model_details"
    description: str = "Retrieve the full available description and source details for a model card by its exact model ID."
    models: dict[str, dict] = {}

    def __init__(self):
        super().__init__()
        with open(Path(__file__).parent.parent.parent / "assets" / "models_with_description.json", encoding="utf-8") as fd:
            self.models = {model["modelId"]: model for model in json.load(fd)}

    def _run(self, model_id: str) -> str:
        model = self.models.get(model_id)
        if model is None:
            return f"No model card found with ID: {model_id}"

        fields = ("modelId", "name", "intendedUse", "referencePublication", "url", "license", "frameworks")
        return "\n".join(f"{field}: {model[field]}" for field in fields if model.get(field))
