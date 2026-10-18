"""
Agent 4: Estimation Agent.
Deconstructs requirements into concrete developer tasks and produces
calibrated 3-point hour estimates (low, likely, high) with explicit uncertainty modeling.
"""
from typing import List
from app.schemas import ExtractedRequirement, DeveloperTask

class EstimationAgent:
    def estimate_tasks(self, requirements: List[ExtractedRequirement]) -> List[DeveloperTask]:
        tasks: List[DeveloperTask] = []
        task_counter = 101

        for req in requirements:
            is_config = req.feasibility_status == "existing_configuration"
            is_custom = req.feasibility_status == "custom_development"
            is_hybrid = req.feasibility_status == "existing_with_limitations"

            if is_config:
                # Built-in configuration requires minimal engineering
                tasks.append(DeveloperTask(
                    task_id=f"TSK-{task_counter}",
                    requirement_id=req.req_id,
                    title=f"Configure {req.title} in Admin Settings",
                    description=f"Set up and test {req.title} using built-in Brilliant Directories configuration tabs.",
                    low_hours=1.5,
                    likely_hours=3.0,
                    high_hours=5.0,
                    uncertainty_level="low",
                    assumptions="Platform settings work as documented; no database migration required."
                ))
                task_counter += 1
            elif is_hybrid:
                # Requires admin configuration plus custom frontend styling/widget
                tasks.append(DeveloperTask(
                    task_id=f"TSK-{task_counter}",
                    requirement_id=req.req_id,
                    title=f"Platform Config & Form Setup: {req.title}",
                    description=f"Configure underlying form fields and parameters for {req.title}.",
                    low_hours=2.0,
                    likely_hours=4.0,
                    high_hours=6.0,
                    uncertainty_level="low",
                    assumptions="Standard form fields suffice."
                ))
                task_counter += 1

                tasks.append(DeveloperTask(
                    task_id=f"TSK-{task_counter}",
                    requirement_id=req.req_id,
                    title=f"Frontend Custom Widget & Responsive CSS: {req.title}",
                    description=f"Implement custom responsive drawer/modal UI with CSS transitions and viewport breakpoint testing.",
                    low_hours=4.0,
                    likely_hours=7.0,
                    high_hours=12.0,
                    dependencies=[f"TSK-{task_counter-1}"],
                    uncertainty_level="medium",
                    assumptions="Cross-browser compatibility for modern iOS Safari and Android Chrome."
                ))
                task_counter += 1
            else:
                # Full custom development
                tasks.append(DeveloperTask(
                    task_id=f"TSK-{task_counter}",
                    requirement_id=req.req_id,
                    title=f"Architecture & Technical Specification: {req.title}",
                    description=f"Define API data contracts, schema design, and error boundaries for {req.title}.",
                    low_hours=3.0,
                    likely_hours=5.0,
                    high_hours=8.0,
                    uncertainty_level="medium",
                    assumptions="Third party service APIs are stable and well documented."
                ))
                task_counter += 1

                tasks.append(DeveloperTask(
                    task_id=f"TSK-{task_counter}",
                    requirement_id=req.req_id,
                    title=f"Custom Engineering Implementation: {req.title}",
                    description=f"Build and test custom service logic, webhooks, or frontend components.",
                    low_hours=6.0,
                    likely_hours=11.0,
                    high_hours=18.0,
                    dependencies=[f"TSK-{task_counter-1}"],
                    uncertainty_level="high",
                    assumptions="Third party credentials provided without delay."
                ))
                task_counter += 1

        # Add standard QA & Staging deployment task
        tasks.append(DeveloperTask(
            task_id=f"TSK-{task_counter}",
            requirement_id="QA-GENERAL",
            title="End-to-End QA, Cross-Device Testing & Staging Release",
            description="Comprehensive validation across desktop and mobile devices, automated test suite verification, and client walkthrough.",
            low_hours=3.0,
            likely_hours=5.0,
            high_hours=8.0,
            uncertainty_level="low",
            assumptions="Client provides staging feedback within 48 hours."
        ))

        return tasks

estimation_agent = EstimationAgent()
