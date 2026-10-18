"""
FastAPI application for Task 3: Meeting to Scope of Work.
"""
import os
import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.schemas import MeetingTranscript, AnalysisRunResponse, ClientProposal, ScopeDiffReport
from agents.orchestrator import orchestrator
from agents.proposal_agent import proposal_agent
from scope_diff.diff_engine import diff_engine

TRANSCRIPTS_DIR = Path(__file__).resolve().parent.parent / "transcripts"

app = FastAPI(
    title="AI Tech Consultant - Meeting to Scope Service",
    version="1.0.0",
    description="Multi-agent meeting analysis, feasibility checking via Knowledge Brain, task estimation, client proposals, and baseline scope comparison."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for generated SOWs and proposals
STORED_RUNS: Dict[str, AnalysisRunResponse] = {}

def load_transcript(meeting_id: str) -> MeetingTranscript:
    clean_id = meeting_id.lower().replace("-", "_")
    file_path = TRANSCRIPTS_DIR / f"{clean_id}.json"
    if not file_path.exists():
        # Try finding meeting_a, meeting_b, meeting_c
        for f in TRANSCRIPTS_DIR.glob("*.json"):
            if meeting_id.lower() in f.stem.lower():
                file_path = f
                break
    if not file_path.exists():
        raise HTTPException(status_code=404, detail=f"Transcript file not found for {meeting_id}")

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        return MeetingTranscript(**data)

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": "Task 3 - Meeting to Scope Service",
        "transcripts_available": [f.stem for f in TRANSCRIPTS_DIR.glob("*.json")]
    }

@app.get("/transcripts")
async def list_transcripts():
    results = []
    for f in TRANSCRIPTS_DIR.glob("*.json"):
        with open(f, "r", encoding="utf-8") as file:
            data = json.load(file)
            results.append({
                "meeting_id": data.get("meeting_id"),
                "title": data.get("title"),
                "client_name": data.get("client_name"),
                "date": data.get("date"),
                "utterance_count": len(data.get("utterances", []))
            })
    return results

@app.get("/transcripts/{meeting_id}")
async def get_transcript_detail(meeting_id: str):
    return load_transcript(meeting_id)

@app.post("/analyze/{meeting_id}", response_model=AnalysisRunResponse)
async def analyze_meeting(meeting_id: str):
    transcript = load_transcript(meeting_id)
    
    baseline_t = None
    baseline_sow = None

    # If analyzing follow-up Meeting C, load baseline Meeting A
    if "c" in meeting_id.lower() or "followup" in meeting_id.lower():
        baseline_t = load_transcript("meeting_a")
        # Ensure Meeting A has been processed
        if "MEETING-A" not in STORED_RUNS:
            STORED_RUNS["MEETING-A"] = orchestrator.process_meeting(baseline_t)
        baseline_sow = STORED_RUNS["MEETING-A"].scope_of_work

    run_response = orchestrator.process_meeting(
        transcript=transcript,
        baseline_transcript=baseline_t,
        baseline_sow=baseline_sow
    )

    STORED_RUNS[transcript.meeting_id] = run_response
    return run_response

class ApproveProposalRequest(BaseModel):
    reviewer_name: str = "Senior Technical Consultant"

@app.post("/proposals/{meeting_id}/approve", response_model=ClientProposal)
async def approve_proposal(meeting_id: str, req: ApproveProposalRequest):
    run_response = STORED_RUNS.get(meeting_id.upper())
    if not run_response:
        # Try running analysis first
        run_response = await analyze_meeting(meeting_id)
    
    approved = proposal_agent.approve_proposal(run_response.proposal, req.reviewer_name)
    run_response.proposal = approved
    return approved

@app.get("/compare/meeting-a/meeting-c", response_model=ScopeDiffReport)
async def compare_baseline_and_followup():
    t_a = load_transcript("meeting_a")
    t_c = load_transcript("meeting_c")
    if "MEETING-A" not in STORED_RUNS:
        STORED_RUNS["MEETING-A"] = orchestrator.process_meeting(t_a)
    
    baseline_sow = STORED_RUNS["MEETING-A"].scope_of_work
    report = diff_engine.compare_meetings(
        baseline_transcript=t_a,
        baseline_requirements=baseline_sow.agreed_requirements,
        followup_transcript=t_c
    )
    return report

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8003, reload=False)
