
ANALYSIS_PROMPT = """
You are an expert meeting analyst.

Analyze the meeting transcript provided below.

Extract the following:

1. Summary:
   Provide a concise summary of the meeting.

2. Key Topics:
   Identify the main topics discussed.

3. Decisions:
   Identify decisions explicitly made during the meeting.
   Include the exact supporting sentence from the transcript.

4. Open Questions:
   Identify unresolved questions or topics requiring clarification.

Important rules:
- Use only information present in the transcript.
- Do not invent facts, names, decisions, or deadlines.
- If no decisions were made, return an empty list.
- If there are no open questions, return an empty list.
- Keep the summary concise.

Meeting Transcript:
{transcript}
"""
