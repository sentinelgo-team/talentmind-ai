"""
TalentMind AI - Learning Roadmap Generator
============================================
Purpose: Generates structured, prioritized learning roadmaps
         based on identified skill gaps.

Takes raw skill gap data and produces actionable,
time-bound learning paths with resources and milestones.

Author  : TalentMind AI Team
Version : 1.0.0
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

from app.utils.industry_benchmarks import get_learning_resource

logger = logging.getLogger(__name__)


# ══════════════════════════════════════════════════════════════════
# PRIORITY DEFINITIONS
# ══════════════════════════════════════════════════════════════════

PRIORITY_ORDER = {
    "critical": 1,
    "high": 2,
    "medium": 3,
    "low": 4,
}

PRIORITY_TIMELINE = {
    "critical": "Immediately (Week 1-2)",
    "high": "Short-term (Month 1)",
    "medium": "Mid-term (Month 2-3)",
    "low": "Long-term (Month 4-6)",
}


class RoadmapGenerator:
    """
    Generates structured learning roadmaps from skill gaps.

    Converts raw gap analysis into an actionable, prioritized
    learning plan with timelines, resources, and milestones.

    Usage:
        generator = RoadmapGenerator()
        roadmap = generator.generate(skill_gaps, experience_level)
    """

    def generate(
        self,
        skill_gaps: List[Dict[str, Any]],
        experience_level: str = "mid",
        target_role: str = "Software Developer",
        current_skills: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Generate a complete learning roadmap.

        Args:
            skill_gaps: List of skill gap dicts with priority
            experience_level: Candidate's current level
            target_role: Target job role
            current_skills: Skills already possessed

        Returns:
            dict: Complete structured learning roadmap
        """
        if not skill_gaps:
            return self._empty_roadmap(target_role)

        # Sort gaps by priority
        sorted_gaps = self._sort_by_priority(skill_gaps)

        # Generate phases
        phases = self._generate_phases(sorted_gaps)

        # Calculate total duration
        total_weeks = self._calculate_duration(sorted_gaps)

        # Generate milestones
        milestones = self._generate_milestones(
            phases, experience_level
        )

        # Generate weekly plan for first month
        weekly_plan = self._generate_weekly_plan(
            sorted_gaps[:8]  # First 8 most critical gaps
        )

        roadmap = {
            "target_role": target_role,
            "experience_level": experience_level,
            "total_gaps": len(skill_gaps),
            "estimated_weeks": total_weeks,
            "estimated_months": round(total_weeks / 4, 1),
            "phases": phases,
            "milestones": milestones,
            "weekly_plan": weekly_plan,
            "immediate_actions": self._get_immediate_actions(
                sorted_gaps
            ),
            "summary": self._generate_summary(
                sorted_gaps, total_weeks, target_role
            ),
        }

        logger.info(
            "Roadmap generated | gaps=%d | weeks=%d | role=%s",
            len(skill_gaps),
            total_weeks,
            target_role,
        )

        return roadmap

    def _sort_by_priority(
        self,
        skill_gaps: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """Sort skill gaps by priority order."""
        return sorted(
            skill_gaps,
            key=lambda x: PRIORITY_ORDER.get(
                x.get("priority", "low"), 4
            ),
        )

    def _generate_phases(
        self,
        sorted_gaps: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """
        Group skill gaps into learning phases.

        Phase 1: Critical skills (must-have for role)
        Phase 2: High priority skills
        Phase 3: Medium priority skills
        Phase 4: Nice-to-have skills
        """
        phases = []

        phase_map = {
            "critical": {
                "phase": 1,
                "name": "Foundation Phase",
                "description": "Critical skills required immediately",
                "skills": [],
            },
            "high": {
                "phase": 2,
                "name": "Core Competency Phase",
                "description": "High-value skills for role readiness",
                "skills": [],
            },
            "medium": {
                "phase": 3,
                "name": "Enhancement Phase",
                "description": "Skills that significantly improve profile",
                "skills": [],
            },
            "low": {
                "phase": 4,
                "name": "Mastery Phase",
                "description": "Advanced skills for career growth",
                "skills": [],
            },
        }

        for gap in sorted_gaps:
            priority = gap.get("priority", "low")
            if priority in phase_map:
                resource = get_learning_resource(
                    gap.get("skill", "")
                )
                phase_map[priority]["skills"].append({
                    "skill": gap.get("skill", ""),
                    "reason": gap.get("reason", ""),
                    "timeline": PRIORITY_TIMELINE.get(
                        priority, "TBD"
                    ),
                    "resource": resource.get(
                        "platform", "Coursera / Udemy"
                    ),
                    "duration": resource.get(
                        "duration", "2-4 weeks"
                    ),
                })

        # Only include phases with skills
        for priority_key, phase_data in phase_map.items():
            if phase_data["skills"]:
                phases.append({
                    "phase_number": phase_data["phase"],
                    "phase_name": phase_data["name"],
                    "description": phase_data["description"],
                    "priority": priority_key,
                    "skills": phase_data["skills"],
                    "skill_count": len(phase_data["skills"]),
                    "timeline": PRIORITY_TIMELINE.get(
                        priority_key, "TBD"
                    ),
                })

        return phases

    def _calculate_duration(
        self,
        skill_gaps: List[Dict[str, Any]],
    ) -> int:
        """
        Estimate total weeks needed to close all gaps.

        Critical: 2 weeks each
        High: 3 weeks each
        Medium: 2 weeks each (can overlap)
        Low: 1 week each (parallel learning)
        """
        week_map = {
            "critical": 2,
            "high": 3,
            "medium": 2,
            "low": 1,
        }

        total = sum(
            week_map.get(gap.get("priority", "low"), 1)
            for gap in skill_gaps
        )

        # Cap at reasonable maximum
        return min(total, 52)  # Max 1 year

    def _generate_milestones(
        self,
        phases: List[Dict[str, Any]],
        experience_level: str,
    ) -> List[Dict[str, str]]:
        """Generate career milestones based on phases."""
        milestones = []

        if not phases:
            return milestones

        # Week 2 milestone
        milestones.append({
            "week": "Week 2",
            "milestone": "Complete first critical skill basics",
            "goal": "Build foundation for role requirements",
        })

        # Month 1 milestone
        milestones.append({
            "week": "Month 1",
            "milestone": "Complete all critical skill courses",
            "goal": "Meet minimum job requirements",
        })

        # Month 2 milestone
        milestones.append({
            "week": "Month 2",
            "milestone": "Build 2 projects using new skills",
            "goal": "Practical experience for portfolio",
        })

        # Month 3 milestone
        milestones.append({
            "week": "Month 3",
            "milestone": "Complete high priority skills",
            "goal": "Become competitive candidate",
        })

        # Final milestone
        milestones.append({
            "week": "Month 4-6",
            "milestone": "Complete full roadmap",
            "goal": f"Ready for {experience_level}-level positions",
        })

        return milestones

    def _generate_weekly_plan(
        self,
        top_gaps: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """Generate a 4-week detailed learning plan."""
        weekly_plan = []

        for week_num in range(1, 5):
            week_gaps = []

            # Assign 2 skills per week
            start_idx = (week_num - 1) * 2
            week_skills = top_gaps[start_idx:start_idx + 2]

            for gap in week_skills:
                resource = get_learning_resource(
                    gap.get("skill", "")
                )
                week_gaps.append({
                    "skill": gap.get("skill", ""),
                    "daily_time": "1-2 hours",
                    "resource": resource.get(
                        "platform", "Coursera / Udemy"
                    ),
                    "goal": f"Complete beginner module of {gap.get('skill', '')}",
                })

            weekly_plan.append({
                "week": week_num,
                "title": f"Week {week_num} Focus",
                "skills": week_gaps,
                "deliverable": f"Complete {len(week_gaps)} skill modules",
            })

        return weekly_plan

    def _get_immediate_actions(
        self,
        sorted_gaps: List[Dict[str, Any]],
    ) -> List[str]:
        """Get top 5 immediate action items."""
        actions = []

        critical_gaps = [
            g for g in sorted_gaps
            if g.get("priority") == "critical"
        ][:3]

        high_gaps = [
            g for g in sorted_gaps
            if g.get("priority") == "high"
        ][:2]

        for gap in critical_gaps:
            skill = gap.get("skill", "")
            resource = get_learning_resource(skill)
            actions.append(
                f"Start learning {skill} immediately — "
                f"{resource.get('platform', 'Coursera / Udemy')}"
            )

        for gap in high_gaps:
            skill = gap.get("skill", "")
            actions.append(
                f"Plan to learn {skill} within 30 days"
            )

        return actions[:5]

    def _generate_summary(
        self,
        gaps: List[Dict[str, Any]],
        total_weeks: int,
        target_role: str,
    ) -> str:
        """Generate human-readable roadmap summary."""
        critical = sum(
            1 for g in gaps if g.get("priority") == "critical"
        )
        high = sum(
            1 for g in gaps if g.get("priority") == "high"
        )
        months = round(total_weeks / 4, 1)

        return (
            f"To qualify for {target_role}, focus on {critical} "
            f"critical and {high} high-priority skill gaps. "
            f"Estimated learning time: {months} months with "
            f"consistent 1-2 hours daily practice."
        )

    def _empty_roadmap(self, target_role: str) -> Dict[str, Any]:
        """Return empty roadmap when no gaps found."""
        return {
            "target_role": target_role,
            "total_gaps": 0,
            "estimated_weeks": 0,
            "estimated_months": 0,
            "phases": [],
            "milestones": [],
            "weekly_plan": [],
            "immediate_actions": [],
            "summary": (
                "No significant skill gaps detected. "
                "Focus on deepening existing expertise."
            ),
        }