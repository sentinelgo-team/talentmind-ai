"""
TalentMind AI - Skill Gap Analysis Page
=========================================
Purpose: Skill gap analysis UI page.
Always reads resume from session state.
Never uses hardcoded user data.

Author  : TalentMind AI Team
Version : 1.0.0
"""

from __future__ import annotations

import streamlit as st
from typing import Any, Dict, List, Optional


def _get_resume_text() -> Optional[str]:
    """
    Get current user resume text from session state.

    Confirmed key from upload.py:
        st.session_state["resume_text"] = result["raw_text"]

    Works for ANY user with ANY resume.
    Never hardcoded. Always dynamic.

    Returns:
        str : Resume text if found
        None: If no resume uploaded yet
    """
    # Primary key confirmed from upload.py line 175
    text = st.session_state.get("resume_text", "")
    if text and isinstance(text, str) and len(text.strip()) > 50:
        return text.strip()

    # Fallback keys for safety
    for key in ["extracted_text", "raw_resume_text", "resume_content"]:
        value = st.session_state.get(key, "")
        if value and isinstance(value, str) and len(value.strip()) > 50:
            return value.strip()

    # Check nested dicts
    for dict_key in ["parsed_resume", "resume_data"]:
        data = st.session_state.get(dict_key, {})
        if isinstance(data, dict):
            nested = data.get("resume_text", "")
            if nested and len(nested.strip()) > 50:
                return nested.strip()

    return None


def render_skill_gap_page() -> None:
    """
    Render skill gap analysis page.

    Reads resume dynamically from session state.
    Works for any user, any resume, any role.
    """
    st.title("Skill Gap Analysis")
    st.markdown(
        "Identify gaps between your current skills "
        "and target role requirements."
    )

    # Get current user resume from session
    resume_text = _get_resume_text()

    # No resume uploaded yet
    if not resume_text:
        st.warning(
            "No resume found. Please upload your resume "
            "on the Resume Parsing page first."
        )
        return

    # Resume found
    st.success(
        "Resume loaded ({} characters)".format(
            len(resume_text)
        )
    )

    # Configuration
    st.subheader("Target Role Configuration")

    col1, col2 = st.columns(2)

    with col1:
        target_role = st.text_input(
            "Target Job Role",
            placeholder="e.g., Python Developer, Doctor, Chef",
            help="Enter any job role in any industry",
        )

    with col2:
        industry = st.text_input(
            "Industry (Optional)",
            placeholder="e.g., FinTech, Healthcare",
        )

    experience_options = [
        "Fresher (0-1 years)",
        "Junior (1-2 years)",
        "Mid Level (2-5 years)",
        "Senior (5-8 years)",
        "Lead (8+ years)",
    ]

    experience_level = st.selectbox(
        "Experience Level",
        options=experience_options,
        index=2,
    )

    job_description = st.text_area(
        "Job Description (Optional)",
        placeholder="Paste job description for better accuracy",
        height=100,
    )

    # Analyze button
    if st.button(
        "Analyze Skill Gap",
        type="primary",
        width="stretch",
    ):
        if not target_role or not target_role.strip():
            st.error("Please enter a target job role.")
            return

        _run_analysis(
            resume_text=resume_text,
            target_role=target_role.strip(),
            experience_level=experience_level,
            job_description=job_description or "",
            industry=industry or "",
        )


def _run_analysis(
    resume_text: str,
    target_role: str,
    experience_level: str,
    job_description: str = "",
    industry: str = "",
) -> None:
    """
    Run skill gap analysis.

    Args:
        resume_text     : From session state (dynamic)
        target_role     : User chosen role
        experience_level: User chosen level
        job_description : Optional JD
        industry        : Optional industry
    """
    with st.spinner(
        "Analyzing skill gaps for {}...".format(target_role)
    ):
        try:
            from app.services.skill_analyzer import SkillAnalyzer

            analyzer = SkillAnalyzer()
            level = analyzer.parse_experience_level(
                experience_level
            )

            result = analyzer.analyze_skill_gap(
                resume_text=resume_text,
                target_role=target_role,
                experience_level=level,
                job_description=job_description,
                industry=industry,
            )

            if result.get("success"):
                _display_results(result, target_role)
            else:
                st.error(
                    "Analysis failed: {}".format(
                        result.get("error", "Unknown error")
                    )
                )

        except Exception as exc:
            st.error("Error: {}".format(str(exc)))
            import traceback
            with st.expander("Error Details"):
                st.code(traceback.format_exc())


def _display_results(
    result: Dict[str, Any],
    target_role: str,
) -> None:
    """Display skill gap results."""

    score = float(result.get("overall_readiness_score", 0))
    gaps = result.get("skill_gaps", [])
    matched = result.get("matched_skills", [])
    roadmap = result.get("learning_roadmap", {})
    label = result.get("readiness_label", "")

    st.subheader("Skill Gap Results: {}".format(target_role))

    # AI generated badge
    if result.get("benchmark_source") == "AI Generated":
        st.info(
            "AI Generated benchmark for {}".format(target_role)
        )

    # Metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Match Score", "{:.0f}%".format(score))

    with col2:
        st.metric("Matched Skills", len(matched))

    with col3:
        st.metric("Missing Skills", len(gaps))

    with col4:
        weeks = roadmap.get("estimated_weeks", 0)
        st.metric(
            "Learning Time",
            "{} weeks".format(weeks) if weeks else "N/A",
        )

    # Progress bar
    progress_val = min(int(score), 100) / 100
    st.progress(
        progress_val,
        text="Readiness: {:.0f}% - {}".format(score, label),
    )

    st.divider()

    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "Current Skills",
        "Missing Skills",
        "Learning Roadmap",
        "Career Advice",
    ])

    with tab1:
        _show_current_skills(result)

    with tab2:
        _show_missing_skills(gaps)

    with tab3:
        _show_roadmap(roadmap)

    with tab4:
        _show_career_advice(result)


def _show_current_skills(result: Dict[str, Any]) -> None:
    """Show current skills tab."""

    detected = result.get("detected_skills", [])
    matched = result.get("matched_skills", [])
    strengths = result.get("strengths", [])

    if detected:
        st.markdown("**Skills Found in Your Resume:**")
        skills_text = ", ".join(str(s) for s in detected[:20])
        st.markdown(skills_text)
        st.markdown("")

    if matched:
        st.markdown(
            "**Skills Matching Role ({}):**".format(len(matched))
        )
        for skill in matched:
            if isinstance(skill, dict):
                name = skill.get("skill", "")
            else:
                name = str(skill)
            if name:
                st.markdown("- {}".format(name))
    else:
        st.info("Run analysis to see matched skills.")

    if strengths:
        st.markdown("**Your Strengths:**")
        for strength in strengths:
            st.success(strength)


def _show_missing_skills(gaps: list) -> None:
    """Show missing skills by priority."""

    if not gaps:
        st.success("No significant skill gaps detected!")
        return

    # Group by priority
    critical = []
    high = []
    medium = []
    low = []

    for gap in gaps:
        if not isinstance(gap, dict):
            continue
        priority = gap.get("priority", "low")
        if priority == "critical":
            critical.append(gap)
        elif priority == "high":
            high.append(gap)
        elif priority == "medium":
            medium.append(gap)
        else:
            low.append(gap)

    # Show critical
    if critical:
        st.markdown("### Critical Gaps (Must Learn)")
        for gap in critical:
            with st.expander(
                "{}".format(gap.get("skill", "")),
                expanded=True,
            ):
                st.markdown(
                    "**Why:** {}".format(
                        gap.get("reason", "Required for role")
                    )
                )
                if gap.get("learning_suggestion"):
                    st.markdown(
                        "**How:** {}".format(
                            gap["learning_suggestion"]
                        )
                    )
                if gap.get("estimated_weeks"):
                    st.markdown(
                        "**Time:** {} weeks".format(
                            gap["estimated_weeks"]
                        )
                    )

    # Show high
    if high:
        st.markdown("### High Priority Gaps")
        for gap in high:
            with st.expander(
                "{}".format(gap.get("skill", ""))
            ):
                st.markdown(
                    "**Why:** {}".format(
                        gap.get("reason", "Highly preferred")
                    )
                )

    # Show medium
    if medium:
        st.markdown("### Medium Priority")
        for gap in medium:
            st.markdown(
                "- **{}** - {}".format(
                    gap.get("skill", ""),
                    gap.get("reason", ""),
                )
            )

    # Show low
    if low:
        st.markdown("### Bonus Skills")
        for gap in low:
            st.markdown("- {}".format(gap.get("skill", "")))


def _show_roadmap(roadmap: Dict[str, Any]) -> None:
    """Show learning roadmap."""

    if not roadmap or roadmap.get("total_gaps", 0) == 0:
        st.info("No gaps to address. Great profile!")
        return

    summary = roadmap.get("summary", "")
    if summary:
        st.info(summary)

    # Metrics
    col1, col2 = st.columns(2)
    with col1:
        st.metric(
            "Total Duration",
            "{} months".format(
                roadmap.get("estimated_months", 0)
            ),
        )
    with col2:
        st.metric(
            "Skills to Learn",
            roadmap.get("total_gaps", 0),
        )

    # Immediate actions
    actions = roadmap.get("immediate_actions", [])
    if actions:
        st.markdown("### Start This Week")
        for i, action in enumerate(actions, 1):
            st.markdown("{}. {}".format(i, action))

    # Phases
    phases = roadmap.get("phases", [])
    if phases:
        st.markdown("### Learning Phases")
        for phase in phases:
            phase_name = phase.get("phase_name", "Phase")
            timeline = phase.get("timeline", "")
            skills = phase.get("skills", [])

            with st.expander(
                "{} - {}".format(phase_name, timeline),
                expanded=(phase.get("phase_number") == 1),
            ):
                for skill in skills:
                    st.markdown(
                        "- **{}** - {} ({})".format(
                            skill.get("skill", ""),
                            skill.get("resource", ""),
                            skill.get("duration", ""),
                        )
                    )

    # Milestones
    milestones = roadmap.get("milestones", [])
    if milestones:
        st.markdown("### Milestones")
        for m in milestones:
            st.markdown(
                "**{}**: {} - {}".format(
                    m.get("week", ""),
                    m.get("milestone", ""),
                    m.get("goal", ""),
                )
            )


def _show_career_advice(result: Dict[str, Any]) -> None:
    """Show career advice tab."""

    career_advice = result.get("career_advice", "")
    industry_insight = result.get("industry_insight", "")
    improvements = result.get("improvement_areas", [])
    strengths = result.get("strengths", [])

    if career_advice:
        st.markdown("### Career Advice")
        st.info(career_advice)

    if industry_insight:
        st.markdown("### Industry Insight")
        st.markdown(industry_insight)

    if strengths:
        st.markdown("### Your Strengths")
        for s in strengths:
            st.success(s)

    if improvements:
        st.markdown("### Areas to Improve")
        for area in improvements:
            st.warning(area)

    if not any([career_advice, industry_insight, improvements, strengths]):
        st.info("Run analysis to get career advice.")