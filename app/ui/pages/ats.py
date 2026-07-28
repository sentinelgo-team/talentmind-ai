"""
TalentMind AI - ATS Analysis Page
====================================
Displays ATS compatibility scores and
improvement suggestions with visualizations.

Author  : TalentMind AI Team
Version : 1.0.0
"""

from __future__ import annotations

import logging

import plotly.graph_objects as go
import streamlit as st

from app.agents.ats_agent import ATSAgent

logger = logging.getLogger(__name__)


def render_ats_page() -> None:
    """Renders the ATS Analysis page."""

    st.markdown(
        ""
        "📊 ATS Analysis",
        unsafe_allow_html=True
    )
    st.markdown(
        ""
        "Check your resume ATS compatibility score "
        "and get improvement suggestions.",
        unsafe_allow_html=True
    )
    st.divider()

    # Check resume uploaded
    if not st.session_state.get("resume_uploaded"):
        st.warning(
            "⚠️  Please upload your resume first "
            "from the **Upload Resume** page."
        )
        return

    # Show if already analyzed
    if st.session_state.get("ats_analyzed"):
        _render_ats_results(
            st.session_state["ats_result"]
        )
        return

    # Target role input
    st.markdown("### 🎯 Target Job Role (Optional)")
    target_role = st.text_input(
        label="Enter the job role you are applying for",
        placeholder="e.g. Cybersecurity Analyst, Python Developer",
        help="Providing a target role improves keyword analysis"
    )

    col1, col2 = st.columns([2, 1])
    with col1:
        st.info(
            f"📄 Resume: "
            f"**{st.session_state.get('resume_file_name')}** "
            f"({st.session_state.get('char_count', 0):,} chars)"
        )
    with col2:
        analyze_btn = st.button(
            "🔍  Analyze ATS Score",
            type="primary",
            width="stretch"
        )

    if analyze_btn:
        _run_ats_agent(
            resume_text = st.session_state.get(
                "resume_text", ""
            ),
            target_role = target_role.strip()
                          if target_role
                          else "Cybersecurity Analyst",
        )


def _run_ats_agent(
    resume_text: str,
    target_role: str
) -> None:
    """Runs ATS Agent with progress feedback."""

    with st.spinner(
        "🔍 ATS Agent analyzing compatibility..."
    ):
        try:
            agent  = ATSAgent()
            result = agent.run({
                "resume_text": resume_text,
                "target_role": target_role,
            })

            if result["success"]:
                st.session_state["ats_analyzed"] = True
                st.session_state["ats_result"]   = result

                score = result["ats_score"]
                label = result["score_label"]
                st.success(
                    f"✅ ATS Analysis Complete! "
                    f"Score: **{score:.0f}/100** — {label}"
                )
                _render_ats_results(result)
            else:
                st.error(
                    f"❌ ATS Analysis failed: "
                    f"{result.get('error')}"
                )

        except Exception as exc:
            st.error(f"❌ Error: {str(exc)}")
            logger.error("ATS page error: %s", exc)


def _render_ats_results(result: dict) -> None:
    """Renders complete ATS analysis results."""

    st.markdown("---")

    # ── Score Overview ───────────────────────────────────────
    st.markdown(
        ""
        "📊 ATS Score Report",
        unsafe_allow_html=True
    )

    overall_score = result.get("ats_score", 0)
    score_label   = result.get("score_label", "")

    # Score color
    if overall_score >= 85:
        score_color = "#059669"
    elif overall_score >= 70:
        score_color = "#2563EB"
    elif overall_score >= 50:
        score_color = "#D97706"
    else:
        score_color = "#DC2626"

    # Main score display
    st.markdown(
        f""
        f""
        f"{overall_score:.0f}"
        f""
        f"out of 100"
        f""
        f"{score_label}"
        f""
        f"Target Role: {result.get('target_role', 'N/A')}"
        f"",
        unsafe_allow_html=True
    )

    st.markdown("")

    # ── Score Breakdown ──────────────────────────────────────
    breakdown = result.get("score_breakdown", {})
    if breakdown:
        st.markdown("### 📈 Score Breakdown")

        cols = st.columns(5)
        score_items = [
            ("🔑 Keywords",     "keyword_score",      "#2563EB"),
            ("📋 Format",       "format_score",       "#7C3AED"),
            ("✍️ Grammar",      "grammar_score",      "#059669"),
            ("✅ Completeness", "completeness_score", "#D97706"),
            ("📖 Readability",  "readability_score",  "#DC2626"),
        ]

        for i, (label, key, color) in enumerate(score_items):
            score = breakdown.get(key, 0)
            with cols[i]:
                st.markdown(
                    f""
                    f""
                    f"{score:.0f}"
                    f""
                    f"{label}"
                    f"",
                    unsafe_allow_html=True
                )

        # Radar Chart
        st.markdown("")
        _render_radar_chart(breakdown)

    # ── Keyword Analysis ─────────────────────────────────────
    keyword = result.get("keyword_analysis", {})
    if keyword:
        st.markdown("### 🔑 Keyword Analysis")

        col1, col2 = st.columns(2)
        with col1:
            found = keyword.get("found_keywords", [])
            st.markdown(
                f"**✅ Keywords Found ({len(found)})**"
            )
            if found:
                kw_html = " ".join([
                    f""
                    f"✓ {kw}"
                    for kw in found
                ])
                st.markdown(kw_html, unsafe_allow_html=True)
            else:
                st.markdown("*No keywords detected*")

        with col2:
            missing = keyword.get("missing_keywords", [])
            st.markdown(
                f"**❌ Missing Keywords ({len(missing)})**"
            )
            if missing:
                kw_html = " ".join([
                    f""
                    f"✗ {kw}"
                    for kw in missing
                ])
                st.markdown(kw_html, unsafe_allow_html=True)
            else:
                st.markdown("*No missing keywords*")

        comment = keyword.get("keyword_comments", "")
        if comment:
            st.info(f"💡 {comment}")

    # ── Format Analysis ──────────────────────────────────────
    fmt = result.get("format_analysis", {})
    if fmt:
        st.markdown("### 📋 Format & Structure Analysis")

        sections = [
            ("Contact Info",   "has_contact_info"),
            ("Summary",        "has_summary"),
            ("Experience",     "has_experience"),
            ("Education",      "has_education"),
            ("Skills",         "has_skills"),
            ("Projects",       "has_projects"),
            ("Certifications", "has_certifications"),
        ]

        cols = st.columns(4)
        for i, (label, key) in enumerate(sections):
            present = fmt.get(key, False)
            icon    = "✅" if present else "❌"
            bg      = "#D1FAE5" if present else "#FEE2E2"
            color   = "#065F46" if present else "#991B1B"
            with cols[i % 4]:
                st.markdown(
                    f""
                    f"{icon} {label}",
                    unsafe_allow_html=True
                )

        # Format issues and strengths
        issues    = fmt.get("format_issues", [])
        strengths = fmt.get("format_strengths", [])

        if issues or strengths:
            col1, col2 = st.columns(2)
            with col1:
                if strengths:
                    st.markdown("**✅ Format Strengths:**")
                    for s in strengths:
                        st.markdown(f"• {s}")
            with col2:
                if issues:
                    st.markdown("**⚠️ Format Issues:**")
                    for issue in issues:
                        st.markdown(f"• {issue}")

    # ── Strengths & Weaknesses ───────────────────────────────
    col1, col2 = st.columns(2)

    strengths  = result.get("strengths", [])
    weaknesses = result.get("weaknesses", [])

    with col1:
        if strengths:
            st.markdown("### 💪 Resume Strengths")
            for s in strengths:
                st.success(f"✅  {s}")

    with col2:
        if weaknesses:
            st.markdown("### ⚠️ Areas to Improve")
            for w in weaknesses:
                st.warning(f"⚠️  {w}")

    # ── Priority Improvements ────────────────────────────────
    priorities = result.get("improvement_priority", [])
    if priorities:
        st.markdown("### 🎯 Priority Action Items")

        priority_colors = {
            "HIGH"   : ("#FEE2E2", "#DC2626", "🔴"),
            "MEDIUM" : ("#FEF3C7", "#D97706", "🟡"),
            "LOW"    : ("#D1FAE5", "#059669", "🟢"),
        }

        for item in priorities:
            level  = item.get("priority", "LOW").upper()
            action = item.get("action", "")
            impact = item.get("impact", "")
            bg, color, icon = priority_colors.get(
                level, ("#F1F5F9", "#64748B", "⚪")
            )

            st.markdown(
                f""
                f""
                f"{icon} {level} PRIORITY"
                f""
                f"Action: {action}"
                f""
                f"Impact: {impact}"
                f"",
                unsafe_allow_html=True
            )

    # ── ATS Suggestions ──────────────────────────────────────
    suggestions = result.get("ats_suggestions", [])
    if suggestions:
        st.markdown("### 💡 ATS Improvement Suggestions")
        for i, suggestion in enumerate(suggestions, 1):
            st.markdown(
                f""
                f"{i}. "
                f"{suggestion}"
                f"",
                unsafe_allow_html=True
            )

    st.divider()

    # Action buttons
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button(
            "🔄  Re-analyze",
            width="stretch"
        ):
            st.session_state.pop("ats_analyzed", None)
            st.session_state.pop("ats_result", None)
            st.rerun()
    with col2:
        if st.button(
            "➡️  Skill Analysis",
            type="primary",
            width="stretch"
        ):
            st.info("Switch to the **Skill Analysis** tab above.")
    with col3:
        if st.button(
            "📄  Download Report",
            width="stretch"
        ):
            st.info("Navigate to **Reports** from the sidebar.")


def _render_radar_chart(breakdown: dict) -> None:
    """Renders a radar chart for score breakdown."""

    categories = [
        "Keywords", "Format",
        "Grammar", "Completeness", "Readability"
    ]
    values = [
        breakdown.get("keyword_score",      0),
        breakdown.get("format_score",        0),
        breakdown.get("grammar_score",       0),
        breakdown.get("completeness_score",  0),
        breakdown.get("readability_score",   0),
    ]

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r     = values + [values[0]],
        theta = categories + [categories[0]],
        fill  = "toself",
        name  = "ATS Scores",
        line  = dict(color="#2563EB", width=2),
        fillcolor="rgba(37, 99, 235, 0.15)",
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickfont=dict(size=10),
                gridcolor="#E2E8F0",
            ),
            angularaxis=dict(
                tickfont=dict(size=12),
                gridcolor="#E2E8F0",
            ),
            bgcolor="#F8FAFC",
        ),
        showlegend=False,
        paper_bgcolor="white",
        height=380,
        margin=dict(t=40, b=40, l=60, r=60),
        title=dict(
            text="ATS Score Radar",
            x=0.5,
            font=dict(size=14, color="#1E293B")
        ),
    )

    st.plotly_chart(fig, width="stretch")