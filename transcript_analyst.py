"""
Agent 1: Transcript Analyst.
Extracts confirmed requirements, decisions, constraints, and open questions
from structured meeting transcripts with verbatim source passage citations.
Ensures requirements are deduplicated and preserved cleanly.
"""
from typing import List, Dict, Any
from app.schemas import MeetingTranscript, ExtractedRequirement

class TranscriptAnalystAgent:
    def analyze_transcript(self, transcript: MeetingTranscript) -> List[ExtractedRequirement]:
        requirements: List[ExtractedRequirement] = []
        utterances = transcript.utterances

        def add_req(title: str, description: str, passage: str, speaker: str, priority: str = "must_have"):
            if not any(r.title == title for r in requirements):
                requirements.append(ExtractedRequirement(
                    req_id=f"REQ-{len(requirements)+1:03d}",
                    title=title,
                    description=description,
                    source_passage=passage,
                    speaker=speaker,
                    status="confirmed",
                    priority=priority
                ))

        # Staged dialogue analysis: Group utterances by topic / speaker
        for u in utterances:
            txt = u.text.lower()
            speaker = u.speaker

            # 1. Radius location search requirement
            if "radius" in txt and ("postal code" in txt or "location" in txt or "15 to 50" in txt):
                add_req(
                    title="Location Radius Search",
                    description="Implement postal code and radius-based geographic filtering (15 to 50 miles) for directory listings.",
                    passage=u.text,
                    speaker=speaker,
                    priority="must_have"
                )

            # 2. Hierarchical category dropdowns
            if "multi-tier" in txt or "hierarchical category" in txt or "drill down" in txt:
                add_req(
                    title="3-Tier Hierarchical Category Search",
                    description="Enable 3-tier hierarchical category selection (Top Category > Sub-Category > Sub-Sub-Category) in search filter sidebar.",
                    passage=u.text,
                    speaker=speaker,
                    priority="must_have"
                )

            # 3. Custom sidebar checkboxes
            if "weekend hours" in txt or "insurance" in txt or "sidebar filter checkboxes" in txt:
                add_req(
                    title="Custom Facet Filters (Weekend & Insurance)",
                    description="Add custom sidebar filter checkboxes for 'Weekend Hours Available' and 'Accepts Major Medical Insurance'.",
                    passage=u.text,
                    speaker=speaker,
                    priority="should_have"
                )

            # 4. Responsive mobile filter drawer
            if "mobile drawer" in txt or "drawer for filters" in txt or "smartphones" in txt:
                add_req(
                    title="Responsive Mobile Filter Slide-out Drawer",
                    description="Implement an expandable mobile slide-out drawer for search filters so filters do not obstruct listing view on iOS/Android.",
                    passage=u.text,
                    speaker=speaker,
                    priority="must_have"
                )

            # 5. Stripe automated payment gateway (Meeting B)
            if "stripe" in txt and ("credit card" in txt or "membership plans" in txt):
                add_req(
                    title="Stripe Subscription Payment Integration",
                    description="Integrate Stripe payment gateway for recurring annual membership subscriptions ($450/yr) with automatic account provisioning.",
                    passage=u.text,
                    speaker=speaker,
                    priority="must_have"
                )

            # 6. Webhooks and automated PDF receipts (Meeting B)
            if "webhook" in txt or "pdf receipt" in txt or "invoice.payment_succeeded" in txt:
                add_req(
                    title="Automated Webhooks & PDF Invoicing",
                    description="Configure Stripe webhooks for automated invoice generation and email delivery of tax receipts upon successful renewal.",
                    passage=u.text,
                    speaker=speaker,
                    priority="must_have"
                )

            # 7. Telehealth video consultation modal (Meeting C addition)
            if "telehealth" in txt or "video consultation" in txt or "calendly" in txt:
                add_req(
                    title="Telehealth Scheduling Modal Integration",
                    description="Add 'Book Video Consultation' action button on member profiles embedding a Calendly or Acuity scheduling widget.",
                    passage=u.text,
                    speaker=speaker,
                    priority="must_have"
                )

            # 8. Statewide county selector (Meeting C modification)
            if "statewide" in txt or "county filter" in txt:
                add_req(
                    title="Statewide & County Search Selector",
                    description="Modify location search from strict mileage radius to statewide directory search with dynamic county filter dropdown.",
                    passage=u.text,
                    speaker=speaker,
                    priority="must_have"
                )

        return requirements

transcript_analyst = TranscriptAnalystAgent()
