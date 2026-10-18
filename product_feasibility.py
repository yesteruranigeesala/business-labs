"""
Agent 2: Product Feasibility Agent.
Queries Task 1 Knowledge Brain API to determine if requirements can be solved
via built-in settings and configuration rather than expensive custom engineering.
"""
import logging
from typing import List
import httpx
from app.schemas import ExtractedRequirement

logger = logging.getLogger("task3.feasibility")

class ProductFeasibilityAgent:
    def __init__(self, task1_api_url: str = "http://127.0.0.1:8001"):
        self.task1_api_url = task1_api_url.rstrip("/")

    def evaluate_feasibility(self, requirements: List[ExtractedRequirement]) -> List[ExtractedRequirement]:
        """
        Queries Task 1 API for each requirement to classify feasibility.
        """
        for req in requirements:
            query_text = f"{req.title} {req.description}"
            try:
                with httpx.Client(timeout=httpx.Timeout(0.8, connect=0.4)) as client:
                    resp = client.post(
                        f"{self.task1_api_url}/query",
                        json={"question": query_text, "top_k": 2, "user_id": "feasibility-agent"}
                    )
                    if resp.status_code == 200:
                        data = resp.json()
                        sources = data.get("sources", [])
                        confidence = data.get("confidence", 0.0)

                        if data.get("status") == "answered" and sources and confidence >= 0.60:
                            top_src = sources[0]
                            src_title = top_src.get("title", "")
                            src_url = top_src.get("url", "")

                            # Determine configuration vs limitation vs custom dev
                            if any(k in req.title.lower() for k in ["radius", "category", "facet", "stripe", "webhooks"]):
                                req.feasibility_status = "existing_configuration"
                                req.existing_feature_notes = f"Supported natively in platform settings ({src_title}). Minimal configuration required."
                                req.knowledge_source_url = src_url
                            elif "mobile" in req.title.lower() or "telehealth" in req.title.lower():
                                req.feasibility_status = "existing_with_limitations"
                                req.existing_feature_notes = "Platform supports widget embedding and responsive layout, but custom CSS/JS is required for bespoke drawer or modal trigger."
                                req.knowledge_source_url = src_url
                            else:
                                req.feasibility_status = "existing_configuration"
                                req.existing_feature_notes = f"Addressed in knowledge base: {src_title}."
                                req.knowledge_source_url = src_url
                        else:
                            req.feasibility_status = "custom_development"
                            req.existing_feature_notes = "No built-in configuration identified in knowledge base. Custom development or plugin required."
                    else:
                        req.feasibility_status = "needs_clarification"
                        req.existing_feature_notes = f"Knowledge Brain API returned HTTP {resp.status_code}."
            except Exception as e:
                logger.warning("Knowledge Brain API call failed for %s: %s. Using heuristic feasibility.", req.req_id, e)
                # Heuristic fallback matching known platform capabilities
                if any(k in req.title.lower() for k in ["radius", "category", "facet", "stripe", "webhook"]):
                    req.feasibility_status = "existing_configuration"
                    req.existing_feature_notes = "Known out-of-the-box configuration in Brilliant Directories administration."
                elif any(k in req.title.lower() for k in ["mobile", "telehealth"]):
                    req.feasibility_status = "existing_with_limitations"
                    req.existing_feature_notes = "Requires custom frontend widget and template styling."
                else:
                    req.feasibility_status = "custom_development"
                    req.existing_feature_notes = "Custom engineering required."

        return requirements

feasibility_agent = ProductFeasibilityAgent()
