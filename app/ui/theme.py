"""
TalentMind AI - Modern UI Theme
================================
Custom CSS and styling for a modern dark-themed UI.

Author  : TalentMind AI Team
Version : 2.0.0
"""

from __future__ import annotations

import streamlit as st


def inject_custom_css() -> None:
    """Injects global custom CSS for modern dark theme."""
    st.markdown("""
    <style>
    /* ── Global Overrides ────────────────────────────────── */
    .stApp {
        background: linear-gradient(180deg, #0E1117 0%, #131720 100%);
    }

    /* ── Sidebar ─────────────────────────────────────────── */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #131720 0%, #1A1F2E 100%);
        border-right: 1px solid rgba(108, 99, 255, 0.2);
    }

    [data-testid="stSidebar"] .stRadio > label {
        font-size: 0.9rem;
    }

    /* ── Cards ────────────────────────────────────────────── */
    .modern-card {
        background: linear-gradient(135deg, #1A1F2E 0%, #1E2435 100%);
        border: 1px solid rgba(108, 99, 255, 0.15);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .modern-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 32px rgba(108, 99, 255, 0.15);
    }

    .glass-card {
        background: rgba(26, 31, 46, 0.7);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 1.2rem;
        margin: 0.5rem 0;
    }

    /* ── Metric Cards ─────────────────────────────────────── */
    .metric-card {
        background: linear-gradient(135deg, #1A1F2E 0%, #222840 100%);
        border: 1px solid rgba(108, 99, 255, 0.2);
        border-radius: 12px;
        padding: 1.2rem;
        text-align: center;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #6C63FF, #48B8D0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0.3rem 0;
    }
    .metric-label {
        font-size: 0.85rem;
        color: #8892A4;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .metric-delta {
        font-size: 0.8rem;
        color: #48D0A0;
    }

    /* ── Score Ring ────────────────────────────────────────── */
    .score-ring {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }
    .score-number {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #6C63FF, #48B8D0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .score-label {
        font-size: 1rem;
        color: #8892A4;
    }
    .score-sublabel {
        font-size: 0.8rem;
        color: #5A6478;
    }

    /* ── Gradient Text ─────────────────────────────────────── */
    .gradient-text {
        background: linear-gradient(135deg, #6C63FF, #48B8D0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
    }
    .gradient-text-warm {
        background: linear-gradient(135deg, #FF6B6B, #FFA07A);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
    }
    .gradient-text-green {
        background: linear-gradient(135deg, #48D0A0, #4FC3F7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
    }

    /* ── Section Headers ───────────────────────────────────── */
    .section-header {
        font-size: 1.3rem;
        font-weight: 600;
        color: #E0E0E0;
        margin: 1.5rem 0 0.8rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid rgba(108, 99, 255, 0.3);
    }

    /* ── Tags/Chips ────────────────────────────────────────── */
    .skill-tag {
        display: inline-block;
        background: rgba(108, 99, 255, 0.15);
        border: 1px solid rgba(108, 99, 255, 0.3);
        color: #B8B0FF;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        margin: 0.2rem;
    }
    .skill-tag-success {
        background: rgba(72, 208, 160, 0.15);
        border: 1px solid rgba(72, 208, 160, 0.3);
        color: #48D0A0;
    }
    .skill-tag-warning {
        background: rgba(255, 183, 77, 0.15);
        border: 1px solid rgba(255, 183, 77, 0.3);
        color: #FFB74D;
    }
    .skill-tag-danger {
        background: rgba(255, 107, 107, 0.15);
        border: 1px solid rgba(255, 107, 107, 0.3);
        color: #FF6B6B;
    }

    /* ── Progress Bar ──────────────────────────────────────── */
    .progress-container {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        height: 10px;
        overflow: hidden;
        margin: 0.5rem 0;
    }
    .progress-fill {
        height: 100%;
        border-radius: 10px;
        background: linear-gradient(90deg, #6C63FF, #48B8D0);
        transition: width 0.5s ease;
    }

    /* ── Hero Section ──────────────────────────────────────── */
    .hero-section {
        background: linear-gradient(135deg, #1A1F2E 0%, #252B3F 50%, #1A1F2E 100%);
        border: 1px solid rgba(108, 99, 255, 0.2);
        border-radius: 20px;
        padding: 3rem 2rem;
        text-align: center;
        margin: 1rem 0 2rem 0;
        position: relative;
        overflow: hidden;
    }
    .hero-section::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle at 30% 70%, rgba(108, 99, 255, 0.05) 0%, transparent 50%);
    }
    .hero-title {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #6C63FF, #48B8D0, #6C63FF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    .hero-subtitle {
        font-size: 1.1rem;
        color: #8892A4;
        max-width: 600px;
        margin: 0 auto;
    }

    /* ── Feature Cards ─────────────────────────────────────── */
    .feature-card {
        background: linear-gradient(135deg, #1A1F2E 0%, #1E2435 100%);
        border: 1px solid rgba(108, 99, 255, 0.15);
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        height: 100%;
        transition: all 0.3s;
    }
    .feature-card:hover {
        border-color: rgba(108, 99, 255, 0.4);
        transform: translateY(-3px);
        box-shadow: 0 12px 40px rgba(108, 99, 255, 0.1);
    }
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 0.8rem;
    }
    .feature-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #E0E0E0;
        margin-bottom: 0.5rem;
    }
    .feature-desc {
        font-size: 0.85rem;
        color: #8892A4;
        line-height: 1.5;
    }

    /* ── Stat Pills ────────────────────────────────────────── */
    .stat-pill {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: rgba(108, 99, 255, 0.1);
        border: 1px solid rgba(108, 99, 255, 0.2);
        border-radius: 24px;
        padding: 0.5rem 1rem;
        margin: 0.3rem;
    }
    .stat-pill-number {
        font-weight: 700;
        color: #6C63FF;
    }
    .stat-pill-label {
        color: #8892A4;
        font-size: 0.85rem;
    }

    /* ── Buttons ───────────────────────────────────────────── */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #6C63FF, #5A52E0) !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        transition: all 0.3s !important;
    }
    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, #7B73FF, #6C63FF) !important;
        box-shadow: 0 4px 20px rgba(108, 99, 255, 0.3) !important;
    }

    /* ── Dividers ──────────────────────────────────────────── */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(108, 99, 255, 0.3), transparent);
        margin: 1.5rem 0;
    }

    /* ── Expanders ─────────────────────────────────────────── */
    .streamlit-expanderHeader {
        background: rgba(26, 31, 46, 0.5) !important;
        border-radius: 8px !important;
    }

    /* ── Step Indicators ───────────────────────────────────── */
    .step-item {
        display: flex;
        align-items: flex-start;
        gap: 1rem;
        margin: 1rem 0;
    }
    .step-number {
        min-width: 32px;
        height: 32px;
        background: linear-gradient(135deg, #6C63FF, #48B8D0);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: 700;
        font-size: 0.85rem;
    }
    .step-content {
        flex: 1;
    }
    .step-title {
        font-weight: 600;
        color: #E0E0E0;
    }
    .step-desc {
        font-size: 0.85rem;
        color: #8892A4;
    }
    </style>
    """, unsafe_allow_html=True)


def render_metric_card(label: str, value: str, delta: str = "") -> str:
    """Returns HTML for a modern metric card."""
    delta_html = f'<div class="metric-delta">{delta}</div>' if delta else ""
    return f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        {delta_html}
    </div>
    """


def render_score_ring(score: float, label: str, sublabel: str = "") -> str:
    """Returns HTML for a score display."""
    sublabel_html = f'<div class="score-sublabel">{sublabel}</div>' if sublabel else ""
    return f"""
    <div class="score-ring">
        <div class="score-number">{score:.0f}</div>
        <div class="score-label">{label}</div>
        {sublabel_html}
    </div>
    """


def render_skill_tags(skills: list, tag_class: str = "skill-tag") -> str:
    """Returns HTML for skill tags."""
    tags = "".join(f'<span class="{tag_class}">{s}</span>' for s in skills)
    return f'<div style="margin: 0.5rem 0;">{tags}</div>'
