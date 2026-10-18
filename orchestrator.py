"""
Multi-Agent Orchestrator for Task 3: Meeting to Scope of Work.
Coordinates staged agent execution, typed handoffs, and follow-up change detection.
"""
from typing import Dict, Any, Optional
from app.schemas import (
    MeetingTranscript,
    AnalysisRunResponse,
    ScopeOfWork,
    DeveloperTask,
    ClientProposal,
    ScopeDiffReport
)
from agents.transcript_analyst import transcript_analyst
from agents.product_feasibility import feasibility_agent
from agents.scope_agent import scope_agent
from agents.estimation_agent import estimation_agent
from agents.proposal_agent import proposal_agent
from scope_diff.diff_engine import diff_engine

class MeetingToScopeOrchestrator:
    def process_meeting(
        self,
        transcript: MeetingTranscript,
        baseline_transcript: Optional[MeetingTranscript] = None,
        baseline_sow: Optional[ScopeOfWork] = None
    ) -> AnalysisRunResponse:
        """
        Executes the 5-agent pipeline sequentially with typed validations:
        Transcript Analyst -> Feasibility Agent -> Scope Agent -> Estimation Agent -> Proposal Agent
        """
        # Step 1: Extract requirements
        raw_reqs = transcript_analyst.analyze_transcript(transcript)

        # Step 2: Product Feasibility check via Task 1 Knowledge Brain
        validated_reqs = feasibility_agent.evaluate_feasibility(raw_reqs)

        # Step 3: Scope of Work compilation
        sow = scope_agent.generate_scope(transcript, validated_reqs)

        # Step 4: Developer task estimation
        tasks = estimation_agent.estimate_tasks(validated_reqs)

        # Step 5: Proposal synthesis
        proposal = proposal_agent.generate_proposal(sow, tasks)

        # Step 6: Follow-up scope comparison (if baseline provided)
        diff_report: Optional[ScopeDiffReport] = None
        if baseline_transcript and baseline_sow:
            diff_report = diff_engine.compare_meetings(
                baseline_transcript=baseline_transcript,
                baseline_requirements=baseline_sow.agreed_requirements,
                followup_transcript=transcript
            )

        return AnalysisRunResponse(
            meeting_id=transcript.meeting_id,
            scope_of_work=sow,
            tasks=tasks,
            proposal=proposal,
            diff_report=diff_report
        )

orchestrator = MeetingToScopeOrchestrator()
