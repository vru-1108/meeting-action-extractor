# Meeting Intelligence & Action Extractor

An AI-powered meeting intelligence application that transforms raw meeting transcripts into structured, actionable insights using **LangGraph, LangChain, and local LLMs through Ollama**.

The application analyzes meeting conversations, generates concise summaries, identifies important decisions, extracts action items, and captures owners and deadlines wherever explicitly mentioned.

## Key Features

- **Transcript Input:** Upload a `.txt` meeting transcript or paste meeting notes directly.
- **Meeting Summarization:** Generate concise summaries of lengthy discussions.
- **Key Topic Extraction:** Identify the main subjects discussed during the meeting.
- **Decision Detection:** Extract important decisions made during discussions.
- **Action Item Extraction:** Identify tasks, responsibilities, owners, deadlines, and priorities when supported by the transcript.
- **Open Question Identification:** Highlight unresolved questions and pending discussions.
- **Structured Output:** Use Pydantic models to validate extracted information.
- **Hallucination Guardrails:** Check extracted information against the original transcript and flag unsupported claims.
- **Retry Mechanism:** Retry extraction when the generated output fails validation.
- **Export Results:** Export structured meeting insights in JSON and CSV formats.

## Architecture

The application uses a sequential LangGraph workflow to process meeting transcripts.

```text
                Meeting Transcript
                        |
                        v
                 Input Validation
                        |
                        v
                Transcript Preprocessing
                        |
                        v
                 Meeting Analysis
                        |
                        v
                Action Item Extraction
                        |
                        v
                 Output Validation
                        |
                 +------+------+
                 |             |
               Valid         Invalid
                 |             |
                 v             v
              Guardrails    Retry Extraction
                 |             |
                 v             |
              Finalize <-------+
                 |
                 v
             Final Results
```

## Workflow Components

| Component | Responsibility |
|---|---|
| `validate_input` | Checks whether the uploaded or pasted transcript is valid. |
| `preprocess` | Cleans and prepares the transcript. |
| `analyze_meeting` | Generates a summary, key topics, decisions, and open questions. |
| `extract_actions` | Extracts actionable tasks with relevant details. |
| `validate_output` | Validates the structured output using Pydantic. |
| `guardrail` | Checks whether extracted information is supported by the transcript. |
| `finalize` | Prepares the final structured meeting result. |

The workflow includes conditional routing for validation failures and a limited retry mechanism to avoid unnecessary repeated LLM calls.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core application development |
| LangGraph | Workflow orchestration and state management |
| LangChain | LLM integration |
| Ollama | Running LLMs locally |
| Pydantic | Structured output validation |
| Streamlit | Interactive user interface |
| Pandas | Data processing and CSV export |
| Pytest | Unit and workflow testing |

## Project Structure

```text
meeting-action-extractor/
│
├── app.py
├── requirements.txt
├── README.md
│
├── graph/
│   ├── __init__.py
│   ├── state.py
│   ├── workflow.py
│   ├── nodes.py
│   └── edges.py
│
├── schemas/
│   ├── __init__.py
│   └── meeting.py
│
├── services/
│   ├── llm_service.py
│   └── guardrail_service.py
│
├── prompts/
│   ├── analysis_prompt.py
│   └── extraction_prompt.py
│
├── utils/
│   ├── preprocessing.py
│   └── export.py
│
└── tests/
    ├── test_extraction.py
    ├── test_guardrails.py
    └── test_workflow.py
```

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/meeting-action-extractor.git

cd meeting-action-extractor
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it:

**Windows**
```bash
venv\Scripts\activate
```

**macOS / Linux**
```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Install and configure Ollama

Download Ollama from:

https://ollama.com/

Pull a model:

```bash
ollama pull llama3.1
```

Ensure the Ollama service is running before starting the application.

### 5. Run the application

```bash
streamlit run app.py
```

Open the local Streamlit URL displayed in your terminal.

## Example Input

```text
Meeting: Product Development Discussion

John: We need to complete the authentication module by Friday.

Sarah: I will handle the API integration and finish it by Wednesday.

David: We should review the database schema before the next sprint.

John: Agreed. Sarah will complete the API integration,
and David will review the database schema.
```

## Example Output

### Meeting Summary

The team discussed authentication development, API integration, and database schema review.

### Key Topics

- Authentication module
- API integration
- Database schema review

### Decisions

- Sarah will handle API integration.
- David will review the database schema.

### Action Items

| Task | Owner | Deadline |
|---|---|---|
| Complete authentication module | John | Friday |
| Complete API integration | Sarah | Wednesday |
| Review database schema | David | Not specified |

*Example output is illustrative. Actual results will depend on the transcript and model.*

## Engineering Focus

This project explores practical implementation of:

- Stateful AI workflows using LangGraph.
- Structured LLM responses using Pydantic.
- Prompt engineering and context management.
- Conditional workflow routing and retry mechanisms.
- Evidence-based extraction and hallucination mitigation.
- Separation of application logic, LLM services, and workflow orchestration.
- Testing and validating AI-generated results.

## Future Enhancements

- Audio meeting transcription using faster-whisper.
- Speaker diarization and timestamp-aware action extraction.
- Multilingual meeting transcript support.
- Human-in-the-loop review and editing.
- Persistent workflow state and conversation history.
- Cloud-based LLM integration for public deployment.
- Calendar and project-management integrations.

## License

This project is intended for learning, experimentation, and portfolio demonstration. A license can be added when the repository is published.
