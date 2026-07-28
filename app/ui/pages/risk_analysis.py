"""
TalentMind AI - Risk Analysis Page
====================================
Displays career risk assessment results.

Author  : TalentMind AI Team
Version : 1.0.0
"""

from __future__ import annotations

import streamlit as st


def risk_analysis_page() -> None:
    """Renders the risk analysis page."""
    st.title("⚠️ Career Risk Assessment")
    st.markdown(
        "Evaluate career transition risks, market stability, "
        "and automation threats — with actionable mitigation strategies."
    )
    st.caption(
        "Unlike Skill Gap Analysis (which shows missing skills), "
        "this page assesses broader career risks: market trends, "
        "role stability, and transition challenges."
    )

    if "resume_text" not in st.session_state:
        st.warning(
            "Please upload a resume first from the "
            "**Upload Resume** page."
        )
        return

    risk_result = st.session_state.get("risk_result") or {}

    if not risk_result.get("success"):
        st.info(
            "Risk analysis has not been run yet. "
            "Click **Run Full Analysis** on the Upload page, "
            "or run it individually below."
        )
        if st.button("🔍 Run Risk Analysis", type="primary"):
            _run_risk_analysis()
        return

    # Display results
    _render_risk_results(risk_result)


def _run_risk_analysis() -> None:
    """Run risk analysis agent."""
    from app.agents.risk_agent import RiskAnalysisAgent

    with st.spinner("Analyzing career risks..."):
        try:
            agent = RiskAnalysisAgent()
            result = agent.run({
                "skill_analysis_result": (
                    st.session_state.get("skill_result") or {}
                ),
                "skill_gap_result": (
                    st.session_state.get("skill_gap_result") or {}
                ),
                "target_role": st.session_state.get(
                    "target_role", "General Technology Role"
                ),
                "experience_level": "mid",
                "experience_years": 0,
            })

            if result.get("success"):
                st.session_state["risk_result"] = result
                st.success("Risk analysis complete!")
                st.rerun()
            else:
                st.error(
                    f"Risk analysis failed: "
                    f"{result.get('error')}"
                )
        except Exception as exc:
            st.error(f"Error: {exc}")


def _render_risk_results(data: dict) -> None:
    """Render risk analysis results."""
    st.divider()

    # Key metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        level = data.get("overall_risk_level", "N/A")
        color = {
            "LOW": "green", "MEDIUM": "orange",
            "HIGH": "red", "CRITICAL": "red"
        }.get(level, "gray")
        st.metric("Overall Risk Level", level)
    with col2:
        st.metric(
            "Risk Score",
            f"{data.get('overall_risk_score', 0)}/100"
        )
    with col3:
        st.metric(
            "Career Stability",
            f"{data.get('career_stability_score', 0)}/100"
        )

    # Risk categories
    categories = data.get("risk_categories") or []
    if categories:
        st.subheader("Risk Categories")
        for cat in categories:
            if isinstance(cat, dict):
                with st.expander(
                    f"{cat.get('category', 'Unknown')} "
                    f"— {cat.get('risk_level', 'N/A')}",
                    expanded=False
                ):
                    st.write(cat.get("description", ""))
                    mitigation = cat.get("mitigation", "")
                    if mitigation:
                        st.success(
                            f"**Mitigation:** {mitigation}"
                        )

    # Market outlook
    outlook = data.get("market_outlook") or {}
    if outlook:
        st.subheader("Market Outlook")
        o_col1, o_col2, o_col3, o_col4 = st.columns(4)
        with o_col1:
            st.metric(
                "Demand", outlook.get("demand_trend", "N/A")
            )
        with o_col2:
            st.metric(
                "Salary",
                outlook.get("salary_stability", "N/A")
            )
        with o_col3:
            st.metric(
                "Remote Work",
                outlook.get("remote_work_availability", "N/A")
            )
        with o_col4:
            st.metric(
                "Industry",
                outlook.get("industry_health", "N/A")
            )

    # Mitigation plan
    mitigation_plan = data.get("mitigation_plan") or []
    if mitigation_plan:
        st.subheader("Mitigation Plan")
        for item in mitigation_plan:
            if isinstance(item, dict):
                st.markdown(
                    f"- **[{item.get('priority', '')}]** "
                    f"{item.get('action', '')} "
                    f"— _{item.get('timeline', '')}_"
                )

    # Summary
    summary = data.get("summary", "")
    if summary:
        st.divider()
        st.info(f"**Summary:** {summary}")
