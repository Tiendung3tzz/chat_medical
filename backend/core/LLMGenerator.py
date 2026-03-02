from openai import OpenAI
from core.PromptManager import PromptManager

class LLMGenerator:

    def __init__(self, api_key, model="gpt-4o-mini"):
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.PRICING = {
            "gpt-4o-mini": {"input": 0.15, "output": 0.60},
            "gpt-4o": {"input": 2.50, "output": 10.00},
            "gpt-4.1-mini": {"input": 0.40, "output": 1.60},
        }
        self.prompts = PromptManager("config/prompts.yaml")
        self.system_prompt = self.prompts.system()

    def _calculate_cost(self, input_tokens, output_tokens):
        price = self.PRICING[self.model]
        return (
            input_tokens / 1_000_000 * price["input"]
            + output_tokens / 1_000_000 * price["output"]
        )

    def generate(self, query, retrieved_chunks, conversation_history=None):
        context = self.prompts.format_context(retrieved_chunks)
        messages = []
        if self.system_prompt:
            messages.append({"role": "system", "content": self.system_prompt})
        
        messages.append(
            {
                "role": "user",
                "content": self.prompts.rag(context=context, query=query),
            }
        )

        response = self.client.responses.create(
            model=self.model,
            input=messages,
            temperature=0.3,
            max_output_tokens=1024,
        )

        return {
            "answer": response.output_text,
            "input_tokens": response.usage.input_tokens,
            "output_tokens": response.usage.output_tokens,
            "cost": self._calculate_cost(
                response.usage.input_tokens,
                response.usage.output_tokens
            ),
        }