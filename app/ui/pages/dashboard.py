"""
TalentMind AI - Dashboard Page
==============================

Analytics dashboard for visualizing resume analysis results, skill gaps, 
career progress, and job market insights.

Author  : TalentMind AI Team
Version : 1.0.0
"""

from __future__ import annotations

import streamlit as st
from typing import Any, Dict, List
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta

def dashboard_page() -> None:
    """Renders the analytics dashboard page."""
    from app.ui.theme import render_metric_card

    st.markdown(
        '<div class="section-header" style="font-size: 1.6rem; border: none;">'
        '📊 Career Dashboard</div>',
        unsafe_allow_html=True
    )

    if "resume_text" not in st.session_state or not st.session_state.resume_text:
        st.warning("Please upload a resume first to see your dashboard.")
        return

    user_data = _get_user_dashboard_data()

    # Key metrics with modern cards
    cols = st.columns(4)
    ats = user_data.get('ats_score', 0)
    match = user_data.get('skill_match_percentage', 0)
    skills_count = user_data.get('total_skills', 0)
    jobs = user_data.get('job_matches_count', 0)

    with cols[0]:
        st.markdown(render_metric_card("ATS Score", f"{ats:.0f}/100"), unsafe_allow_html=True)
    with cols[1]:
        st.markdown(render_metric_card("Skills Match", f"{match:.0f}%"), unsafe_allow_html=True)
    with cols[2]:
        st.markdown(render_metric_card("Skills Found", str(skills_count)), unsafe_allow_html=True)
    with cols[3]:
        st.markdown(render_metric_card("Job Matches", str(jobs)), unsafe_allow_html=True)
    
    st.divider()
    
    st.markdown("<br>", unsafe_allow_html=True)

    # Charts section
    chart_col1, chart_col2 = st.columns(2)

    dark_layout = dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#E0E0E0"),
        margin=dict(t=40, b=20, l=20, r=20),
    )

    with chart_col1:
        st.markdown('<div class="section-header">Skills Distribution</div>', unsafe_allow_html=True)
        skills_data = user_data.get('skills_distribution', {})
        if skills_data:
            df_skills = pd.DataFrame(list(skills_data.items()), columns=['Category', 'Count'])
            fig_skills = px.pie(
                df_skills, values='Count', names='Category', hole=0.5,
                color_discrete_sequence=["#6C63FF", "#48B8D0", "#48D0A0", "#FFB74D", "#FF6B6B", "#B388FF"]
            )
            fig_skills.update_traces(textposition='inside', textinfo='percent+label')
            fig_skills.update_layout(**dark_layout)
            st.plotly_chart(fig_skills, use_container_width=True)
        else:
            st.info("Run skill analysis to see distribution.")

    with chart_col2:
        st.markdown('<div class="section-header">Skill Proficiency</div>', unsafe_allow_html=True)
        proficiency_data = user_data.get('skill_proficiency', {})
        if proficiency_data:
            skills = list(proficiency_data.keys())[:6]
            scores = list(proficiency_data.values())[:6]

            fig_radar = go.Figure()
            fig_radar.add_trace(go.Scatterpolar(
                r=scores, theta=skills, fill='toself',
                fillcolor='rgba(108, 99, 255, 0.2)',
                line=dict(color='#6C63FF', width=2),
            ))
            fig_radar.update_layout(
                polar=dict(
                    bgcolor="rgba(0,0,0,0)",
                    radialaxis=dict(visible=True, range=[0, 100], color="#5A6478"),
                    angularaxis=dict(color="#8892A4"),
                ),
                showlegend=False,
                **dark_layout
            )
            st.plotly_chart(fig_radar, use_container_width=True)
        else:
            st.info("Run skill analysis to see proficiency.")
    
    # Skill gap analysis section
    st.markdown('<div class="section-header">Skill Gap Analysis</div>', unsafe_allow_html=True)
    gap_col1, gap_col2 = st.columns([2, 1])

    with gap_col1:
        skill_gaps = user_data.get('skill_gaps', [])
        if skill_gaps:
            gap_data = []
            for gap in skill_gaps[:5]:
                gap_data.append({
                    'Skill': gap.get('skill', 'Unknown'),
                    'Gap Level': gap.get('gap_level', 'Medium'),
                    'Priority': gap.get('priority', 'Medium')
                })
            
            if gap_data:
                df_gaps = pd.DataFrame(gap_data)
                # Color code by priority
                color_map = {'High': '#ff4444', 'Medium': '#ffaa00', 'Low': '#00C851'}
                fig_gaps = px.bar(
                    df_gaps,
                    x='Skill',
                    y='Gap Level',
                    color='Priority',
                    color_discrete_map=color_map,
                    title="Top Skill Gaps to Address"
                )
                fig_gaps.update_layout(xaxis_tickangle=-45)
                st.plotly_chart(fig_gaps, width="stretch")
        else:
            st.info("Skill gap analysis will appear after completing skill gap assessment.")
    
    with gap_col2:
        # Learning progress
        st.subheader("📚 Learning Progress")
        learning_data = user_data.get('learning_progress', {})
        if learning_data:
            completed = learning_data.get('completed_courses', 0)
            total = learning_data.get('total_courses', 0)
            progress_pct = (completed / total * 100) if total > 0 else 0
            
            st.metric("Courses Completed", f"{completed}/{total}")
            st.progress(progress_pct / 100)
            
            # Next recommended course
            next_course = learning_data.get('next_course', 'Complete skill assessment to get recommendations')
            st.info(f"**Next Recommendation:** {next_course}")
        else:
            st.info("Learning recommendations will appear after skill gap analysis.")
    
    # Job market insights
    st.subheader("💼 Job Market Insights")
    market_col1, market_col2 = st.columns(2)
    
    with market_col1:
        # Job demand trend
        st.write("**Demand for Your Skills**")
        demand_data = user_data.get('job_demand_trend', {})
        if demand_data:
            dates = list(demand_data.keys())
            demand_values = list(demand_data.values())
            
            fig_demand = px.line(
                x=dates, 
                y=demand_values,
                title="Job Demand Trend (Last 6 Months)",
                labels={'x': 'Month', 'y': 'Job Postings'}
            )
            st.plotly_chart(fig_demand, width="stretch")
        else:
            st.info("Job demand data will appear after job matching analysis.")
    
    with market_col2:
        # Salary trends
        st.write("**Salary Trends**")
        salary_data = user_data.get('salary_trends', {})
        if salary_data:
            roles = list(salary_data.keys())
            salaries = list(salary_data.values())
            
            fig_salary = px.bar(
                x=roles,
                y=salaries,
                title="Average Salary by Related Role",
                labels={'x': 'Job Role', 'y': 'Average Salary (USD)'}
            )
            fig_salary.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig_salary, width="stretch")
        else:
            st.info("Salary data will appear after job matching analysis.")
    
    # Recommendations section
    st.markdown("---")
    st.markdown('<div class="section-header">Recommended Next Steps</div>', unsafe_allow_html=True)

    recommendations = user_data.get('recommendations', [
        "Run full analysis from the Upload page for complete insights",
        "Try Skill Gap analysis for your target role",
        "Generate a PDF report to share with recruiters",
    ])

    rec_cols = st.columns(len(recommendations[:3]))
    icons = ["🎯", "📈", "📄"]
    for i, rec in enumerate(recommendations[:3]):
        with rec_cols[i]:
            st.markdown(
                f"""
                <div class="glass-card" style="text-align: center; min-height: 100px;
                     display: flex; flex-direction: column; justify-content: center;">
                    <div style="font-size: 1.5rem;">{icons[i % 3]}</div>
                    <div style="font-size: 0.85rem; color: #B8B0FF; margin-top: 0.5rem;">
                        {rec}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )


def _get_user_dashboard_data() -> Dict[str, Any]:
    """
    Extract and process user data from session state for dashboard visualization.
    Pulls from actual analysis results stored by the orchestrator.
    """
    ats_result = st.session_state.get("ats_result") or {}
    skill_result = st.session_state.get("skill_result") or {}
    skill_gap_result = st.session_state.get("skill_gap_result") or {}
    job_matching_result = st.session_state.get("job_matching_result") or {}
    recommendation_result = st.session_state.get("recommendation_result") or {}
    ranking_result = st.session_state.get("ranking_result") or {}

    # Extract skills distribution from skill analysis
    skills_distribution = {}
    skill_categories = skill_result.get("skill_categories") or {}
    if isinstance(skill_categories, dict):
        for cat, skills in skill_categories.items():
            if isinstance(skills, list):
                skills_distribution[cat] = len(skills)

    # Extract skill proficiency
    skill_proficiency = {}
    top_skills = skill_result.get("top_skills") or []
    for s in top_skills[:8]:
        if isinstance(s, dict):
            name = s.get("skill", "")
            prof = s.get("proficiency_score", s.get("proficiency", 70))
            if name:
                try:
                    skill_proficiency[name] = int(prof) if str(prof).isdigit() else 70
                except (ValueError, TypeError):
                    skill_proficiency[name] = 70
        elif isinstance(s, str):
            skill_proficiency[s] = 70

    # Extract skill gaps
    raw_gaps = skill_gap_result.get("skill_gaps") or []
    skill_gaps = []
    for gap in raw_gaps[:5]:
        if isinstance(gap, dict):
            skill_gaps.append({
                'skill': gap.get('skill', 'Unknown'),
                'gap_level': gap.get('priority', 'Medium').title(),
                'priority': gap.get('priority', 'Medium').title(),
            })

    # Job matches count
    career_paths = job_matching_result.get("career_paths") or job_matching_result.get("job_matches") or []
    job_matches_count = len(career_paths) if isinstance(career_paths, list) else 0

    # Salary trends from job matching
    salary_trends = {}
    if isinstance(career_paths, list):
        for path in career_paths[:4]:
            if isinstance(path, dict):
                role = path.get("role") or path.get("title", "")
                salary = path.get("salary_range", "")
                if role and salary:
                    try:
                        nums = [int(x.replace(",", "").replace("$", "").strip())
                                for x in salary.replace("k", "000").split("-")
                                if x.strip().replace(",", "").replace("$", "").strip().isdigit()]
                        if nums:
                            salary_trends[role[:20]] = sum(nums) // len(nums)
                    except (ValueError, TypeError):
                        pass

    # Recommendations
    recommendations = []
    rec_actions = recommendation_result.get("immediate_actions") or []
    for action in rec_actions[:5]:
        if isinstance(action, dict):
            recommendations.append(action.get("action", ""))
        elif isinstance(action, str):
            recommendations.append(action)
    if not recommendations:
        recommendations = [
            "Run full analysis to get personalized recommendations"
        ]

    total_skills = len(top_skills) + sum(
        len(v) for v in skill_categories.values()
        if isinstance(v, list)
    ) if skill_categories else len(top_skills)

    user_data = {
        'ats_score': ats_result.get('ats_score', 0),
        'ats_score_improvement': 0,
        'skill_match_percentage': skill_gap_result.get(
            'overall_readiness_score', 0
        ),
        'skill_match_improvement': 0,
        'total_skills': total_skills,
        'new_skills': 0,
        'job_matches_count': job_matches_count,
        'new_job_matches': 0,
        'skills_distribution': skills_distribution,
        'skill_proficiency': skill_proficiency,
        'skill_gaps': skill_gaps,
        'learning_progress': {},
        'job_demand_trend': {},
        'salary_trends': salary_trends,
        'recommendations': recommendations,
    }

    # Add learning progress from roadmap
    roadmap = skill_gap_result.get("learning_roadmap") or {}
    if roadmap:
        phases = roadmap.get("phases") or roadmap.get("milestones") or []
        if phases:
            user_data['learning_progress'] = {
                'completed_courses': 0,
                'total_courses': len(phases),
                'next_course': (
                    phases[0].get("title", "Start learning path")
                    if isinstance(phases[0], dict) else str(phases[0])
                ) if phases else "Complete analysis first",
            }

    return user_data