from openai import AzureOpenAI

class CobolSummarizer:
    def __init__(self, client: AzureOpenAI, deployment_name: str):
        self.client = client
        self.deployment_name = deployment_name

    def summarize_paragraph(self, name: str, code: str):
        prompt = f"""
You are a senior COBOL modernization expert.

Analyze the following COBOL paragraph.

Paragraph Name: {name}

COBOL Code:
{code}

Provide:
1. Business purpose
2. Inputs used
3. Outputs produced
4. Side effects (file I/O, calls)
5. High-level summary (2–3 sentences)
"""

        response = self.client.chat.completions.create(
            model=self.deployment_name,
            messages=[
                {"role": "system", "content": "You are a COBOL documentation expert."},
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )

        return response.choices[0].message.content
