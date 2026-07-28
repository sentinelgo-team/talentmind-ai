"""
TalentMind AI - Main Application Entry Point
==============================================
Modern dark-themed multi-agent career platform.

Author  : TalentMind AI Team
Version : 2.0.0
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st

from app.core.constants import APP_NAME, APP_TAGLINE, APP_VERSION
from app.core.logging_config import setup_logging, get_logger
from app.core.settings import get_settings
from app.database.connection import db_manager
from app.database import models  # noqa: F401
from app.ui.theme import inject_custom_css

setup_logging()
logger = get_logger(__name__)


def initialize_application() -> bool:
    """Performs startup validation checks."""
    cfg = get_settings()

    if not cfg.validate_google_api_key():
        st.error(
            "**Google API Key Not Configured**\n\n"
            "Please add your `GOOGLE_API_KEY` to `.env` "
            "and restart the application."
        )
        return False

    if not db_manager.health_check():
        st.error("**Database Connection Failed**")
        return False

    db_manager.create_tables()
    return True


def configure_page() -> None:
    """Configures Streamlit page settings."""
    st.set_page_config(
        page_title=APP_NAME,
        page_icon="🧠",
        layout="wide",
        initial_sidebar_state="expanded",
    )


def render_sidebar() -> str:
    """Renders modern sidebar navigation."""
    with st.sidebar:
        st.markdown(
            f"""
            <div style="text-align: center; padding: 1rem 0;">
                <div style="font-size: 2rem;">🧠</div>
                <div class="gradient-text" style="font-size: 1.3rem;">
                    {APP_NAME}
                </div>
                <div style="font-size: 0.75rem; color: #8892A4; margin-top: 0.3rem;">
                    {APP_TAGLINE}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.session_state.get("resume_uploaded"):
            fname = st.session_state.get("resume_file_name", "")
            st.markdown(
                f"""
                <div style="background: rgba(72, 208, 160, 0.1);
                            border: 1px solid rgba(72, 208, 160, 0.3);
                            border-radius: 8px; padding: 0.6rem;
                            text-align: center; margin: 0.5rem 0;">
                    <span style="color: #48D0A0; font-size: 0.8rem;">
                        ✓ {fname}
                    </span>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown("---")

        page = st.radio(
            label="Navigation",
            options=[
                "🏠  Home",
                "📄  Upload Resume",
                "🔍  Analysis",
                "💼  Job Matching",
                "🎯  Interview Prep",
                "📊  Dashboard",
                "📑  Reports",
            ],
            label_visibility="collapsed"
        )

        st.markdown("---")
        st.markdown(
            f"""
            <div style="text-align: center; padding: 0.5rem 0;">
                <span style="color: #5A6478; font-size: 0.7rem;">
                    v{APP_VERSION} | Powered by Gemini AI
                </span>
            </div>
            """,
            unsafe_allow_html=True
        )

    return page


def render_home() -> None:
    """Renders modern home page."""

    # Hero Section
    st.markdown(
        f"""
        <div class="hero-section">
            <div class="hero-title">{APP_NAME}</div>
            <div class="hero-subtitle">
                Multi-Agent AI Platform for Intelligent Recruitment & Career Guidance.
                Upload your resume and let 11 specialized AI agents analyze every aspect of your career profile.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Stats pills
    st.markdown(
        """
        <div style="text-align: center; margin-bottom: 2rem;">
            <span class="stat-pill">
                <span class="stat-pill-number">11</span>
                <span class="stat-pill-label">AI Agents</span>
            </span>
            <span class="stat-pill">
                <span class="stat-pill-number">50+</span>
                <span class="stat-pill-label">Metrics Analyzed</span>
            </span>
            <span class="stat-pill">
                <span class="stat-pill-number">PDF</span>
                <span class="stat-pill-label">Report Export</span>
            </span>
            <span class="stat-pill">
                <span class="stat-pill-number">Any</span>
                <span class="stat-pill-label">Industry/Role</span>
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Feature Cards
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon">📄</div>
                <div class="feature-title">Resume Intelligence</div>
                <div class="feature-desc">
                    AI-powered parsing with ATS scoring and keyword optimization
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon">🎯</div>
                <div class="feature-title">Skill Gap Analysis</div>
                <div class="feature-desc">
                    Dynamic benchmarks for any role with personalized learning roadmaps
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon">💼</div>
                <div class="feature-title">Job Matching</div>
                <div class="feature-desc">
                    AI-matched career paths with salary insights and fit scores
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col4:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon">🎤</div>
                <div class="feature-title">Interview Prep</div>
                <div class="feature-desc">
                    Role-specific questions with hints and sample answers
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # How it works
    st.markdown(
        '<div class="section-header">How It Works</div>',
        unsafe_allow_html=True
    )

    steps = [
        ("Upload", "Drop your resume (PDF, DOCX, or TXT)"),
        ("AI Analysis", "11 specialized agents process your profile"),
        ("Insights", "Get ATS score, skill gaps, and career matches"),
        ("Action Plan", "Follow your personalized learning roadmap"),
    ]

    cols = st.columns(4)
    for i, (title, desc) in enumerate(steps):
        with cols[i]:
            st.markdown(
                f"""
                <div class="glass-card" style="text-align: center;">
                    <div class="step-number" style="margin: 0 auto 0.8rem auto;">{i + 1}</div>
                    <div class="feature-title">{title}</div>
                    <div class="feature-desc">{desc}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown("<br>", unsafe_allow_html=True)

    # CTA
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button(
            "🚀  Get Started — Upload Your Resume",
            type="primary",
            use_container_width=True,
        ):
            st.session_state["nav_to_upload"] = True
            st.rerun()


def main() -> None:
    """Main application entry point."""
    configure_page()
    inject_custom_css()

    if "initialized" not in st.session_state:
        with st.spinner("Initializing TalentMind AI..."):
            success = initialize_application()
            st.session_state["initialized"] = success

    if not st.session_state.get("initialized"):
        st.stop()

    page = render_sidebar()

    # ── Page Routing ─────────────────────────────────────────
    if "Home" in page:
        render_home()

    elif "Upload" in page:
        from app.ui.pages.upload import render_upload_page
        render_upload_page()

    elif "Analysis" in page:
        tab1, tab2, tab3, tab4 = st.tabs([
            "📄  Resume Parsing",
            "📊  ATS Analysis",
            "🛠️  Skill Analysis",
            "🗺️  Skill Gap",
        ])
        with tab1:
            from app.ui.pages.analysis import render_analysis_page
            render_analysis_page()
        with tab2:
            from app.ui.pages.ats import render_ats_page
            render_ats_page()
        with tab3:
            from app.ui.pages.skills import render_skills_page
            render_skills_page()
        with tab4:
            from app.ui.pages.skill_gap import render_skill_gap_page
            render_skill_gap_page()

    elif "Job Matching" in page:
        from app.ui.pages.job_matching import job_matching_page
        job_matching_page()

    elif "Interview" in page:
        from app.ui.pages.interview import interview_page
        interview_page()

    elif "Dashboard" in page:
        from app.ui.pages.dashboard import dashboard_page
        dashboard_page()

    elif "Reports" in page:
        from app.ui.pages.reports import reports_page
        reports_page()


if __name__ == "__main__":
    main()
