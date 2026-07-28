"""
TalentMind AI - Upload Page
==============================
Streamlit UI for resume file upload with
validation feedback and progress indicators.

Author  : TalentMind AI Team
Version : 1.0.0
"""

from __future__ import annotations

import logging

import streamlit as st

from app.core.exceptions import (
    EmptyDocumentError,
    FileSizeExceededError,
    InvalidFileTypeError,
    TalentMindBaseException,
)
from app.core.settings import get_settings
from app.services.resume_service import ResumeService

logger = logging.getLogger(__name__)
cfg    = get_settings()


def render_upload_page() -> None:
    """
    Renders the complete resume upload page.

    Features:
        - Drag and drop file upload
        - Real-time validation feedback
        - Upload progress indicator
        - Text preview after extraction
        - Session state management
    """

    # ── Page Header ──────────────────────────────────────────
    st.markdown(
        '<div class="section-header" style="font-size: 1.6rem; border: none;">'
        '📄 Upload Resume</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<p style="color: #8892A4; margin-top: -0.5rem;">'
        'Upload your resume and let 11 specialized AI agents '
        'analyze every aspect of your career profile.</p>',
        unsafe_allow_html=True
    )
    st.markdown("---")

    # ── Upload Guidelines ────────────────────────────────────
    with st.expander("📋 Upload Guidelines", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            **Supported Formats:**
            - PDF  (.pdf)
            - Word Document  (.docx)
            - Plain Text  (.txt)
            """)
        with col2:
            st.markdown(f"""
            **Requirements:**
            - Max size: {cfg.MAX_FILE_SIZE_MB} MB
            - Min content: 100 characters
            - Must contain readable text
            """)

    st.markdown("### Upload Your Resume")

    # ── File Upload Widget ───────────────────────────────────
    uploaded_file = st.file_uploader(
        label="Drag and drop or click to browse",
        type=cfg.allowed_file_types_list,
        accept_multiple_files=False,
        help=(
            f"Supported: "
            f"{', '.join(cfg.allowed_file_types_list).upper()} "
            f"| Max: {cfg.MAX_FILE_SIZE_MB}MB"
        ),
    )

    # ── Optional Candidate Name ──────────────────────────────
    candidate_name = st.text_input(
        label="Your Name (Optional)",
        placeholder="e.g. John Smith",
        max_chars=100,
        help="Helps personalize your analysis report."
    )

    # ── Target Role ──────────────────────────────────────────
    target_role = st.text_input(
        label="Target Role (Optional)",
        placeholder="e.g. Senior Software Engineer",
        max_chars=100,
        value=st.session_state.get(
            "target_role", ""
        ),
        help="The role you're targeting. Improves analysis accuracy."
    )
    if target_role:
        st.session_state["target_role"] = target_role

    # ── Process Upload ───────────────────────────────────────
    if uploaded_file is not None:

        # Show file info
        file_size_kb = len(uploaded_file.getvalue()) / 1024
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("File Name", uploaded_file.name)
        with col2:
            st.metric(
                "File Size",
                f"{file_size_kb:.1f} KB"
            )
        with col3:
            st.metric(
                "File Type",
                uploaded_file.type or "Unknown"
            )

        st.markdown("---")

        # Analyze button
        analyze_btn = st.button(
            label="🚀  Analyze Resume",
            type="primary",
            width="stretch",
        )

        if analyze_btn:
            _process_uploaded_file(
                uploaded_file=uploaded_file,
                candidate_name=candidate_name.strip()
                               if candidate_name else None,
            )

    # ── Show Results if Already Uploaded ────────────────────
    if st.session_state.get("resume_uploaded"):
        _render_upload_success()


def _process_uploaded_file(
    uploaded_file,
    candidate_name: str | None,
) -> None:
    """
    Processes the uploaded file with progress feedback.

    Args:
        uploaded_file  : Streamlit UploadedFile object
        candidate_name : Optional candidate name
    """
    service = ResumeService()

    # Progress bar
    progress = st.progress(0, text="Starting upload...")

    try:
        # Read file bytes
        progress.progress(20, text="Reading file...")
        file_bytes = uploaded_file.getvalue()

        # Process file
        progress.progress(50, text="Extracting text...")
        result = service.upload_resume(
            file_bytes     = file_bytes,
            file_name      = uploaded_file.name,
            candidate_name = candidate_name,
        )

        progress.progress(80, text="Saving to database...")

        if result["success"]:
            progress.progress(
                100, text="Upload complete!"
            )

            # Save to session state
            st.session_state["resume_uploaded"]  = True
            st.session_state["candidate_id"]     = result["candidate_id"]
            st.session_state["resume_id"]        = result["resume_id"]
            st.session_state["resume_text"]      = result["raw_text"]
            st.session_state["resume_file_name"] = result["file_name"]
            st.session_state["resume_file_type"] = result["file_type"]
            st.session_state["char_count"]       = result["char_count"]

            st.success(
                f"✅  **{result['message']}**"
            )
            logger.info(
                "Upload success | candidate=%s | resume=%s",
                result["candidate_id"],
                result["resume_id"]
            )

        else:
            progress.empty()
            st.error(f"❌  {result['message']}")

    except InvalidFileTypeError as exc:
        progress.empty()
        st.error(
            f"❌  **Invalid File Type**\n\n{exc.message}"
        )

    except FileSizeExceededError as exc:
        progress.empty()
        st.error(
            f"❌  **File Too Large**\n\n{exc.message}"
        )

    except EmptyDocumentError as exc:
        progress.empty()
        st.error(
            f"❌  **Empty Document**\n\n{exc.message}"
        )

    except TalentMindBaseException as exc:
        progress.empty()
        st.error(f"❌  **Error:** {exc.message}")

    except Exception as exc:
        progress.empty()
        st.error(
            f"❌  **Unexpected Error**\n\n"
            f"Please try again. Details: {str(exc)}"
        )
        logger.error("Upload page error: %s", exc)


def _render_upload_success() -> None:
    """
    Renders success state after upload with
    text preview and navigation options.
    """
    st.divider()
    st.markdown("### ✅ Resume Uploaded Successfully")

    # Metrics row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(
            "File",
            st.session_state.get("resume_file_name", "N/A")
        )
    with col2:
        st.metric(
            "Type",
            st.session_state.get(
                "resume_file_type", "N/A"
            ).upper()
        )
    with col3:
        char_count = st.session_state.get("char_count", 0)
        st.metric("Characters", f"{char_count:,}")
    with col4:
        st.metric("Status", "✅ Ready")

    # Resume text preview
    st.markdown("### 📄 Extracted Text Preview")

    resume_text = st.session_state.get("resume_text", "")
    preview_text = (
        resume_text[:1500] + "..."
        if len(resume_text) > 1500
        else resume_text
    )

    st.text_area(
        label      = "Resume Content (Preview)",
        value      = preview_text,
        height     = 300,
        disabled   = True,
        help       = "First 1500 characters of your resume."
    )

    # Action buttons
    st.markdown("### 🚀 Next Steps")
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button(
            "🔍  Run Full Analysis",
            width="stretch",
            type="primary"
        ):
            _run_full_analysis()

    with col2:
        if st.button(
            "📤  Upload New Resume",
            width="stretch"
        ):
            # Clear session state
            for key in list(st.session_state.keys()):
                if key != "initialized":
                    st.session_state.pop(key, None)
            st.rerun()

    with col3:
        if st.button(
            "📊  View Dashboard",
            width="stretch"
        ):
            st.info(
                "Navigate to Dashboard from the sidebar."
            )

    # Show analysis status if already run
    if st.session_state.get("full_analysis_complete"):
        st.divider()
        st.success(
            "✅ Full analysis complete! Navigate to "
            "**Analysis**, **Dashboard**, or **Reports** "
            "from the sidebar to view results."
        )


def _run_full_analysis() -> None:
    """Run the complete agent pipeline."""
    from app.orchestrator.workflow import AgentOrchestrator

    resume_text = st.session_state.get("resume_text", "")
    if not resume_text:
        st.error("No resume text available.")
        return

    orchestrator = AgentOrchestrator()
    progress_bar = st.progress(0, text="Starting analysis...")

    def on_progress(step: int, total: int, msg: str):
        progress_bar.progress(
            step / total, text=msg
        )

    try:
        results = orchestrator.run_full_analysis(
            resume_text=resume_text,
            target_role=st.session_state.get(
                "target_role", "General Technology Role"
            ),
            candidate_id=st.session_state.get(
                "candidate_id", ""
            ),
            candidate_name=st.session_state.get(
                "candidate_name", ""
            ),
            progress_callback=on_progress,
        )

        progress_bar.progress(1.0, text="Analysis complete!")

        # Store all results in session state
        st.session_state["full_analysis_complete"] = True
        st.session_state["analysis_results"] = results

        # Store individual results for page access
        resume_result = results.get("resume_result") or {}
        if resume_result.get("success"):
            st.session_state["resume_parsed"] = True
            st.session_state["parsed_resume"] = (
                resume_result.get("parsed_resume", {})
            )

        for key in [
            "ats_result", "skill_result",
            "skill_gap_result", "job_matching_result",
            "interview_result", "risk_result",
            "recommendation_result", "ranking_result",
            "reflection_result",
        ]:
            if results.get(key):
                st.session_state[key] = results[key]

        st.success(
            f"✅ Full analysis complete in "
            f"{results.get('total_time_seconds', 0):.1f}s! "
            f"Navigate to other pages to see results."
        )

    except Exception as exc:
        progress_bar.empty()
        st.error(f"❌ Analysis failed: {str(exc)}")
        logger.error("Full analysis error: %s", exc)