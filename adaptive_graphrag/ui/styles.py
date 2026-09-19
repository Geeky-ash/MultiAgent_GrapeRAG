"""Enterprise Dark Theme Styles and Custom CSS Tokens for Streamlit Console."""

CUSTOM_CSS = """
<style>
    /* Global Theme Overrides */
    .stApp {
        background-color: #0D1117;
        color: #F0F6FC;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }

    /* Top Telemetry Header */
    .telemetry-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding-bottom: 12px;
        margin-bottom: 16px;
        border-bottom: 1px solid #30363D;
    }
    .telemetry-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(99, 102, 241, 0.12);
        border: 1px solid #6366F1;
        color: #818CF8;
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }
    .pulse-dot {
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background-color: #10B981;
        box-shadow: 0 0 8px #10B981;
    }

    /* KPI Telemetry Cards (Left Column) */
    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 8px;
        margin-bottom: 14px;
    }
    .kpi-card {
        background: #161B22;
        border: 1px solid #30363D;
        border-radius: 8px;
        padding: 10px 12px;
    }
    .kpi-label {
        font-size: 10px;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        color: #8B949E;
        font-weight: 600;
    }
    .kpi-value {
        font-size: 18px;
        font-weight: 700;
        color: #F0F6FC;
        margin-top: 2px;
    }

    /* Dynamic Modality Glow Badges */
    .badge-vector {
        background: rgba(16, 185, 129, 0.15);
        border: 1px solid #10B981;
        color: #34D399;
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: 700;
        font-size: 12px;
        box-shadow: 0 0 10px rgba(16, 185, 129, 0.3);
    }
    .badge-graph {
        background: rgba(6, 182, 212, 0.15);
        border: 1px solid #06B6D4;
        color: #38BDF8;
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: 700;
        font-size: 12px;
        box-shadow: 0 0 10px rgba(6, 182, 212, 0.3);
    }
    .badge-hybrid {
        background: rgba(139, 92, 246, 0.15);
        border: 1px solid #8B5CF6;
        color: #A78BFA;
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: 700;
        font-size: 12px;
        box-shadow: 0 0 10px rgba(139, 92, 246, 0.3);
    }

    /* Response Card (Right Column Top) */
    .response-card {
        background: #161B22;
        border: 1px solid #30363D;
        border-left: 4px solid #6366F1;
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 16px;
        font-size: 14px;
        line-height: 1.6;
        color: #F0F6FC;
    }

    /* Step Tracker */
    .step-tracker {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: #161B22;
        border: 1px solid #30363D;
        border-radius: 8px;
        padding: 10px 14px;
        margin-bottom: 12px;
    }
    .step-item {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 2px;
    }
    .step-title {
        font-size: 11px;
        font-weight: 600;
        color: #C9D1D9;
    }
    .step-time {
        font-size: 10px;
        color: #58A6FF;
        font-family: monospace;
    }
    .step-arrow {
        color: #484F58;
        font-size: 14px;
    }
</style>
"""
