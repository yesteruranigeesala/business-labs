"""
Unit and integration test suite for Task 3: Meeting to Scope of Work.
"""
import unittest
from pathlib import Path
import json

from app.schemas import MeetingTranscript
from agents.transcript_analyst import transcript_analyst
from agents.scope_agent import scope_agent
from agents.estimation_agent import estimation_agent
from agents.proposal_agent import proposal_agent
from scope_diff.diff_engine import diff_engine

TRANSCRIPTS_DIR = Path(__file__).resolve().parent.parent / "transcripts"

class TestTask3MeetingToScope(unittest.TestCase):
    def setUp(self):
        with open(TRANSCRIPTS_DIR / "meeting_a.json", "r", encoding="utf-8") as f:
            self.transcript_a = MeetingTranscript(**json.load(f))
        with open(TRANSCRIPTS_DIR / "meeting_c.json", "r", encoding="utf-8") as f:
            self.transcript_c = MeetingTranscript(**json.load(f))

    def test_transcript_analyst_extraction(self):
        reqs = transcript_analyst.analyze_transcript(self.transcript_a)
        self.assertGreaterEqual(len(reqs), 4)
        for r in reqs:
            self.assertTrue(len(r.source_passage) > 0)
            self.assertTrue(len(r.speaker) > 0)

    def test_scope_deliverables_and_exclusions(self):
        reqs = transcript_analyst.analyze_transcript(self.transcript_a)
        sow = scope_agent.generate_scope(self.transcript_a, reqs)
        self.assertGreaterEqual(len(sow.deliverables), 4)
        self.assertGreaterEqual(len(sow.exclusions), 3)
        self.assertTrue(any("native ios" in e.lower() for e in sow.exclusions))

    def test_estimation_monotonic_hours(self):
        reqs = transcript_analyst.analyze_transcript(self.transcript_a)
        tasks = estimation_agent.estimate_tasks(reqs)
        self.assertGreaterEqual(len(tasks), 4)
        for t in tasks:
            self.assertLessEqual(t.low_hours, t.likely_hours)
            self.assertLessEqual(t.likely_hours, t.high_hours)

    def test_proposal_human_approval_barrier(self):
        reqs = transcript_analyst.analyze_transcript(self.transcript_a)
        sow = scope_agent.generate_scope(self.transcript_a, reqs)
        tasks = estimation_agent.estimate_tasks(reqs)
        proposal = proposal_agent.generate_proposal(sow, tasks)
        
        # Must be unapproved by default
        self.assertFalse(proposal.human_approved)
        self.assertIsNone(proposal.approved_by)

        # Human sign-off
        approved = proposal_agent.approve_proposal(proposal, "Senior Reviewer")
        self.assertTrue(approved.human_approved)
        self.assertEqual(approved.approved_by, "Senior Reviewer")

    def test_scope_diff_followup_changes(self):
        reqs_a = transcript_analyst.analyze_transcript(self.transcript_a)
        diff = diff_engine.compare_meetings(
            baseline_transcript=self.transcript_a,
            baseline_requirements=reqs_a,
            followup_transcript=self.transcript_c
        )
        self.assertIsNotNone(diff)
        self.assertTrue(diff.out_of_scope_flagged)
        self.assertEqual(diff.net_hours_delta, 10.0)
        self.assertEqual(diff.net_cost_delta_usd, 1200.0)
        self.assertTrue(diff.requires_client_change_order)

if __name__ == "__main__":
    unittest.main()
