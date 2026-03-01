import yaml

class PromptManager:
    def __init__(self, path):
        self.prompts = self._load(path)

    def _load(self, path):
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}

    def system(self):
        return self.prompts.get("system", "")

    def rag(self, context, query):
        template = self.prompts.get("rag_prompt", "{context}\n\n{query}")
        return template.format(context=context, query=query)

    @staticmethod
    def format_context(chunks):
        return "\n\n".join(
            f"[Nguon {i+1}]\n{c.metadata.get('enriched_content')}"
            for i, c in enumerate(chunks)
        )