import reflex as rx
from business_analytics_dashboard.states.dashboard_state import DashboardState
from business_analytics_dashboard.components.kpi_card import kpi_card, kpi_grid
from business_analytics_dashboard.components.cs_charts import reviews_trend_chart, reviews_distribution_chart
from business_analytics_dashboard.components.date_filter import date_filter


def _skeleton_cards(n: int = 4) -> rx.Component:
    return rx.grid(
        *[rx.box(height="112px", background="#334155", border_radius="12px") for _ in range(n)],
        columns=rx.breakpoints(initial="1", sm="2", xl="4"),
        spacing="4",
        margin_bottom="32px",
    )


def _skeleton_charts() -> rx.Component:
    return rx.grid(
        rx.box(height="340px", background="#334155", border_radius="12px"),
        rx.box(height="340px", background="#334155", border_radius="12px"),
        columns=rx.breakpoints(initial="1", xl="2"),
        spacing="4",
    )


def _score_badge(label: str, value: rx.Var, color: str, icon: str, sublabel: str) -> rx.Component:
    """Card destacado com nota em destaque e barra de progresso visual."""
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.text(icon, font_size="20px"),
                rx.vstack(
                    rx.text(label, font_size="11px", font_weight="600",
                            text_transform="uppercase", letter_spacing="0.08em", color="#64748b"),
                    rx.text(sublabel, font_size="10px", color="#475569"),
                    spacing="0",
                    align="start",
                ),
                spacing="2",
                align="center",
            ),
            rx.hstack(
                rx.text(value, font_size="36px", font_weight="800", color=color, line_height="1"),
                rx.text("/ 5", font_size="14px", color="#475569", align_self="flex-end",
                        padding_bottom="4px"),
                spacing="1",
                display="flex",
                align_items="flex-end",
            ),
            spacing="3",
            align="start",
        ),
        background="#1e293b",
        border="1px solid #334155",
        border_top=f"3px solid {color}",
        border_radius="12px",
        padding="18px 20px",
        _hover={"border_color": color, "box_shadow": f"0 0 20px {color}22"},
        transition="all 0.2s ease",
    )


def cs_page() -> rx.Component:
    return rx.box(
        # ── Cabeçalho ────────────────────────────────────────────────────
        rx.hstack(
            rx.hstack(
                rx.text("⭐", font_size="24px"),
                rx.vstack(
                    rx.text("CS Dashboard", font_size="22px", font_weight="700",
                            color="white", line_height="1"),
                    rx.text("Customer Experience & Reviews", font_size="13px",
                            color="#64748b", line_height="1"),
                    spacing="1",
                    align="start",
                ),
                spacing="3",
                align="center",
            ),
            rx.box(
                rx.text("Olist · 2016–2018", font_size="11px", color="#64748b"),
                background="#1e293b",
                border="1px solid #334155",
                border_radius="999px",
                padding="4px 12px",
            ),
            justify="between",
            align="center",
            margin_bottom="24px",
        ),

        # ── Filtro de data ────────────────────────────────────────────────
        date_filter(),

        # ── Score cards em destaque ───────────────────────────────────────
        rx.cond(
            DashboardState.loading,
            rx.grid(
                *[rx.box(height="120px", background="#334155", border_radius="12px") for _ in range(4)],
                columns=rx.breakpoints(initial="1", sm="2", xl="4"),
                spacing="4",
                margin_bottom="32px",
            ),
            rx.grid(
                _score_badge(
                    label="Nota Média Geral",
                    value=DashboardState.cs_kpis["avg_review_score"],
                    color="#f59e0b",
                    icon="⭐",
                    sublabel="Todos os pedidos entregues",
                ),
                _score_badge(
                    label="Total de Reviews",
                    value=DashboardState.cs_kpis["total_reviews"],
                    color="#60a5fa",
                    icon="💬",
                    sublabel="Reviews com nota",
                ),
                _score_badge(
                    label="Nota — No Prazo",
                    value=DashboardState.cs_kpis["avg_score_on_time"],
                    color="#34d399",
                    icon="✅",
                    sublabel="Entregas dentro do prazo",
                ),
                _score_badge(
                    label="Nota — Atrasado",
                    value=DashboardState.cs_kpis["avg_score_late"],
                    color="#f43f5e",
                    icon="⏰",
                    sublabel="Entregas com atraso",
                ),
                columns=rx.breakpoints(initial="1", sm="2", xl="4"),
                spacing="4",
                margin_bottom="32px",
            ),
        ),

        # ── Insight de impacto do atraso ──────────────────────────────────
        rx.cond(
            DashboardState.loading,
            rx.fragment(),
            rx.box(
                rx.hstack(
                    rx.text("💡", font_size="16px"),
                    rx.text(
                        "Impacto do atraso na satisfação: pedidos atrasados têm nota média ",
                        font_size="13px", color="#94a3b8",
                    ),
                    rx.text(
                        DashboardState.cs_kpis["avg_score_late"],
                        font_size="13px", font_weight="700", color="#f43f5e",
                    ),
                    rx.text(
                        " vs ",
                        font_size="13px", color="#64748b",
                    ),
                    rx.text(
                        DashboardState.cs_kpis["avg_score_on_time"],
                        font_size="13px", font_weight="700", color="#34d399",
                    ),
                    rx.text(
                        " nos pedidos no prazo.",
                        font_size="13px", color="#94a3b8",
                    ),
                    spacing="1",
                    align="center",
                    flex_wrap="wrap",
                ),
                background="#1e293b",
                border="1px solid #334155",
                border_left="4px solid #f59e0b",
                border_radius="10px",
                padding="12px 16px",
                margin_bottom="32px",
            ),
        ),

        # ── Divisor ───────────────────────────────────────────────────────
        rx.hstack(
            rx.text("ANÁLISE TEMPORAL", font_size="11px", font_weight="600",
                    letter_spacing="0.1em", color="#475569"),
            rx.box(flex="1", height="1px", background="#334155", margin_left="12px"),
            align="center",
            margin_bottom="24px",
        ),

        # ── Gráficos ─────────────────────────────────────────────────────
        rx.cond(
            DashboardState.loading,
            _skeleton_charts(),
            rx.grid(
                reviews_trend_chart(),
                reviews_distribution_chart(),
                columns=rx.breakpoints(initial="1", xl="2"),
                spacing="4",
            ),
        ),

        padding="24px",
        background="#0f172a",
        min_height="100vh",
        width="100%",
        on_mount=[DashboardState.set_current_page('cs'), DashboardState.fetch_cs_data],
    )