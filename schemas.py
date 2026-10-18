"""
Pydantic schemas and data contracts for Task 3: Meeting to Scope of Work.
"""
from typing import List, Optional, Dict, Any, Literal
from pydantic import BaseModel, Field

class TranscriptUtterance(BaseModel):
    speaker: str
    timestamp: Optional[str] = None
    text: str

class MeetingTranscript(BaseModel):
    meeting_id: str
    title: str
    date: str
    client_name: str
    project_name: str
    participants: List[str]
    utterances: List[TranscriptUtterance]
    full_text: Optional[str] = None

class ExtractedRequirement(BaseModel):
    req_id: str = Field(..., description="Unique ID, e.g. REQ-001")
    title: str
    description: str
    source_passage: str = Field(..., description="Verbatim quote from meeting transcript")
    speaker: str
    status: Literal["confirmed", "assumed", "open_question"] = "confirmed"
    priority: Literal["must_have", "should_have", "optional"] = "must_have"
    feasibility_status: Optional[Literal["existing_configuration", "existing_with_limitations", "custom_development", "needs_clarification"]] = None
    existing_feature_notes: Optional[str] = None
    knowledge_source_url: Optional[str] = None

class DeveloperTask(BaseModel):
    task_id: str = Field(..., description="e.g. TSK-101")
    requirement_id: str
    title: str
    description: str
    low_hours: float
    likely_hours: float
    high_hours: float
    dependencies: List[str] = Field(default_factory=list)
    uncertainty_level: Literal["low", "medium", "high"] = "medium"
    assumptions: str

class ScopeOfWork(BaseModel):
    project_id: str
    project_title: str
    client_name: str
    objective: str
    problem_statement: str
    agreed_requirements: List[ExtractedRequirement]
    deliverables: List[str]
    exclusions: List[str]
    dependencies: List[str]
    acceptance_criteria: List[str]
    client_responsibilities: List[str]
    open_questions: List[str]
    created_at: str
    version: str = "v1.0"

class ClientProposal(BaseModel):
    proposal_id: str
    project_title: str
    client_name: str
    executive_summary: str
    problem_and_solution: str
    deliverables_summary: List[str]
    exclusions_summary: List[str]
    total_low_hours: float
    total_likely_hours: float
    total_high_hours: float
    hourly_rate_usd: float = 120.0
    estimated_cost_low: float
    estimated_cost_likely: float
    estimated_cost_high: float
    timeline_weeks_likely: float
    assumptions_and_risks: List[str]
    human_approved: bool = False
    approved_by: Optional[str] = None
    approved_at: Optional[str] = None
    version: str = "v1.0"

class ScopeDiffItem(BaseModel):
    req_id: str
    change_type: Literal["added", "modified", "removed", "unchanged", "out_of_scope"]
    title: str
    description: str
    baseline_details: Optional[str] = None
    revised_details: Optional[str] = None
    hours_delta_likely: float = 0.0
    cost_impact_usd: float = 0.0
    action_required: str

class ScopeDiffReport(BaseModel):
    baseline_meeting_id: str
    followup_meeting_id: str
    summary_of_changes: str
    items: List[ScopeDiffItem]
    net_hours_delta: float
    net_cost_delta_usd: float
    timeline_shift_weeks: float
    out_of_scope_flagged: bool
    requires_client_change_order: bool

class AnalysisRunResponse(BaseModel):
    meeting_id: str
    scope_of_work: ScopeOfWork
    tasks: List[DeveloperTask]
    proposal: ClientProposal
    diff_report: Optional[ScopeDiffReport] = None
