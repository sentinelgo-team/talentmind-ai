"""
TalentMind AI - Analysis Page
================================
Displays resume parsing results with
structured sections and visual formatting.

Author  : TalentMind AI Team
Version : 1.0.0
"""

from __future__ import annotations

import logging

import streamlit as st

from app.agents.resume_agent import ResumeAgent
from app.core.constants import UIColor

logger = logging.getLogger(__name__)


def render_analysis_page() -> None:
    """Renders the resume analysis page."""

    st.markdown(
        "🔍 Resume Analysis",
        unsafe_allow_html=True
    )
    st.markdown(
        "AI-powered resume "
        "parsing and structured data extraction.",
        unsafe_allow_html=True
    )
    st.divider()

    # Check if resume uploaded
    if not st.session_state.get("resume_uploaded"):
        st.warning(
            "⚠️  **No Resume Uploaded**\n\n"
            "Please upload your resume first from the "
            "**Upload Resume** page."
        )
        return

    resume_text = st.session_state.get("resume_text", "")
    resume_id   = st.session_state.get("resume_id", "")

    # Check if already parsed
    if st.session_state.get("resume_parsed"):
        _render_parsed_results(
            st.session_state["parsed_resume"]
        )
        return

    # Parse button
    col1, col2 = st.columns([2, 1])
    with col1:
        st.info(
            f"📄 Resume ready: "
            f"**{st.session_state.get('resume_file_name')}**  "
            f"({st.session_state.get('char_count', 0):,} chars)"
        )
    with col2:
        parse_btn = st.button(
            "🤖  Parse Resume",
            type="primary",
            width="stretch"
        )

    if parse_btn:
        _run_resume_agent(resume_text, resume_id)


def _run_resume_agent(
    resume_text: str,
    resume_id  : str
) -> None:
    """Runs Resume Agent and displays results."""

    with st.spinner(
        "🤖 Resume Agent analyzing your resume..."
    ):
        try:
            agent  = ResumeAgent()
            result = agent.run({
                "resume_text": resume_text,
                "resume_id"  : resume_id,
            })

            if result["success"]:
                # Save to session
                st.session_state["resume_parsed"]  = True
                st.session_state["parsed_resume"]  = result["parsed_resume"]

                st.success(
                    f"✅ Resume parsed successfully! "
                    f"Found **{result['skills_count']}** skills, "
                    f"**{result['education_count']}** education, "
                    f"**{result['experience_count']}** experience, "
                    f"**{result['projects_count']}** projects."
                )
                _render_parsed_results(result["parsed_resume"])

            else:
                st.error(
                    f"❌ Parsing failed: {result.get('error')}"
                )

        except Exception as exc:
            st.error(f"❌ Agent error: {str(exc)}")
            logger.error("Resume agent error: %s", exc)


def _render_parsed_results(parsed: dict) -> None:
    """Renders all parsed resume sections."""

    st.markdown("---")
    st.markdown(
        ""
        "📊 Parsed Resume Data",
        unsafe_allow_html=True
    )

    # ── Contact Info ─────────────────────────────────────────
    contact = parsed.get("contact_info", {})
    if any(contact.values()):
        st.markdown("### 👤 Contact Information")
        cols = st.columns(3)
        info_items = [
            ("Name",     contact.get("name")),
            ("Email",    contact.get("email")),
            ("Phone",    contact.get("phone")),
            ("Location", contact.get("location")),
            ("LinkedIn", contact.get("linkedin")),
            ("GitHub",   contact.get("github")),
        ]
        for i, (label, value) in enumerate(info_items):
            if value:
                with cols[i % 3]:
                    st.metric(label, value)

    # ── Professional Summary ─────────────────────────────────
    summary = parsed.get("summary")
    if summary:
        st.markdown("### 📝 Professional Summary")
        st.info(summary)

    # ── Skills ───────────────────────────────────────────────
    skills = parsed.get("skills", [])
    if skills:
        st.markdown(f"### 🛠️ Skills ({len(skills)} detected)")
        cols = st.columns(4)
        for i, skill in enumerate(skills):
            with cols[i % 4]:
                st.markdown(
                    f""
                    f"⚡ {skill}",
                    unsafe_allow_html=True
                )
        st.markdown("")

    # ── Education ────────────────────────────────────────────
    education = parsed.get("education", [])
    if education:
        st.markdown(f"### 🎓 Education ({len(education)})")
        for edu in education:
            with st.expander(
                f"🏛️ {edu.get('institution', 'Unknown')} "
                f"— {edu.get('degree', 'Degree')}",
                expanded=True
            ):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown(
                        f"**Field:** "
                        f"{edu.get('field_of_study', 'N/A')}"
                    )
                with col2:
                    st.markdown(
                        f"**Period:** "
                        f"{edu.get('start_year', '?')} - "
                        f"{edu.get('end_year', '?')}"
                    )
                with col3:
                    st.markdown(
                        f"**Grade:** "
                        f"{edu.get('grade', 'N/A')}"
                    )

    # ── Work Experience ──────────────────────────────────────
    experience = parsed.get("experience", [])
    if experience:
        st.markdown(
            f"### 💼 Work Experience ({len(experience)})"
        )
        for exp in experience:
            current = " 🟢 Current" if exp.get("is_current") else ""
            with st.expander(
                f"🏢 {exp.get('company', 'Company')} "
                f"— {exp.get('job_title', 'Role')}{current}",
                expanded=True
            ):
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(
                        f"**Period:** "
                        f"{exp.get('start_date', '?')} - "
                        f"{exp.get('end_date', '?')}"
                    )
                with col2:
                    st.markdown(
                        f"**Location:** "
                        f"{exp.get('location', 'N/A')}"
                    )

                desc = exp.get("description", [])
                if desc:
                    st.markdown("**Responsibilities:**")
                    for item in desc:
                        st.markdown(f"• {item}")

                techs = exp.get("technologies", [])
                if techs:
                    st.markdown(
                        "**Technologies:** " +
                        " | ".join(
                            [f"`{t}`" for t in techs]
                        )
                    )

    # ── Projects ─────────────────────────────────────────────
    projects = parsed.get("projects", [])
    if projects:
        st.markdown(f"### 🚀 Projects ({len(projects)})")
        for proj in projects:
            with st.expander(
                f"💡 {proj.get('name', 'Project')}",
                expanded=True
            ):
                desc = proj.get("description")
                if desc:
                    st.markdown(f"**Description:** {desc}")

                role = proj.get("role")
                if role:
                    st.markdown(f"**Role:** {role}")

                techs = proj.get("technologies", [])
                if techs:
                    st.markdown(
                        "**Technologies:** " +
                        " | ".join(
                            [f"`{t}`" for t in techs]
                        )
                    )

                highlights = proj.get("highlights", [])
                if highlights:
                    st.markdown("**Highlights:**")
                    for h in highlights:
                        st.markdown(f"• {h}")

    # ── Certifications ───────────────────────────────────────
    certs = parsed.get("certifications", [])
    if certs:
        st.markdown(
            f"### 🏆 Certifications ({len(certs)})"
        )
        for cert in certs:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(
                    f"**{cert.get('name', 'Certificate')}**"
                )
            with col2:
                st.markdown(
                    f"Issuer: {cert.get('issuer', 'N/A')}"
                )
            with col3:
                st.markdown(
                    f"Date: {cert.get('date', 'N/A')}"
                )

    # ── Languages ────────────────────────────────────────────
    languages = parsed.get("languages", [])
    if languages:
        st.markdown("### 🌐 Languages")
        st.markdown(
            " | ".join([f"**{lang}**" for lang in languages])
        )

    st.divider()

    # Re-parse button
    col1, col2 = st.columns(2)
    with col1:
        if st.button(
            "🔄  Re-parse Resume",
            width="stretch"
        ):
            st.session_state.pop("resume_parsed", None)
            st.session_state.pop("parsed_resume", None)
            st.rerun()

    with col2:
        if st.button(
            "➡️  Continue to ATS Analysis",
            type="primary",
            width="stretch"
        ):
            st.info(
                "Switch to the **ATS Analysis** tab above "
                "to see your ATS compatibility score."
            )