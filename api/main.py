from fastapi import FastAPI,HTTPException

from schemas.api import MeetingRequest, MeetingResponse
from graph.workflow import build_workflow
from functools import lru_cache


@lru_cache
def get_workflow():
    return build_workflow()

app = FastAPI(
    title="Meeting Intelligence API",
    description="AI-powered meeting analysis and action extraction",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "Welcome to Meeting Intelligence API"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }

@app.post(
    "/api/v1/meetings/analyze",
    response_model=MeetingResponse
)
def analyze_meeting(request: MeetingRequest):

    workflow = get_workflow()

    try:
        result = workflow.invoke({
            "transcript": request.transcript,
            "retry_count": 0
        })

        # Check input validation
        if not result.get("is_input_valid", False):
            raise HTTPException(
                status_code=400,
                detail=result.get("error", "Invalid transcript.")
            )

        # Check LLM processing failures
        if result.get("processing_failed", False):
            raise HTTPException(
                status_code=502,
                detail=result.get("error", "LLM processing failed.")
            )

        # Check output validation failures
        if result.get("error") or result.get("final_result") is None:
            raise HTTPException(
                status_code=502,
                detail=result.get("error", "Meeting analysis failed.")
            )

        return MeetingResponse(
            success=True,
            result=result["final_result"],
            guardrail_issues=result.get("guardrail_issues", [])
        )

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred during meeting analysis."
        )