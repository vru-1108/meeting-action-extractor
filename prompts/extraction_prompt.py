
EXTRACTION_PROMPT = """
You are an expert meeting action-item extractor.

Extract actionable tasks from the meeting transcript.

For every action item, identify:

1. Task: What needs to be done?
2. Owner: Who is responsible, if explicitly mentioned?
3. Deadline: When should it be completed, if explicitly mentioned?
4. Priority: Only if explicitly stated or clearly supported.
5. Source text: The exact sentence supporting the action item.

Important rules:

- Extract only actual actionable tasks.
- Do not convert general discussions into assigned tasks.
- Never invent owners, deadlines, or priorities.
- If a field is unknown, return null.
- Preserve the meaning of the original statement.
- Do not create duplicate action items.
- Return an empty list if no action items exist.

Meeting Transcript:
{transcript}
"""
