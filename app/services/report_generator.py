"""
TalentMind AI - PDF Report Generator
======================================
Generates professional PDF reports using ReportLab.

Author  : TalentMind AI Team
Version : 1.0.0
"""

from __future__ import annotations

import logging
from datetime import datetime
from io import BytesIO
from pathlib import Path
from typing import Any, Dict, List, Optional

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch, mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
    HRFlowable,
)

from app.core.settings import get_settings

logger = logging.getLogger(__name__)
cfg = get_settings()


class ReportGenerator:
    """
    Generates professional PDF career analysis reports.

    Supports multiple report types:
        - Full Analysis Report
        - Resume Analysis Report
        - Skill Gap Report
        - Career Guidance Report
        - Interview Prep Guide
    """

    def __init__(self) -> None:
        self._styles = getSampleStyleSheet()
        self._setup_custom_styles()

    def _setup_custom_styles(self) -> None:
        """Define custom paragraph styles for the report."""
        self._styles.add(ParagraphStyle(
            name="ReportTitle",
            parent=self._styles["Title"],
            fontSize=24,
            spaceAfter=20,
            textColor=colors.HexColor("#2563EB"),
        ))
        self._styles.add(ParagraphStyle(
            name="SectionHeader",
            parent=self._styles["Heading1"],
            fontSize=16,
            spaceBefore=20,
            spaceAfter=10,
            textColor=colors.HexColor("#1E293B"),
        ))
        self._styles.add(ParagraphStyle(
            name="SubHeader",
            parent=self._styles["Heading2"],
            fontSize=13,
            spaceBefore=12,
            spaceAfter=6,
            textColor=colors.HexColor("#374151"),
        ))
        self._styles.add(ParagraphStyle(
            name="BodyText2",
            parent=self._styles["Normal"],
            fontSize=10,
            spaceBefore=4,
            spaceAfter=4,
            leading=14,
        ))
        self._styles.add(ParagraphStyle(
            name="MetricLabel",
            parent=self._styles["Normal"],
            fontSize=9,
            textColor=colors.HexColor("#64748B"),
        ))
        self._styles.add(ParagraphStyle(
            name="MetricValue",
            parent=self._styles["Normal"],
            fontSize=14,
            textColor=colors.HexColor("#2563EB"),
            alignment=TA_CENTER,
        ))
        self._styles.add(ParagraphStyle(
            name="Footer",
            parent=self._styles["Normal"],
            fontSize=8,
            textColor=colors.HexColor("#94A3B8"),
            alignment=TA_CENTER,
        ))

    def generate_full_report(
        self,
        candidate_name: str,
        analysis_data: Dict[str, Any],
    ) -> bytes:
        """
        Generate a complete career analysis PDF report.

        Args:
            candidate_name: Name of the candidate
            analysis_data: All analysis results combined

        Returns:
            bytes: PDF file content
        """
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=20 * mm,
            leftMargin=20 * mm,
            topMargin=25 * mm,
            bottomMargin=20 * mm,
        )

        elements: List = []

        # Title Page
        elements.extend(self._build_title_page(
            candidate_name, analysis_data
        ))
        elements.append(PageBreak())

        # Resume Analysis Section
        resume_data = analysis_data.get("resume_result") or {}
        if resume_data.get("success"):
            elements.extend(
                self._build_resume_section(resume_data)
            )
            elements.append(PageBreak())

        # ATS Analysis Section
        ats_data = analysis_data.get("ats_result") or {}
        if ats_data.get("success"):
            elements.extend(self._build_ats_section(ats_data))
            elements.append(PageBreak())

        # Skill Analysis Section
        skill_data = analysis_data.get("skill_result") or {}
        if skill_data.get("success"):
            elements.extend(
                self._build_skill_section(skill_data)
            )

        # Skill Gap Section
        gap_data = analysis_data.get("skill_gap_result") or {}
        if gap_data.get("success"):
            elements.extend(
                self._build_skill_gap_section(gap_data)
            )
            elements.append(PageBreak())

        # Risk Analysis Section
        risk_data = analysis_data.get("risk_result") or {}
        if risk_data.get("success"):
            elements.extend(
                self._build_risk_section(risk_data)
            )

        # Recommendations Section
        rec_data = analysis_data.get(
            "recommendation_result"
        ) or {}
        if rec_data.get("success"):
            elements.extend(
                self._build_recommendations_section(rec_data)
            )

        # Footer
        elements.append(Spacer(1, 30))
        elements.append(HRFlowable(
            width="100%", thickness=1,
            color=colors.HexColor("#E2E8F0")
        ))
        elements.append(Spacer(1, 10))
        elements.append(Paragraph(
            f"Generated by TalentMind AI on "
            f"{datetime.now().strftime('%B %d, %Y at %I:%M %p')}",
            self._styles["Footer"]
        ))

        doc.build(elements)
        pdf_bytes = buffer.getvalue()
        buffer.close()

        logger.info(
            "PDF report generated | size=%d bytes",
            len(pdf_bytes)
        )
        return pdf_bytes

    def save_report(
        self,
        pdf_bytes: bytes,
        candidate_id: str,
        report_type: str = "full_report",
    ) -> str:
        """
        Save PDF report to disk.

        Args:
            pdf_bytes: PDF content
            candidate_id: Candidate UUID
            report_type: Type of report

        Returns:
            str: Path to saved file
        """
        reports_dir = cfg.reports_dir_path
        reports_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{report_type}_{candidate_id[:8]}_{timestamp}.pdf"
        filepath = reports_dir / filename

        filepath.write_bytes(pdf_bytes)
        logger.info("Report saved | path=%s", filepath)
        return str(filepath)

    def _build_title_page(
        self,
        candidate_name: str,
        analysis_data: Dict[str, Any],
    ) -> List:
        """Build the title/cover page elements."""
        elements = []
        elements.append(Spacer(1, 60))
        elements.append(Paragraph(
            "TalentMind AI",
            self._styles["ReportTitle"]
        ))
        elements.append(Paragraph(
            "Career Analysis Report",
            self._styles["SectionHeader"]
        ))
        elements.append(Spacer(1, 30))
        elements.append(HRFlowable(
            width="100%", thickness=2,
            color=colors.HexColor("#2563EB")
        ))
        elements.append(Spacer(1, 30))

        # Candidate info
        elements.append(Paragraph(
            f"<b>Candidate:</b> {candidate_name or 'Not specified'}",
            self._styles["BodyText2"]
        ))
        elements.append(Paragraph(
            f"<b>Date:</b> {datetime.now().strftime('%B %d, %Y')}",
            self._styles["BodyText2"]
        ))

        target_role = analysis_data.get(
            "target_role", "General Technology Role"
        )
        elements.append(Paragraph(
            f"<b>Target Role:</b> {target_role}",
            self._styles["BodyText2"]
        ))
        elements.append(Spacer(1, 40))

        # Key metrics summary
        ats_score = (
            analysis_data.get("ats_result") or {}
        ).get("ats_score", "N/A")
        readiness = (
            analysis_data.get("skill_gap_result") or {}
        ).get("overall_readiness_score", "N/A")
        risk_level = (
            analysis_data.get("risk_result") or {}
        ).get("overall_risk_level", "N/A")

        metrics_data = [
            ["ATS Score", "Readiness", "Risk Level"],
            [
                str(ats_score),
                str(readiness),
                str(risk_level),
            ],
        ]
        metrics_table = Table(
            metrics_data,
            colWidths=[150, 150, 150],
        )
        metrics_table.setStyle(TableStyle([
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTSIZE", (0, 0), (-1, 0), 9),
            ("TEXTCOLOR", (0, 0), (-1, 0),
             colors.HexColor("#64748B")),
            ("FONTSIZE", (0, 1), (-1, 1), 18),
            ("TEXTCOLOR", (0, 1), (-1, 1),
             colors.HexColor("#2563EB")),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
            ("TOPPADDING", (0, 1), (-1, 1), 4),
            ("GRID", (0, 0), (-1, -1), 0.5,
             colors.HexColor("#E2E8F0")),
        ]))
        elements.append(metrics_table)

        return elements

    def _build_resume_section(
        self, data: Dict[str, Any]
    ) -> List:
        """Build the resume analysis section."""
        elements = []
        elements.append(Paragraph(
            "Resume Analysis", self._styles["SectionHeader"]
        ))
        elements.append(HRFlowable(
            width="100%", thickness=1,
            color=colors.HexColor("#E2E8F0")
        ))

        parsed = data.get("parsed_resume") or {}
        contact = parsed.get("contact_info") or {}

        if contact:
            elements.append(Paragraph(
                "Contact Information",
                self._styles["SubHeader"]
            ))
            info_items = [
                f"<b>Name:</b> {contact.get('name', 'N/A')}",
                f"<b>Email:</b> {contact.get('email', 'N/A')}",
                f"<b>Phone:</b> {contact.get('phone', 'N/A')}",
            ]
            for item in info_items:
                elements.append(Paragraph(
                    item, self._styles["BodyText2"]
                ))

        skills_count = data.get("skills_count", 0)
        exp_count = data.get("experience_count", 0)
        edu_count = data.get("education_count", 0)

        elements.append(Spacer(1, 10))
        elements.append(Paragraph(
            "Profile Summary", self._styles["SubHeader"]
        ))
        elements.append(Paragraph(
            f"Skills Identified: {skills_count} | "
            f"Experience Entries: {exp_count} | "
            f"Education: {edu_count}",
            self._styles["BodyText2"]
        ))

        return elements

    def _build_ats_section(
        self, data: Dict[str, Any]
    ) -> List:
        """Build the ATS analysis section."""
        elements = []
        elements.append(Paragraph(
            "ATS Compatibility Analysis",
            self._styles["SectionHeader"]
        ))
        elements.append(HRFlowable(
            width="100%", thickness=1,
            color=colors.HexColor("#E2E8F0")
        ))

        score = data.get("ats_score", 0)
        label = data.get("score_label", "N/A")
        elements.append(Paragraph(
            f"Overall Score: <b>{score}/100</b> ({label})",
            self._styles["BodyText2"]
        ))
        elements.append(Spacer(1, 10))

        # Score breakdown table
        breakdown = data.get("score_breakdown") or {}
        if breakdown:
            elements.append(Paragraph(
                "Score Breakdown", self._styles["SubHeader"]
            ))
            table_data = [["Category", "Score"]]
            for cat, val in breakdown.items():
                display_cat = cat.replace("_", " ").title()
                table_data.append([display_cat, f"{val}/100"])

            t = Table(table_data, colWidths=[300, 100])
            t.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0),
                 colors.HexColor("#F1F5F9")),
                ("FONTSIZE", (0, 0), (-1, -1), 10),
                ("GRID", (0, 0), (-1, -1), 0.5,
                 colors.HexColor("#E2E8F0")),
                ("PADDING", (0, 0), (-1, -1), 6),
            ]))
            elements.append(t)

        # Suggestions
        suggestions = data.get("ats_suggestions") or []
        if suggestions:
            elements.append(Spacer(1, 10))
            elements.append(Paragraph(
                "Improvement Suggestions",
                self._styles["SubHeader"]
            ))
            for i, s in enumerate(suggestions[:5], 1):
                elements.append(Paragraph(
                    f"{i}. {s}", self._styles["BodyText2"]
                ))

        return elements

    def _build_skill_section(
        self, data: Dict[str, Any]
    ) -> List:
        """Build the skill analysis section."""
        elements = []
        elements.append(Paragraph(
            "Skill Analysis", self._styles["SectionHeader"]
        ))
        elements.append(HRFlowable(
            width="100%", thickness=1,
            color=colors.HexColor("#E2E8F0")
        ))

        top_skills = data.get("top_skills") or []
        if top_skills:
            elements.append(Paragraph(
                "Top Skills Identified",
                self._styles["SubHeader"]
            ))
            for skill in top_skills[:10]:
                if isinstance(skill, dict):
                    name = skill.get("skill", "")
                    level = skill.get("proficiency", "")
                    elements.append(Paragraph(
                        f"- {name} ({level})",
                        self._styles["BodyText2"]
                    ))
                elif isinstance(skill, str):
                    elements.append(Paragraph(
                        f"- {skill}",
                        self._styles["BodyText2"]
                    ))

        return elements

    def _build_skill_gap_section(
        self, data: Dict[str, Any]
    ) -> List:
        """Build the skill gap analysis section."""
        elements = []
        elements.append(Paragraph(
            "Skill Gap Analysis",
            self._styles["SectionHeader"]
        ))
        elements.append(HRFlowable(
            width="100%", thickness=1,
            color=colors.HexColor("#E2E8F0")
        ))

        score = data.get("overall_readiness_score", 0)
        label = data.get("readiness_label", "N/A")
        elements.append(Paragraph(
            f"Readiness Score: <b>{score}/100</b> ({label})",
            self._styles["BodyText2"]
        ))

        gaps = data.get("skill_gaps") or []
        if gaps:
            elements.append(Spacer(1, 10))
            elements.append(Paragraph(
                "Identified Gaps", self._styles["SubHeader"]
            ))
            table_data = [["Skill", "Priority", "Reason"]]
            for gap in gaps[:8]:
                if isinstance(gap, dict):
                    table_data.append([
                        gap.get("skill", ""),
                        gap.get("priority", "").upper(),
                        gap.get("reason", "")[:50],
                    ])
            if len(table_data) > 1:
                t = Table(
                    table_data,
                    colWidths=[150, 80, 230]
                )
                t.setStyle(TableStyle([
                    ("BACKGROUND", (0, 0), (-1, 0),
                     colors.HexColor("#F1F5F9")),
                    ("FONTSIZE", (0, 0), (-1, -1), 9),
                    ("GRID", (0, 0), (-1, -1), 0.5,
                     colors.HexColor("#E2E8F0")),
                    ("PADDING", (0, 0), (-1, -1), 5),
                ]))
                elements.append(t)

        return elements

    def _build_risk_section(
        self, data: Dict[str, Any]
    ) -> List:
        """Build the risk analysis section."""
        elements = []
        elements.append(Paragraph(
            "Risk Analysis", self._styles["SectionHeader"]
        ))
        elements.append(HRFlowable(
            width="100%", thickness=1,
            color=colors.HexColor("#E2E8F0")
        ))

        level = data.get("overall_risk_level", "N/A")
        score = data.get("overall_risk_score", 0)
        elements.append(Paragraph(
            f"Overall Risk: <b>{level}</b> (Score: {score}/100)",
            self._styles["BodyText2"]
        ))

        categories = data.get("risk_categories") or []
        if categories:
            elements.append(Spacer(1, 10))
            elements.append(Paragraph(
                "Risk Categories", self._styles["SubHeader"]
            ))
            for cat in categories[:5]:
                if isinstance(cat, dict):
                    elements.append(Paragraph(
                        f"<b>{cat.get('category', '')}:</b> "
                        f"{cat.get('description', '')}",
                        self._styles["BodyText2"]
                    ))

        mitigation = data.get("mitigation_plan") or []
        if mitigation:
            elements.append(Spacer(1, 10))
            elements.append(Paragraph(
                "Mitigation Plan", self._styles["SubHeader"]
            ))
            for item in mitigation[:5]:
                if isinstance(item, dict):
                    elements.append(Paragraph(
                        f"- [{item.get('priority', '')}] "
                        f"{item.get('action', '')} "
                        f"({item.get('timeline', '')})",
                        self._styles["BodyText2"]
                    ))

        return elements

    def _build_recommendations_section(
        self, data: Dict[str, Any]
    ) -> List:
        """Build the recommendations section."""
        elements = []
        elements.append(Paragraph(
            "Career Recommendations",
            self._styles["SectionHeader"]
        ))
        elements.append(HRFlowable(
            width="100%", thickness=1,
            color=colors.HexColor("#E2E8F0")
        ))

        # Career paths
        paths = data.get("career_paths") or []
        if paths:
            elements.append(Paragraph(
                "Recommended Career Paths",
                self._styles["SubHeader"]
            ))
            for path in paths[:5]:
                if isinstance(path, dict):
                    elements.append(Paragraph(
                        f"<b>{path.get('role', '')}</b> "
                        f"(Fit: {path.get('fit_score', 0)}%) "
                        f"- {path.get('timeline', '')}",
                        self._styles["BodyText2"]
                    ))

        # Immediate actions
        actions = data.get("immediate_actions") or []
        if actions:
            elements.append(Spacer(1, 10))
            elements.append(Paragraph(
                "Immediate Actions",
                self._styles["SubHeader"]
            ))
            for action in actions[:5]:
                if isinstance(action, dict):
                    elements.append(Paragraph(
                        f"- [{action.get('priority', '')}] "
                        f"{action.get('action', '')} "
                        f"({action.get('timeline', '')})",
                        self._styles["BodyText2"]
                    ))

        return elements
