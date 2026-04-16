import reflex as rx
from business_analytics_dashboard.states.dashboard_state import DashboardState


def granularity_toggle() -> rx.Component:
    def btn(label: str, value: str) -> rx.Component:
        is_active = DashboardState.time_granularity == value
        return rx.box(
            rx.text(label, font_size="12px", font_weight="500"),
            on_click=DashboardState.set_granularity(value),
            cursor="pointer",
            padding="5px 12px",
            border_radius="6px",
            border=rx.cond(is_active, "1px solid #475569", "1px solid transparent"),
            background=rx.cond(is_active, "#334155", "transparent"),
            color=rx.cond(is_active, "white", "#64748b"),
            _hover={"color": "white", "background": "#1e293b"},
            transition="all 0.15s ease",
        )

    return rx.hstack(
        rx.text("Ver por:", font_size="11px", color="#475569", font_weight="500"),
        rx.box(
            btn("Dia",  "day"),
            btn("Mês",  "month"),
            btn("Ano",  "year"),
            display="flex",
            flex_direction="row",
            background="#0f172a",
            border="1px solid #334155",
            border_radius="8px",
            padding="3px",
            gap="2px",
        ),
        spacing="2",
        align="center",
    )