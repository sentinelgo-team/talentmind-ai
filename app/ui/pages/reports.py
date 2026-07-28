"""
TalentMind AI - Reports Page
============================

Generate and view professional reports including resume analysis reports,
skill gap reports, career guidance reports, and interview preparation guides.

Author  : TalentMind AI Team
Version : 1.0.0
"""

from __future__ import annotations

import streamlit as st
from typing import Any, Dict
import base64
from datetime import datetime
from io import BytesIO

def reports_page() -> None:
    """Renders the reports generation and viewing page."""
    st.title("📑 Reports & Documentation")
    st.markdown("Generate professional reports to document your career profile, skills, and recommendations.")
    
    # Check if resume has been processed
    if "resume_text" not in st.session_state or not st.session_state.resume_text:
        st.warning("Please upload and process a resume first in the Upload section to generate reports.")
        return
    
    # Report type selection
    st.subheader("📋 Select Report Type")
    
    report_col1, report_col2 = st.columns(2)
    
    with report_col1:
        report_type = st.selectbox(
            "Choose Report Type",
            [
                "Resume Analysis Report",
                "Skill Gap Analysis Report", 
                "Career Guidance Report",
                "Interview Preparation Guide",
                "Job Matching Report",
                "Complete Career Portfolio"
            ]
        )
    
    with report_col2:
        report_format = st.radio(
            "Report Format",
            ["PDF (Professional)", "HTML (Web)", "Markdown", "Plain Text"],
            index=0
        )
    
    # Report options
    st.subheader("⚙️ Report Options")
    
    option_col1, option_col2 = st.columns(2)
    
    with option_col1:
        include_charts = st.checkbox("Include Charts & Visualizations", value=True)
        include_recommendations = st.checkbox("Include Recommendations", value=True)
        include_timeline = st.checkbox("Include Career Timeline", value=False)
    
    with option_col2:
        include_contact_info = st.checkbox("Include Contact Information", value=True)
        include_skills_matrix = st.checkbox("Include Skills Matrix", value=True)
        include_project_highlights = st.checkbox("Include Project Highlights", value=True)
    
    # Generate report button
    if st.button("📄 Generate Report", type="primary", width="stretch"):
        with st.spinner(f"Generating {report_type}..."):
            if report_format == "PDF (Professional)":
                pdf_bytes = _generate_pdf_report()
                if pdf_bytes:
                    st.session_state.generated_report_pdf = pdf_bytes
                    st.session_state.report_type = report_type
                    st.session_state.report_format = report_format
                    st.success(f"✅ {report_type} generated successfully!")
                else:
                    st.error("Failed to generate PDF report.")
            else:
                report_data = _generate_report_content(
                    report_type,
                    report_format,
                    include_charts,
                    include_recommendations,
                    include_timeline,
                    include_contact_info,
                    include_skills_matrix,
                    include_project_highlights
                )
                st.session_state.generated_report = report_data
                st.session_state.report_type = report_type
                st.session_state.report_format = report_format
                st.success(f"✅ {report_type} generated successfully!")

    # Display generated report
    if "generated_report_pdf" in st.session_state and st.session_state.get("report_format") == "PDF (Professional)":
        st.divider()
        st.subheader(f"📄 {st.session_state.get('report_type', 'Report')}")
        st.info("PDF report generated! Click below to download.")

        pdf_bytes = st.session_state.generated_report_pdf
        st.download_button(
            label="💾 Download PDF Report",
            data=pdf_bytes,
            file_name=f"talentmind_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
            mime="application/pdf",
            type="primary",
        )

    elif "generated_report" in st.session_state:
        st.divider()
        st.subheader(f"📄 {st.session_state.get('report_type', 'Report')}")

        report_content = st.session_state.generated_report
        report_fmt = st.session_state.get("report_format", "")

        if report_fmt == "HTML (Web)":
            st.components.v1.html(report_content, height=600, scrolling=True)
        elif report_fmt == "Markdown":
            st.markdown(report_content)
        else:
            st.text(report_content)

        st.download_button(
            label="💾 Download Report",
            data=report_content.encode("utf-8"),
            file_name=f"talentmind_report.{'md' if 'Markdown' in report_fmt else 'txt'}",
            mime="text/plain",
        )
    
    # Report history section
    st.divider()
    st.subheader("📚 Report History")
    st.info("Reports you generate will appear as downloads above.")


def _generate_pdf_report() -> bytes:
    """Generate a real PDF report using ReportGenerator and session data."""
    try:
        from app.services.report_generator import ReportGenerator

        generator = ReportGenerator()
        candidate_name = st.session_state.get("candidate_name", "Candidate")

        analysis_data = st.session_state.get("analysis_results") or {}
        if not analysis_data:
            analysis_data = {
                "resume_result": st.session_state.get("resume_result") or (
                    {"success": True, "parsed_resume": st.session_state.get("parsed_resume", {})}
                    if st.session_state.get("resume_parsed") else {}
                ),
                "ats_result": st.session_state.get("ats_result") or {},
                "skill_result": st.session_state.get("skill_result") or {},
                "skill_gap_result": st.session_state.get("skill_gap_result") or {},
                "risk_result": st.session_state.get("risk_result") or {},
                "recommendation_result": st.session_state.get("recommendation_result") or {},
                "target_role": st.session_state.get("target_role", "General Technology Role"),
            }

        pdf_bytes = generator.generate_full_report(
            candidate_name=candidate_name,
            analysis_data=analysis_data,
        )
        return pdf_bytes

    except Exception as exc:
        st.error(f"PDF generation error: {exc}")
        return b""


def _generate_report_content(
    report_type: str,
    format_type: str,
    include_charts: bool,
    include_recommendations: bool,
    include_timeline: bool,
    include_contact_info: bool,
    include_skills_matrix: bool,
    include_project_highlights: bool
) -> str:
    """
    Generate report content based on selected options.
    In a real implementation, this would use actual data from analysis results.
    """
    
    # Get user data from session state (simulated)
    user_data = _get_user_data_for_reports()
    
    # Generate report based on type
    if report_type == "Resume Analysis Report":
        return _generate_resume_report(
            user_data, format_type, include_charts, include_recommendations,
            include_contact_info, include_skills_matrix, include_project_highlights
        )
    elif report_type == "Skill Gap Analysis Report":
        return _generate_skill_gap_report(
            user_data, format_type, include_charts, include_recommendations,
            include_timeline, include_contact_info
        )
    elif report_type == "Career Guidance Report":
        return _generate_career_guidance_report(
            user_data, format_type, include_charts, include_recommendations,
            include_timeline, include_contact_info
        )
    elif report_type == "Interview Preparation Guide":
        return _generate_interview_guide(
            user_data, format_type, include_charts, include_recommendations
        )
    elif report_type == "Job Matching Report":
        return _generate_job_matching_report(
            user_data, format_type, include_charts, include_recommendations
        )
    else:  # Complete Career Portfolio
        return _generate_complete_portfolio(
            user_data, format_type, include_charts, include_recommendations,
            include_timeline, include_contact_info, include_skills_matrix,
            include_project_highlights
        )


def _get_user_data_for_reports() -> Dict[str, Any]:
    """Get user data from session state for report generation."""
    parsed_resume = st.session_state.get("parsed_resume") or {}
    ats_result = st.session_state.get("ats_result") or {}
    skill_result = st.session_state.get("skill_result") or {}
    skill_gap_result = st.session_state.get("skill_gap_result") or {}
    recommendation_result = st.session_state.get("recommendation_result") or {}
    interview_result = st.session_state.get("interview_result") or {}
    job_matching_result = st.session_state.get("job_matching_result") or {}

    contact = parsed_resume.get("contact_info") or {}
    personal_info = {
        "name": contact.get("name", st.session_state.get("candidate_name", "Candidate")),
        "email": contact.get("email", "N/A"),
        "phone": contact.get("phone", "N/A"),
        "location": contact.get("location", "N/A"),
        "linkedin": contact.get("linkedin", ""),
        "github": contact.get("github", ""),
    }

    # Skills
    top_skills = skill_result.get("top_skills") or []
    tech_skills = [s.get("skill", s) if isinstance(s, dict) else s for s in top_skills]
    soft_skills = skill_result.get("soft_skills") or []

    # Experience
    experience = []
    for exp in parsed_resume.get("experience") or []:
        if isinstance(exp, dict):
            experience.append({
                "company": exp.get("company", ""),
                "position": exp.get("job_title", ""),
                "duration": f"{exp.get('start_date', '')} - {exp.get('end_date', 'Present')}",
                "achievements": exp.get("description") or [],
            })

    # Education
    education = []
    for edu in parsed_resume.get("education") or []:
        if isinstance(edu, dict):
            education.append({
                "degree": edu.get("degree", ""),
                "institution": edu.get("institution", ""),
                "year": str(edu.get("end_year", "")),
                "gpa": edu.get("grade", "N/A"),
            })

    # Projects
    projects = []
    for proj in parsed_resume.get("projects") or []:
        if isinstance(proj, dict):
            projects.append({
                "name": proj.get("name", ""),
                "description": proj.get("description", ""),
                "technologies": proj.get("technologies") or [],
                "outcome": ", ".join(proj.get("highlights") or []),
            })

    # Skill gaps
    raw_gaps = skill_gap_result.get("skill_gaps") or []
    skill_gaps = []
    for gap in raw_gaps[:5]:
        if isinstance(gap, dict):
            skill_gaps.append({
                "skill": gap.get("skill", ""),
                "importance": gap.get("priority", "Medium").title(),
                "suggestion": gap.get("reason", ""),
            })

    # Career recommendations
    career_recs = []
    for action in (recommendation_result.get("immediate_actions") or [])[:5]:
        if isinstance(action, dict):
            career_recs.append(action.get("action", ""))
        elif isinstance(action, str):
            career_recs.append(action)
    if not career_recs:
        career_recs = ["Run full analysis to get recommendations"]

    # Interview prep
    interview_data = interview_result.get("questions") or interview_result.get("interview_questions") or {}
    technical_topics = []
    behavioral_questions = []
    if isinstance(interview_data, dict):
        for cat, questions in interview_data.items():
            if isinstance(questions, list):
                for q in questions[:3]:
                    if "technical" in cat.lower() or "coding" in cat.lower():
                        technical_topics.append(q if isinstance(q, str) else q.get("question", ""))
                    else:
                        behavioral_questions.append(q if isinstance(q, str) else q.get("question", ""))
    elif isinstance(interview_data, list):
        for q in interview_data[:6]:
            if isinstance(q, dict):
                behavioral_questions.append(q.get("question", ""))
            elif isinstance(q, str):
                behavioral_questions.append(q)

    # Job matches
    raw_matches = job_matching_result.get("career_paths") or job_matching_result.get("job_matches") or []
    job_matches = []
    for match in raw_matches[:5]:
        if isinstance(match, dict):
            job_matches.append({
                "title": match.get("role") or match.get("title", ""),
                "company": match.get("company", "Various"),
                "match_score": match.get("fit_score") or match.get("match_score", 0),
                "salary_range": match.get("salary_range", "N/A"),
                "highlights": match.get("requirements") or match.get("highlights") or [],
            })

    return {
        "personal_info": personal_info,
        "resume_summary": {
            "total_experience": f"{parsed_resume.get('total_experience_years', 0)} years",
            "current_level": skill_gap_result.get("experience_level", "mid").title(),
            "primary_domain": skill_result.get("primary_domain", "Technology"),
            "target_role": st.session_state.get("target_role", "General Technology Role"),
            "ats_score": ats_result.get("ats_score", 0),
        },
        "skills": {
            "technical": tech_skills[:10],
            "soft": soft_skills[:5] if soft_skills else [],
        },
        "experience": experience,
        "education": education,
        "projects": projects,
        "skill_gaps": skill_gaps,
        "career_recommendations": career_recs,
        "interview_prep": {
            "technical_topics": technical_topics[:5] or ["Complete analysis for topics"],
            "behavioral_questions": behavioral_questions[:5] or ["Complete analysis for questions"],
            "questions_to_ask": ["What does success look like in this role?", "What are the team's biggest challenges?", "How does the team approach technical debt?"],
        },
        "job_matches": job_matches,
    }


def _generate_resume_report(user_data, format_type, include_charts, include_recommendations,
                          include_contact_info, include_skills_matrix, include_project_highlights) -> str:
    """Generate resume analysis report."""
    if format_type == "Markdown":
        result = f"""# Resume Analysis Report

## Personal Information
**Name:** {user_data['personal_info']['name']}
**Email:** {user_data['personal_info']['email']}
**Phone:** {user_data['personal_info']['phone']}
**Location:** {user_data['personal_info']['location']}

## Professional Summary
- **Experience Level:** {user_data['resume_summary']['total_experience']}
- **Current Role:** {user_data['resume_summary']['current_level']}
- **Primary Domain:** {user_data['resume_summary']['primary_domain']}
- **Target Role:** {user_data['resume_summary']['target_role']}
- **ATS Compatibility Score:** {user_data['resume_summary']['ats_score']}/100

## Skills Overview
"""
        if include_skills_matrix:
            tech = user_data['skills']['technical']
            soft = user_data['skills']['soft']
            result += f"### Technical Skills ({len(tech)}): {', '.join(tech)}\n"
            result += f"### Soft Skills ({len(soft)}): {', '.join(soft)}\n"

        result += "\n## Professional Experience\n"

        for i, exp in enumerate(user_data['experience'], 1):
            result += f"### {i}. {exp['position']} at {exp['company']}\n"
            result += f"**Duration:** {exp['duration']}\n"
            result += "**Key Achievements:**\n"
            for achievement in exp['achievements']:
                result += f"- {achievement}\n"
            result += "\n"

        if include_project_highlights:
            result += "## Notable Projects\n"
            for i, project in enumerate(user_data['projects'], 1):
                result += f"### {i}. {project['name']}\n"
                result += f"**Description:** {project['description']}\n"
                result += f"**Technologies:** {', '.join(project['technologies'])}\n"
                result += f"**Outcome:** {project['outcome']}\n\n"

        result += "## Education\n"
        for edu in user_data['education']:
            result += f"- **{edu['degree']}** from {edu['institution']} ({edu['year']}) - GPA: {edu['gpa']}\n"

        if include_recommendations:
            result += "\n## Recommendations for Improvement\n"
            for i, rec in enumerate(user_data['career_recommendations'], 1):
                result += f"{i}. {rec}\n"

        return result

    else:
        return f"""Resume Analysis Report for {user_data['personal_info']['name']}

Professional Summary:
- Experience: {user_data['resume_summary']['total_experience']}
- Level: {user_data['resume_summary']['current_level']}
- Domain: {user_data['resume_summary']['primary_domain']}
- Target: {user_data['resume_summary']['target_role']}
- ATS Score: {user_data['resume_summary']['ats_score']}/100

Skills: {len(user_data['skills']['technical'])} technical, {len(user_data['skills']['soft'])} soft skills

Experience: {len(user_data['experience'])} positions
Education: {len(user_data['education'])} degrees
Projects: {len(user_data['projects'])} projects

Recommendations: {len(user_data['career_recommendations'])} items provided
"""


def _generate_skill_gap_report(user_data, format_type, include_charts, include_recommendations,
                             include_timeline, include_contact_info) -> str:
    """Generate skill gap analysis report."""
    if format_type == "Markdown":
        result = f"""# Skill Gap Analysis Report

## Target Role: {user_data['resume_summary']['target_role']}
## Current Level: {user_data['resume_summary']['current_level']}

## Identified Skill Gaps
"""
        for i, gap in enumerate(user_data['skill_gaps'], 1):
            result += f"""### {i}. {gap['skill']}
**Importance Level:** {gap['importance']}
**Recommendation:** {gap['suggestion']}

"""
        
        if include_recommendations:
            result += "## Learning Recommendations\n"
            for i, rec in enumerate(user_data['career_recommendations'], 1):
                result += f"{i}. {rec}\n"
        
        return result
    
    else:
        result = f"""Skill Gap Analysis Report

Target Role: {user_data['resume_summary']['target_role']}
Current Level: {user_data['resume_summary']['current_level']}

Identified Skill Gaps: {len(user_data['skill_gaps'])}
"""
        for gap in user_data['skill_gaps']:
            result += f"- {gap['skill']} ({gap['importance']} importance)\n"

        return result


def _generate_career_guidance_report(user_data, format_type, include_charts, include_recommendations,
                                   include_timeline, include_contact_info) -> str:
    """Generate career guidance report."""
    if format_type == "Markdown":
        result = f"""# Career Guidance Report

## Candidate Profile
**Name:** {user_data['personal_info']['name']}
**Current Level:** {user_data['resume_summary']['current_level']}
**Target Role:** {user_data['resume_summary']['target_role']}
**Industry Focus:** {user_data['resume_summary']['primary_domain']}

## Career Development Path
"""
        
        if include_recommendations:
            result += "### Recommended Career Path\n"
            for i, rec in enumerate(user_data['career_recommendations'], 1):
                result += f"{i}. {rec}\n"
        
        result += f"""## Skill Development Priorities
"""
        for i, gap in enumerate(user_data['skill_gaps'][:3], 1):
            result += f"{i}. **{gap['skill']}** - {gap['suggestion']}\n"
        
        return result
    
    else:
        return f"""Career Guidance Report

Candidate: {user_data['personal_info']['name']}
Current Level: {user_data['resume_summary']['current_level']}
Target Role: {user_data['resume_summary']['target_role']}

Recommendations: {len(user_data['career_recommendations'])} items
Priority Skills: {len([g for g in user_data['skill_gaps'] if g['importance'] == 'High'])} high-priority gaps
"""


def _generate_interview_guide(user_data, format_type, include_charts, include_recommendations) -> str:
    """Generate interview preparation guide."""
    if format_type == "Markdown":
        result = f"""# Interview Preparation Guide

## Target Role: {user_data['resume_summary']['target_role']}
## Experience Level: {user_data['resume_summary']['current_level']}

## Technical Preparation Areas
"""
        for i, topic in enumerate(user_data['interview_prep']['technical_topics'], 1):
            result += f"{i}. {topic}\n"
        
        result += "\n## Behavioral Interview Preparation\n"
        for i, question in enumerate(user_data['interview_prep']['behavioral_questions'], 1):
            result += f"{i}. {question}\n"
        
        result += "\n## Questions to Ask the Interviewer\n"
        for i, question in enumerate(user_data['interview_prep']['questions_to_ask'], 1):
            result += f"{i}. {question}\n"
        
        return result
    
    else:
        return f"""Interview Preparation Guide

Target Role: {user_data['resume_summary']['target_role']}
Experience Level: {user_data['resume_summary']['current_level']}

Technical Topics: {len(user_data['interview_prep']['technical_topics'])} areas
Behavioral Questions: {len(user_data['interview_prep']['behavioral_questions'])} prepared
Questions to Ask: {len(user_data['interview_prep']['questions_to_ask'])} ready
"""


def _generate_job_matching_report(user_data, format_type, include_charts, include_recommendations) -> str:
    """Generate job matching report."""
    if format_type == "Markdown":
        result = f"""# Job Matching Report

## Target Role: {user_data['resume_summary']['target_role']}
## Current Level: {user_data['resume_summary']['current_level']}

## Top Job Matches
"""
        for i, job in enumerate(user_data['job_matches'], 1):
            result += f"""### {i}. {job['title']} at {job['company']}
**Match Score:** {job['match_score']}%
**Salary Range:** {job['salary_range']}
**Key Highlights:** {', '.join(job['highlights'])}

"""
        
        return result
    
    else:
        result = f"""Job Matching Report

Target Role: {user_data['resume_summary']['target_role']}
Current Level: {user_data['resume_summary']['current_level']}

Number of Matches: {len(user_data['job_matches'])}

Top Matches:
"""
        for i, job in enumerate(user_data['job_matches'][:3], 1):
            result += f"{i}. {job['title']} at {job['company']} ({job['match_score']}% match)\n"

        return result


def _generate_complete_portfolio(user_data, format_type, include_charts, include_recommendations,
                               include_timeline, include_contact_info, include_skills_matrix,
                               include_project_highlights) -> str:
    """Generate complete career portfolio."""
    # Combine all report types
    resume_report = _generate_resume_report(
        user_data, format_type, include_charts, include_recommendations,
        include_contact_info, include_skills_matrix, include_project_highlights
    )
    
    skill_gap_report = _generate_skill_gap_report(
        user_data, format_type, include_charts, include_recommendations,
        include_timeline, include_contact_info
    )
    
    career_report = _generate_career_guidance_report(
        user_data, format_type, include_charts, include_recommendations,
        include_timeline, include_contact_info
    )
    
    if format_type == "Markdown":
        return f"""# Complete Career Portfolio

## Section 1: Resume Analysis
{resume_report}

## Section 2: Skill Gap Analysis
{skill_gap_report}

## Section 3: Career Guidance
{career_report}

## Section 4: Interview Preparation
{_generate_interview_guide(user_data, format_type, include_charts, include_recommendations)}

## Section 5: Job Market Analysis
{_generate_job_matching_report(user_data, format_type, include_charts, include_recommendations)}

---
*Report generated by TalentMind AI on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}*
"""
    
    else:
        return f"""Complete Career Portfolio

Generated for: {user_data['personal_info']['name']}
Date: {datetime.now().strftime('%B %d, %Y')}

Sections Included:
1. Resume Analysis
2. Skill Gap Analysis  
3. Career Guidance
4. Interview Preparation
5. Job Market Analysis

Total Sections: 5
"""