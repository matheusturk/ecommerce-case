import reflex as rx
from business_analytics_dashboard.states.dashboard_state import DashboardState


def _preset_button(label: str, preset: str) -> rx.Component:
    is_active = DashboardState.active_preset == preset
    return rx.box(
        rx.text(label, font_size="12px", font_weight="500"),
        on_click=DashboardState.set_preset(preset),
        cursor="pointer",
        padding="6px 14px",
        border_radius="6px",
        border=rx.cond(is_active, "1px solid #34d399", "1px solid #334155"),
        background=rx.cond(is_active, "#064e3b", "#1e293b"),
        color=rx.cond(is_active, "#34d399", "#94a3b8"),
        _hover={"border_color": "#34d399", "color": "#34d399"},
        transition="all 0.15s ease",
        white_space="nowrap",
    )


def _divider() -> rx.Component:
    return rx.box(width="1px", height="28px", background="#334155", margin="0 4px")


def date_filter() -> rx.Component:
    return rx.box(
        rx.hstack(
            # ── Presets ──────────────────────────────────────────────────
            rx.hstack(
                _preset_button("1 mês",       "1m"),
                _preset_button("3 meses",     "3m"),
                _preset_button("6 meses",     "6m"),
                _preset_button("Todo período","all"),
                spacing="2",
                align="center",
            ),
            _divider(),
            # ── Custom range ─────────────────────────────────────────────
            rx.hstack(
                rx.text("De", font_size="12px", color="#64748b"),
                rx.el.input(
                    type="date",
                    value=DashboardState.date_start,
                    on_change=DashboardState.set_date_start,
                    style={
                        "background":   "#1e293b",
                        "border":       "1px solid #334155",
                        "borderRadius": "6px",
                        "color":        "#e2e8f0",
                        "fontSize":     "12px",
                        "padding":      "5px 10px",
                        "outline":      "none",
                        "cursor":       "pointer",
                        "colorScheme":  "dark",
                    },
                ),
                rx.text("até", font_size="12px", color="#64748b"),
                rx.el.input(
                    type="date",
                    value=DashboardState.date_end,
                    on_change=DashboardState.set_date_end,
                    style={
                        "background":   "#1e293b",
                        "border":       "1px solid #334155",
                        "borderRadius": "6px",
                        "color":        "#e2e8f0",
                        "fontSize":     "12px",
                        "padding":      "5px 10px",
                        "outline":      "none",
                        "cursor":       "pointer",
                        "colorScheme":  "dark",
                    },
                ),
                spacing="2",
                align="center",
            ),
            spacing="3",
            align="center",
            flex_wrap="wrap",
        ),
        background="#0f172a",
        border="1px solid #334155",
        border_radius="10px",
        padding="12px 16px",
        margin_bottom="28px",
    )