from graph.workflow import build_workflow


def test_empty_transcript():
    app = build_workflow()

    result = app.invoke({"transcript": ""})

    assert result["is_input_valid"] is False
    assert "transcript" in result["error"].lower()


def test_short_transcript():
    app = build_workflow()

    result = app.invoke({"transcript": "Hello team."})

    assert result["is_input_valid"] is False
    assert "too short" in result["error"].lower()


def test_ollama_failure(monkeypatch):
    def failing_llm():
        raise ConnectionError("Ollama is unavailable")

    monkeypatch.setattr("graph.nodes.get_llm", failing_llm)

    app = build_workflow()

    result = app.invoke({
        "transcript": (
            "Sarah will complete API integration by Wednesday."
        ),
        "retry_count": 0
    })

    assert result["processing_failed"] is True
    assert "Ollama" in result["error"]