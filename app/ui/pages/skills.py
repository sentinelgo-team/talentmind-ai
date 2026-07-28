"""
TalentMind AI - Skill Analysis Page
======================================
Displays skill detection, classification,
proficiency levels, and industry comparison.

Author  : TalentMind AI Team
Version : 1.0.0
"""

from __future__ import annotations

import logging

import plotly.graph_objects as go
import plotly.express as px
import streamlit as st

from app.agents.skill_agent import SkillAnalysisAgent

logger = logging.getLogger(__name__)

# Proficiency colors
PROFICIENCY_COLORS = {
    "Expert"      : "#059669",
    "Advanced"    : "#2563EB",
    "Intermediate": "#D97706",
    "Beginner"    : "#DC2626",
}

# Category colors
CATEGORY_COLORS = [
    "#2563EB","#7C3AED","#059669","#D97706",
    "#DC2626","#0891B2","#DB2777","#65A30D",
]


def render_skills_page() -> None:
    """Renders the Skill Analysis page."""

    st.markdown(
        ""
        "🛠️ Skill Analysis",
        unsafe_allow_html=True
    )
    st.markdown(
        ""
        "Comprehensive skill detection, classification, "
        "and industry benchmarking.",
        unsafe_allow_html=True
    )
    st.divider()

    if not st.session_state.get("resume_uploaded"):
        st.warning(
            "⚠️  Please upload your resume first."
        )
        return

    if st.session_state.get("skills_analyzed"):
        _render_skill_results(
            st.session_state["skill_result"]
        )
        return

    # Target role input
    target_role = st.text_input(
        "🎯 Target Role",
        placeholder="e.g. Cybersecurity Analyst",
        value=st.session_state.get(
            "target_role", "Cybersecurity Analyst"
        )
    )

    col1, col2 = st.columns([2, 1])
    with col1:
        st.info(
            f"📄 Resume: "
            f"**{st.session_state.get('resume_file_name')}**"
        )
    with col2:
        analyze_btn = st.button(
            "🔍  Analyze Skills",
            type="primary",
            width="stretch"
        )

    if analyze_btn:
        _run_skill_agent(
            resume_text = st.session_state.get(
                "resume_text", ""
            ),
            target_role = target_role.strip()
                          if target_role
                          else "Cybersecurity Analyst",
        )


def _run_skill_agent(
    resume_text: str,
    target_role: str
) -> None:
    """Runs Skill Agent and displays results."""

    with st.spinner(
        "🔍 Skill Agent analyzing your skills..."
    ):
        try:
            agent  = SkillAnalysisAgent()
            result = agent.run({
                "resume_text": resume_text,
                "target_role": target_role,
            })

            if result["success"]:
                st.session_state["skills_analyzed"] = True
                st.session_state["skill_result"]    = result
                st.session_state["target_role"]     = target_role
                st.session_state["skill_gaps"]      = result.get(
                    "skill_gaps", []
                )

                total = result.get("total_skills_count", 0)
                score = result.get(
                    "skill_scores", {}
                ).get("overall_score", 0)

                st.success(
                    f"✅ Skill Analysis Complete! "
                    f"Found **{total}** skills. "
                    f"Overall Score: **{score}/100**"
                )
                _render_skill_results(result)
            else:
                st.error(
                    f"❌ Failed: {result.get('error')}"
                )

        except Exception as exc:
            st.error(f"❌ Error: {str(exc)}")
            logger.error("Skill page error: %s", exc)


def _render_skill_results(result: dict) -> None:
    """Renders all skill analysis sections."""

    st.markdown("---")

    # ── Score Overview ───────────────────────────────────────
    scores = result.get("skill_scores", {})
    if scores:
        st.markdown(
            ""
            "📊 Skill Scores",
            unsafe_allow_html=True
        )

        col1, col2, col3, col4 = st.columns(4)
        score_items = [
            (col1, "Technical",  "technical_score",  "#2563EB"),
            (col2, "Diversity",  "diversity_score",  "#7C3AED"),
            (col3, "Relevance",  "relevance_score",  "#059669"),
            (col4, "Overall",    "overall_score",    "#D97706"),
        ]

        for col, label, key, color in score_items:
            score = scores.get(key, 0)
            with col:
                st.markdown(
                    f""
                    f"{score}"
                    f""
                    f"{label}"
                    f"",
                    unsafe_allow_html=True
                )

    # ── Industry Comparison ──────────────────────────────────
    industry = result.get("industry_comparison", {})
    if industry:
        st.markdown("### 🏭 Industry Comparison")

        match_pct = industry.get("match_percentage", 0)
        comment   = industry.get("comparison_comment", "")

        col1, col2 = st.columns([1, 2])
        with col1:
            # Match percentage gauge
            color = (
                "#059669" if match_pct >= 70
                else "#D97706" if match_pct >= 50
                else "#DC2626"
            )
            st.markdown(
                f""
                f""
                f"{match_pct}%"
                f""
                f"Role Match"
                f"",
                unsafe_allow_html=True
            )

        with col2:
            if comment:
                st.info(f"💡 {comment}")

            have    = industry.get("candidate_has", [])
            missing = industry.get("candidate_missing", [])

            if have:
                st.markdown("**✅ You Have:**")
                st.markdown(
                    " ".join([
                        f"`{s}`" for s in have
                    ])
                )
            if missing:
                st.markdown("**❌ You Need:**")
                st.markdown(
                    " ".join([
                        f"`{s}`" for s in missing
                    ])
                )

    # ── Top Skills ───────────────────────────────────────────
    top_skills = result.get("top_skills", [])
    if top_skills:
        st.markdown("### ⭐ Top Skills")
        cols = st.columns(min(len(top_skills), 5))
        for i, skill in enumerate(top_skills[:5]):
            with cols[i % 5]:
                st.markdown(
                    f""
                    f"⭐ {skill}"
                    f"",
                    unsafe_allow_html=True
                )

    # ── Skill Categories ─────────────────────────────────────
    categories = result.get("skill_categories", {})
    if categories:
        st.markdown("### 📂 Skills by Category")

        non_empty = {
            k: v for k, v in categories.items()
            if v
        }

        if non_empty:
            # Bar chart
            cat_names  = list(non_empty.keys())
            cat_counts = [len(v) for v in non_empty.values()]

            fig = go.Figure(go.Bar(
                x             = cat_counts,
                y             = cat_names,
                orientation   = "h",
                marker_color  = CATEGORY_COLORS[:len(cat_names)],
                text          = cat_counts,
                textposition  = "outside",
            ))
            fig.update_layout(
                height        = max(300, len(cat_names) * 45),
                margin        = dict(l=10, r=40, t=20, b=10),
                paper_bgcolor = "white",
                plot_bgcolor  = "#F8FAFC",
                xaxis=dict(
                    title="Number of Skills",
                    gridcolor="#E2E8F0"
                ),
                yaxis=dict(automargin=True),
            )
            st.plotly_chart(fig, width="stretch")

            # Skill tags per category
            for cat, skills in non_empty.items():
                with st.expander(
                    f"📁 {cat}  ({len(skills)} skills)",
                    expanded=False
                ):
                    tags_html = " ".join([
                        f""
                        f"⚡ {s}"
                        for s in skills
                    ])
                    st.markdown(
                        tags_html, unsafe_allow_html=True
                    )
                    st.markdown("")

    # ── Proficiency Breakdown ────────────────────────────────
    proficiency = result.get("proficiency_summary", {})
    if proficiency:
        st.markdown("### 📊 Proficiency Levels")

        non_empty_prof = {
            k: v for k, v in proficiency.items() if v
        }

        if non_empty_prof:
            col1, col2 = st.columns([1, 1])

            with col1:
                # Pie chart
                labels = list(non_empty_prof.keys())
                values = [len(v) for v in non_empty_prof.values()]
                colors = [
                    PROFICIENCY_COLORS.get(l, "#64748B")
                    for l in labels
                ]

                fig = go.Figure(go.Pie(
                    labels    = labels,
                    values    = values,
                    marker    = dict(colors=colors),
                    hole      = 0.4,
                    textinfo  = "label+value",
                ))
                fig.update_layout(
                    height        = 300,
                    margin        = dict(t=20,b=20,l=20,r=20),
                    paper_bgcolor = "white",
                    showlegend    = True,
                )
                st.plotly_chart(fig, width="stretch")

            with col2:
                # Proficiency list
                for level, skills in non_empty_prof.items():
                    color = PROFICIENCY_COLORS.get(
                        level, "#64748B"
                    )
                    st.markdown(
                        f""
                        f""
                        f"{level} ({len(skills)})"
                        f""
                        f"{', '.join(skills[:5])}"
                        f"{'...' if len(skills)>5 else ''}"
                        f"",
                        unsafe_allow_html=True
                    )

    # ── Skill Gaps ───────────────────────────────────────────
    gaps = result.get("skill_gaps", [])
    if gaps:
        st.markdown("### ⚠️ Skill Gaps Detected")
        st.markdown(
            f""
            f"These skills are needed for "
            f"{result.get('target_role')} "
            f"but missing from your resume.",
            unsafe_allow_html=True
        )
        cols = st.columns(4)
        for i, gap in enumerate(gaps):
            with cols[i % 4]:
                st.markdown(
                    f""
                    f"❌ {gap}",
                    unsafe_allow_html=True
                )
        st.markdown("")

    # ── Recommendations ──────────────────────────────────────
    recs = result.get("recommendations", [])
    if recs:
        st.markdown("### 💡 Skill Recommendations")
        for i, rec in enumerate(recs, 1):
            st.markdown(
                f""
                f"{i}. "
                f"{rec}",
                unsafe_allow_html=True
            )

    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        if st.button(
            "🔄  Re-analyze Skills",
            width="stretch"
        ):
            st.session_state.pop("skills_analyzed", None)
            st.session_state.pop("skill_result", None)
            st.rerun()
    with col2:
        if st.button(
            "➡️  View Skill Gap Analysis",
            type="primary",
            width="stretch"
        ):
            st.info("Switch to the **Skill Gap** tab above.")