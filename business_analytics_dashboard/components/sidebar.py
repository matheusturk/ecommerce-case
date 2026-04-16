import reflex as rx
from business_analytics_dashboard.states.dashboard_state import DashboardState


def nav_item(label: str, icon: str, href: str, page_key: str) -> rx.Component:
    is_active = DashboardState.current_page == page_key
    return rx.el.a(
        rx.hstack(
            rx.text(icon, font_size="16px", width="24px", text_align="center"),
            rx.text(
                label,
                font_size="14px",
                font_weight=rx.cond(is_active, "600", "500"),
            ),
            spacing="3",
            align="center",
        ),
        href=href,
        text_decoration="none",
        display="flex",
        align_items="center",
        padding="10px 16px",
        border_radius="8px",
        color=rx.cond(is_active, "#34d399", "#94a3b8"),
        background=rx.cond(is_active, "#064e3b", "transparent"),
        border=rx.cond(is_active, "1px solid #065f46", "1px solid transparent"),
        _hover={"color": "white", "background": "#1e293b"},
        transition="all 0.15s ease",
    )


def sidebar() -> rx.Component:
    return rx.box(
        # Logo
        rx.hstack(
            rx.box(
                rx.text("V", color="#34d399", font_weight="900", font_size="18px"),
                width="32px",
                height="32px",
                background="#334155",
                border_radius="8px",
                border="1px solid #475569",
                display="flex",
                align_items="center",
                justify_content="center",
            ),
            rx.vstack(
                rx.text("Volis", color="white", font_weight="700", font_size="14px", line_height="1"),
                rx.text("Analytics", color="#64748b", font_size="11px", line_height="1"),
                spacing="1",
                align="start",
            ),
            spacing="3",
            align="center",
            padding="20px 16px",
            border_bottom="1px solid #334155",
            margin_bottom="16px",
        ),
        # Label
        rx.text(
            "STAKEHOLDERS",
            font_size="10px",
            color="#475569",
            font_weight="600",
            letter_spacing="0.12em",
            padding="0 16px",
            margin_bottom="8px",
        ),
        # Nav
        rx.vstack(
            nav_item("CFO",         "💰", "/cfo",         "cfo"),
            nav_item("COO",         "⚙️",  "/coo",         "coo"),
            nav_item("CS",          "⭐", "/cx",           "cs"),
            nav_item("Marketplace", "🏪", "/marketplace", "marketplace"),
            spacing="1",
            align="stretch",
            padding="0 8px",
        ),
        # Rodapé
        rx.box(
            rx.text("Dataset: Olist 2016–2018", font_size="11px", color="#475569"),
            position="absolute",
            bottom="0",
            left="0",
            right="0",
            padding="16px",
            border_top="1px solid #334155",
        ),
        position="relative",
        width="224px",
        min_height="100vh",
        background="#0f172a",
        border_right="1px solid #334155",
        flex_shrink="0",
    )