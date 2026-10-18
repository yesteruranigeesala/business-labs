"""
Agent 3: Scope Agent.
Transforms validated requirements into a formal, binding Scope of Work (SOW)
with clear deliverables, explicit exclusions, and verifiable acceptance criteria.
"""
from typing import List
from app.schemas import MeetingTranscript, ExtractedRequirement, ScopeOfWork

class ScopeAgent:
    def generate_scope(self, transcript: MeetingTranscript, requirements: List[ExtractedRequirement]) -> ScopeOfWork:
        # Deliverables based on confirmed requirements
        deliverables: List[str] = []
        acceptance_criteria: List[str] = []

        for req in requirements:
            if "radius" in req.title.lower():
                deliverables.append("Configured Zip/Postal Code radius search slider (15-50 miles) in Search Settings tab.")
                acceptance_criteria.append("Directory visitors entering a valid postal code can filter results within selectable 15, 25, or 50 mile boundaries.")
            elif "category" in req.title.lower():
                deliverables.append("Structured 3-tier category hierarchy (Top, Sub, Sub-Sub) in main directory search sidebar.")
                acceptance_criteria.append("Dropdown menus cascade dynamically without page reload upon selecting parent category.")
            elif "facet" in req.title.lower():
                deliverables.append("Custom searchable checkbox fields for 'Weekend Hours' and 'Insurance Accepted' via Form Manager.")
                acceptance_criteria.append("Filtering by 'Accepts Insurance' displays only members who selected 'Yes' in their profile.")
            elif "mobile" in req.title.lower():
                deliverables.append("Responsive mobile filter drawer with animated slide-out trigger for iOS and Android viewports.")
                acceptance_criteria.append("Filter drawer opens smoothly on tap, does not obscure member results, and closes cleanly upon applying filters.")
            elif "stripe" in req.title.lower():
                deliverables.append("Stripe payment gateway integration for automated annual $450 member plan subscriptions.")
                acceptance_criteria.append("Test card transactions process successfully in test mode and trigger member account activation.")
            elif "webhook" in req.title.lower():
                deliverables.append("Stripe webhook listener and automated branded invoice PDF email notifications.")
                acceptance_criteria.append("Webhook events invoice.payment_succeeded send dynamic email receipt with client tax ID.")
            elif "telehealth" in req.title.lower():
                deliverables.append("Embedded Calendly / Acuity modal scheduling trigger on member directory profiles.")
                acceptance_criteria.append("Clicking 'Book Consultation' launches embedded scheduling modal without navigating away.")
            elif "statewide" in req.title.lower():
                deliverables.append("Statewide search dropdown with dynamic county filtering.")
                acceptance_criteria.append("Selecting a county filters members across the entire state without requiring exact zip codes.")

        # Standard explicit exclusions to protect the agency
        exclusions = [
            "Native iOS and Android mobile app development (requires separate scoping and budget).",
            "Third-party merchant processor transaction fees or Stripe account onboarding approval.",
            "Manual copywriting or translation of custom practitioner bios.",
            "Data cleanup of corrupted legacy member CSV imports."
        ]

        # Key dependencies
        dependencies = [
            "Client provision of active Google Maps API key with Geocoding and Places API enabled.",
            "Client provision of Stripe Live and Test API keys with Webhook permissions.",
            "Timely feedback on staging environment revisions within 2 business days."
        ]

        # Client responsibilities
        client_responsibilities = [
            "Review and approve staging preview links within 48 hours of delivery.",
            "Provide brand assets, high-resolution SVG logo, and primary corporate color hex codes.",
            "Designate a single authorized executive point of contact for change order sign-offs."
        ]

        # Open questions / risks
        open_questions = [
            "Confirm exact list of county names for statewide dropdown.",
            "Confirm whether Calendly embed requires individual practitioner webhook tracking."
        ]

        return ScopeOfWork(
            project_id=transcript.project_name.lower().replace(" ", "-"),
            project_title=transcript.project_name,
            client_name=transcript.client_name,
            objective=f"Deliver production enhancements for {transcript.client_name} to maximize directory conversions and member satisfaction.",
            problem_statement="Current platform limitations create visitor friction, unsegmented search results, and high administrative overhead.",
            agreed_requirements=requirements,
            deliverables=deliverables,
            exclusions=exclusions,
            dependencies=dependencies,
            acceptance_criteria=acceptance_criteria,
            client_responsibilities=client_responsibilities,
            open_questions=open_questions,
            created_at=transcript.date,
            version="v1.0"
        )

scope_agent = ScopeAgent()
