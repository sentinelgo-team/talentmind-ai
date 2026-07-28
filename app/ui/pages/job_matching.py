"""
TalentMind AI - Job Matching Page
=================================

Streamlit page for job matching module.

Author  : TalentMind AI Team
Version : 1.0.0
"""

from __future__ import annotations

import streamlit as st
from typing import Any, Dict, List

from app.services.job_matching_service import JobMatchingService
from app.core.constants import UIColor, AgentName

def job_matching_page() -> None:
    """
    Renders the job matching page.
    """
    st.title("💼 Job Matching & Career Guidance")
    st.markdown("Discover your best job matches and get personalized career recommendations.")

    # Check if resume has been processed
    if "resume_text" not in st.session_state or not st.session_state.resume_text:
        st.warning("Please upload and process a resume first in the Upload section.")
        return

    # Initialize service
    if "job_matching_service" not in st.session_state:
        st.session_state.job_matching_service = JobMatchingService()

    # Get data from session state
    resume_text = st.session_state.resume_text
    skill_result = st.session_state.get("skill_result") or {}
    detected_skills = st.session_state.get("detected_skills", [])
    if not detected_skills:
        # Pull from skill analysis result
        top_skills = skill_result.get("top_skills") or []
        detected_skills = [
            s if isinstance(s, str) else s.get("skill", s.get("name", ""))
            for s in top_skills
        ]
        # Also check parsed resume skills
        if not detected_skills:
            parsed = st.session_state.get("parsed_resume") or {}
            detected_skills = parsed.get("skills", [])

    experience_level = (
        skill_result.get("experience_level")
        or st.session_state.get("experience_level", "Mid-level")
    )
    primary_domain = (
        skill_result.get("primary_domain")
        or st.session_state.get("primary_domain", "Technology")
    )
    target_role = st.session_state.get("target_role", "")

    # Display current resume info
    with st.expander("📄 Current Resume Profile", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Experience Level:** {experience_level}")
            st.write(f"**Primary Domain:** {primary_domain}")
        with col2:
            st.write(f"**Target Role Preference:** {target_role if target_role else 'Open to opportunities'}")
            st.write(f"**Detected Skills:** {', '.join(detected_skills) if detected_skills else 'None'}")

    # Find job matches button
    if st.button("🔍 Find My Best Job Matches", type="primary"):
        with st.spinner("Analyzing your profile and finding job matches..."):
            result = st.session_state.job_matching_service.match_jobs(
                resume_text=resume_text,
                detected_skills=detected_skills,
                experience_level=experience_level,
                primary_domain=primary_domain,
                target_role=target_role,
            )

        if not result.get("success", False):
            st.error(f"Failed to find job matches: {result.get('error', 'Unknown error')}")
            return

        # Store results in session state
        st.session_state.job_matches_result = result
        st.success("Job matches found successfully!")

    # Display results if available
    if "job_matches_result" in st.session_state and st.session_state.job_matches_result.get("success"):
        result = st.session_state.job_matches_result

        # Salary range info
        if result.get("salary_range"):
            salary_range = result["salary_range"]
            if isinstance(salary_range, dict) and salary_range.get("min") and salary_range.get("max"):
                st.subheader("💰 Expected Salary Range")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Minimum", f"₹{salary_range['min']:,} {salary_range.get('currency', 'INR')} {salary_range.get('period', 'per annum')}")
                with col2:
                    st.metric("Maximum", f"₹{salary_range['max']:,} {salary_range.get('currency', 'INR')} {salary_range.get('period', 'per annum')}")
                with col3:
                    st.metric("Currency", salary_range.get('currency', 'INR'))

        # Next role suggestion
        if result.get("next_role_suggestion"):
            st.subheader("🎯 Next Role Suggestion")
            st.info(f"**{result['next_role_suggestion']}**")

        # Create tabs for different sections
        tab1, tab2, tab3, tab4 = st.tabs([
            "🎯 Job Matches", 
            "📈 Career Paths", 
            "🎓 Internships", 
            "🏭 Industry Fit"
        ])

        # Job Matches Tab
        with tab1:
            st.subheader(f"Top {len(result.get('job_matches', []))} Job Matches")
            job_matches = result.get("job_matches", [])
            
            if not job_matches:
                st.info("No job matches found.")
            else:
                for i, job in enumerate(job_matches, 1):
                    # Determine match label color
                    score = job.get("match_score", 0)
                    if score >= 85:
                        color = "green"
                        label = "Excellent Match"
                    elif score >= 70:
                        color = "orange"
                        label = "Good Match"
                    elif score >= 50:
                        color = "orange"
                        label = "Fair Match"
                    else:
                        color = "red"
                        label = "Poor Match"
                    
                    with st.expander(f"#{i} {job.get('role', 'Unknown Role')} - {score}% Match"):
                        col1, col2 = st.columns([2, 1])
                        
                        with col1:
                            st.markdown(f"**Match Score:** :{color}[{score}%]")
                            st.markdown(f"**Match Label:** :{color}[{label}]")
                            st.markdown(f"**Why Good Fit:** {job.get('why_good_fit', 'Not specified')}")
                            
                            # Skills match/missing
                            matching_skills = job.get("matching_skills", [])
                            missing_skills = job.get("missing_skills", [])
                            
                            if matching_skills:
                                st.markdown(f"**✅ Matching Skills:** {', '.join(matching_skills)}")
                            if missing_skills:
                                st.markdown(f"**❌ Missing Skills:** {', '.join(missing_skills)}")
                            
                            # Required skills
                            required_skills = job.get("required_skills", [])
                            if required_skills:
                                st.markdown(f"**📋 Required Skills:** {', '.join(required_skills)}")
                        
                        with col2:
                            st.markdown(f"**💰 Salary Range:** {job.get('salary_range', 'Not specified')}")
                            st.markdown(f"**🏢 Companies:** {', '.join(job.get('companies', ['Not specified']))}")
                            st.markdown(f"**📈 Growth Path:** {job.get('growth_path', 'Not specified')}")

        # Career Paths Tab
        with tab2:
            st.subheader("📈 Career Progression Paths")
            career_paths = result.get("career_paths", [])
            
            if not career_paths:
                st.info("No career paths suggested.")
            else:
                for i, path in enumerate(career_paths, 1):
                    st.markdown(f"**Path {i}:** {path}")

        # Internships Tab
        with tab3:
            st.subheader("🎓 Internship Recommendations")
            internship_recs = result.get("internship_recs", [])
            
            # Only show internships for entry-level candidates
            if experience_level.lower() in ["entry", "fresher", "entry-level", "intern"] or not internship_recs:
                if not internship_recs:
                    st.info("Internship recommendations are typically for entry-level candidates.")
                else:
                    for internship in internship_recs:
                        with st.expander(f"🎓 {internship.get('role', 'Internship')} at {internship.get('company', 'Company')}"):
                            st.markdown(f"**Duration:** {internship.get('duration', 'Not specified')}")
                            st.markdown(f"**Stipend:** {internship.get('stipend', 'Not specified')}")
                            st.markdown(f"**Skills Gained:** {', '.join(internship.get('skills_gained', []))}")
            else:
                st.info("Internship recommendations are shown for entry-level candidates.")

        # Industry Fit Tab
        with tab4:
            st.subheader("🏭 Industry Fit Analysis")
            industry_fit = result.get("industry_fit", [])
            
            if not industry_fit:
                st.info("No industry fit analysis available.")
            else:
                for industry in industry_fit:
                    with st.expander(f"🏭 {industry.get('industry', 'Unknown Industry')} - {industry.get('fit_score', 0)}% Fit"):
                        st.markdown(f"**Fit Score:** {industry.get('fit_score', 0)}%")
                        st.markdown(f"**Description:** {industry.get('fit_description', 'No description available')}")

        # Overall stats
        st.divider()
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Matches", result.get("total_matches", 0))
        with col2:
            avg_score = sum(job.get("match_score", 0) for job in result.get("job_matches", [])) / max(len(result.get("job_matches", [])), 1)
            st.metric("Avg Match Score", f"{avg_score:.1f}%")
        with col3:
            st.metric("Categories", "4")
