"""
TalentMind AI - PDF Report Agent
==================================
Agent 11: Coordinates report generation by gathering
all analysis results and producing PDF reports.

Responsibilities:
    - Collect all analysis results
    - Determine report sections
    - Invoke ReportGenerator
    - Save report to DB

Author  : TalentMind AI Team
Version : 1.0.0
"""

from __future__ import annotations

import logging
from typing import Any, Dict

from app.core.constants import AgentName

logger = logging.getLogger(__name__)


class PDFReportAgent:
    """
    Agent 11 - PDF Report Generation Agent

    Unlike other agents, this one doesn't call the LLM.
    It orchestrates the ReportGenerator service to produce
    PDF reports from analysis results.

    Input:
        candidate_name : str
        candidate_id   : str
        analysis_data  : dict (all agent results)
        report_type    : str

    Output:
        success      : bool
        report_path  : str
        report_bytes : bytes
        error        : str or None
    """

    def __init__(self) -> None:
        self.agent_name = AgentName.PDF_REPORT
        self._logger = logging.getLogger(
            f"agents.{self.agent_name}"
        )
        self._generator = None

    def _get_generator(self):
        """Lazy-load the report generator."""
        if self._generator is None:
            from app.services.report_generator import (
                ReportGenerator,
            )
            self._generator = ReportGenerator()
        return self._generator

    def run(
        self,
        input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate PDF report from analysis results.

        Args:
            input_data: {
                candidate_name: str
                candidate_id  : str
                analysis_data : dict
                report_type   : str (default: "full_report")
            }

        Returns:
            dict with success, report_path, report_bytes
        """
        self._logger.info("PDFReportAgent started")

        candidate_name = input_data.get(
            "candidate_name", "Unknown"
        )
        candidate_id = input_data.get("candidate_id", "")
        analysis_data = input_data.get("analysis_data") or {}
        report_type = input_data.get(
            "report_type", "full_report"
        )

        if not analysis_data:
            return {
                "success": False,
                "error": "No analysis data provided.",
                "report_path": "",
                "report_bytes": b"",
            }

        try:
            generator = self._get_generator()

            pdf_bytes = generator.generate_full_report(
                candidate_name=candidate_name,
                analysis_data=analysis_data,
            )

            report_path = generator.save_report(
                pdf_bytes=pdf_bytes,
                candidate_id=candidate_id,
                report_type=report_type,
            )

            self._logger.info(
                "Report generated | path=%s | size=%d",
                report_path, len(pdf_bytes)
            )

            return {
                "success": True,
                "error": None,
                "report_path": report_path,
                "report_bytes": pdf_bytes,
                "report_type": report_type,
            }

        except Exception as exc:
            self._logger.error(
                "Report generation failed: %s", exc
            )
            return {
                "success": False,
                "error": str(exc),
                "report_path": "",
                "report_bytes": b"",
            }
