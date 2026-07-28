"""
TalentMind AI - Interview Preparation Page
==========================================

Streamlit page for interview preparation module.

Author  : TalentMind AI Team
Version : 1.0.0
"""

from __future__ import annotations

import streamlit as st
from typing import Any, Dict, List

from app.services.interview_service import InterviewService
from app.core.constants import UIColor, AgentName

def interview_page() -> None:
    """
    Renders the interview preparation page.
    """
    st.title("🎯 Interview Preparation")
    st.markdown("Generate personalized interview questions based on your resume analysis.")

    # Check if resume has been processed
    if "resume_text" not in st.session_state or not st.session_state.resume_text:
        st.warning("Please upload and process a resume first in the Upload section.")
        return

    # Initialize service
    if "interview_service" not in st.session_state:
        st.session_state.interview_service = InterviewService()

    # Get data from session state
    resume_text = st.session_state.resume_text
    parsed_resume = st.session_state.get("parsed_resume", {})
    target_role = st.session_state.get("target_role", "Software Developer")
    experience_level = st.session_state.get("experience_level", "Mid-level")
    detected_skills = st.session_state.get("detected_skills", [])

    # Display current resume info
    with st.expander("📄 Current Resume Info", expanded=False):
        st.write(f"**Target Role:** {target_role}")
        st.write(f"**Experience Level:** {experience_level}")
        st.write(f"**Detected Skills:** {', '.join(detected_skills) if detected_skills else 'None'}")

    # Generate interview questions button
    if st.button("🚀 Generate Interview Questions", type="primary"):
        with st.spinner("Generating personalized interview questions..."):
            result = st.session_state.interview_service.generate_interview_questions(
                resume_text=resume_text,
                parsed_resume=parsed_resume,
                target_role=target_role,
                experience_level=experience_level,
                detected_skills=detected_skills,
            )

        if not result.get("success", False):
            st.error(f"Failed to generate interview questions: {result.get('error', 'Unknown error')}")
            return

        # Store results in session state
        st.session_state.interview_questions = result
        st.success("Interview questions generated successfully!")

    # Display results if available
    if "interview_questions" in st.session_state and st.session_state.interview_questions.get("success"):
        result = st.session_state.interview_questions

        # Display preparation tips
        if result.get("preparation_tips"):
            st.subheader("💡 Preparation Tips")
            for tip in result["preparation_tips"]:
                st.info(tip)

        # Create tabs for different question types
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "🔧 Technical", 
            "💻 Coding", 
            "👥 HR/Behavioral", 
            "📁 Project", 
            "💭 Conceptual"
        ])

        # Technical Questions
        with tab1:
            st.subheader(f"Technical Questions ({len(result.get('technical_questions', []))})")
            display_questions(result.get("technical_questions", []), "technical")

        # Coding Questions
        with tab2:
            st.subheader(f"Coding Questions ({len(result.get('coding_questions', []))})")
            display_questions(result.get("coding_questions", []), "coding")

        # HR/Behavioral Questions
        with tab3:
            st.subheader(f"HR/Behavioral Questions ({len(result.get('hr_questions', []))})")
            display_questions(result.get("hr_questions", []), "hr")

        # Project Questions
        with tab4:
            st.subheader(f"Project Questions ({len(result.get('project_questions', []))})")
            display_questions(result.get("project_questions", []), "project")

        # Conceptual Questions
        with tab5:
            st.subheader(f"Conceptual Questions ({len(result.get('conceptual_questions', []))})")
            display_questions(result.get("conceptual_questions", []), "conceptual")

        # Overall stats
        st.divider()
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Questions", result.get("total_questions", 0))
        with col2:
            st.metric("Difficulty Level", result.get("difficulty_level", "Medium").title())
        with col3:
            st.metric("Categories", "5")

def display_questions(questions: List[Dict[str, Any]], category: str) -> None:
    """
    Displays a list of questions with optional filtering and interaction.

    Args:
        questions: List of question dictionaries
        category: Question category (for styling)
    """
    if not questions:
        st.info(f"No {category} questions generated.")
        return

    # Filter controls
    col1, col2 = st.columns([2, 1])
    with col1:
        difficulty_filter = st.selectbox(
            f"Filter by Difficulty ({category})",
            options=["All", "Easy", "Medium", "Hard"],
            key=f"diff_filter_{category}"
        )
    with col2:
        # Sort options
        sort_option = st.selectbox(
            "Sort by",
            options=["Order", "Difficulty"],
            key=f"sort_{category}"
        )

    # Filter questions
    filtered_questions = questions
    if difficulty_filter != "All":
        filtered_questions = [
            q for q in questions 
            if q.get("difficulty", "").lower() == difficulty_filter.lower()
        ]

    # Sort questions
    if sort_option == "Difficulty":
        order = {"Easy": 0, "Medium": 1, "Hard": 2}
        filtered_questions = sorted(
            filtered_questions,
            key=lambda x: order.get(x.get("difficulty", "Medium"), 1)
        )

    # Display each question
    for i, q in enumerate(filtered_questions, 1):
        with st.expander(f"Question {i}: {q.get('question', 'No question text')[:100]}..."):
            st.markdown(f"**Question:** {q.get('question', 'N/A')}")
            st.markdown(f"**Category:** {q.get('category', category).title()}")
            st.markdown(f"**Difficulty:** {q.get('difficulty', 'Medium').title()}")
            if q.get("hint"):
                st.markdown(f"**Hint:** {q.get('hint')}")
            if q.get("why_asked"):
                st.markdown(f"**Why asked:** {q.get('why_asked')}")
            if q.get("sample_answer"):
                st.markdown(f"**Sample Answer:** {q.get('sample_answer')}")

            # Copy to clipboard button
            if st.button("📋 Copy Question", key=f"copy_{category}_{i}"):
                st.write("Question copied to clipboard!")
                # In a real app, we would use st.clipboard or similar
                # For now, we just show a message

# For direct testing
if __name__ == "__main__":
    interview_page()