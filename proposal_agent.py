"""
Agent 5: Proposal and Review Agent.
Synthesizes Scope of Work and Task Estimates into a formal Client Proposal.
Strictly enforces human approval barrier prior to external distribution.
"""
from typing import List, Optional
from datetime import datetime
from app.schemas import ScopeOfWork, DeveloperTask, ClientProposal

class ProposalAgent:
    def __init__(self, hourly_rate_usd: float = 120.0):
        self.hourly_rate_usd = hourly_rate_usd

    def generate_proposal(self, sow: ScopeOfWork, tasks: List[DeveloperTask]) -> ClientProposal:
        low_hours = round(sum(t.low_hours for t in tasks), 1)
        likely_hours = round(sum(t.likely_hours for t in tasks), 1)
        high_hours = round(sum(t.high_hours for t in tasks), 1)

        cost_low = round(low_hours * self.hourly_rate_usd, 2)
        cost_likely = round(likely_hours * self.hourly_rate_usd, 2)
        cost_high = round(high_hours * self.hourly_rate_usd, 2)

        # Estimate delivery timeline in weeks assuming 25-30 consulting hours/week
        timeline_weeks = round(max(1.5, likely_hours / 25.0), 1)

        exec_summary = (
            f"This proposal outlines the technical consulting engagement for {sow.client_name} "
            f"regarding the '{sow.project_title}'. By maximizing existing Brilliant Directories "
            f"native platform features and strategically deploying custom frontend enhancements, "
            f"we deliver high performance at a competitive development velocity."
        )

        problem_solution = (
            f"Problem: {sow.problem_statement}\n\n"
            f"Solution: Implement verified platform configurations supplemented with responsive "
            f"frontend mobile widgets. Total estimated engineering effort: {likely_hours} hours "
            f"(nominal range: {low_hours} - {high_hours} hrs), targeting delivery in approximately {timeline_weeks} weeks."
        )

        assumptions_and_risks = [
            f"Standard consulting billing rate: ${self.hourly_rate_usd:,.2f}/hour.",
            "Estimates reflect nominal development scenarios. Scope additions trigger formal Change Orders.",
            "Client will provide third-party API credentials (Google Maps, Stripe) at project kickoff."
        ]

        return ClientProposal(
            proposal_id=f"PROP-{sow.project_id.upper()[:12]}-V1",
            project_title=sow.project_title,
            client_name=sow.client_name,
            executive_summary=exec_summary,
            problem_and_solution=problem_solution,
            deliverables_summary=sow.deliverables,
            exclusions_summary=sow.exclusions,
            total_low_hours=low_hours,
            total_likely_hours=likely_hours,
            total_high_hours=high_hours,
            hourly_rate_usd=self.hourly_rate_usd,
            estimated_cost_low=cost_low,
            estimated_cost_likely=cost_likely,
            estimated_cost_high=cost_high,
            timeline_weeks_likely=timeline_weeks,
            assumptions_and_risks=assumptions_and_risks,
            human_approved=False,  # Enforces human approval barrier
            approved_by=None,
            approved_at=None,
            version=sow.version
        )

    def approve_proposal(self, proposal: ClientProposal, reviewer_name: str) -> ClientProposal:
        proposal.human_approved = True
        proposal.approved_by = reviewer_name
        proposal.approved_at = datetime.now().isoformat()
        return proposal

proposal_agent = ProposalAgent()
