import reflex as rx
from business_analytics_dashboard.states.dashboard_state import DashboardState
from business_analytics_dashboard.components.kpi_card import kpi_card, kpi_grid
from business_analytics_dashboard.components.cfo_charts import revenue_chart, payment_distribution_chart
from business_analytics_dashboard.components.date_filter import date_filter


def _skeleton_cards() -> rx.Component:
    return rx.grid(
        *[rx.box(height="112px", background="#334155", border_radius="12px") for _ in range(5)],
        columns=rx.breakpoints(initial="1", sm="2", lg="3", xl="5"),
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


def cfo_page() -> rx.Component:
    return rx.box(
        # ── Cabeçalho ────────────────────────────────────────────────────
        rx.hstack(
            rx.hstack(
                rx.text("💰", font_size="24px"),
                rx.vstack(
                    rx.text("CFO Dashboard", font_size="22px", font_weight="700", color="white", line_height="1"),
                    rx.text("Visão financeira consolidada", font_size="13px", color="#64748b", line_height="1"),
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

        # ── KPI Cards ────────────────────────────────────────────────────
        rx.cond(
            DashboardState.loading,
            _skeleton_cards(),
            kpi_grid(
                kpi_card(
                    title="Receita Total",
                    value=DashboardState.cfo_kpis["total_revenue"],
                    subtitle="Receita bruta acumulada",
                    icon="💵",
                    accent_color="emerald",
                    prefix="R$",
                ),
                kpi_card(
                    title="Total de Pedidos",
                    value=DashboardState.cfo_kpis["total_orders"],
                    subtitle="Pedidos aprovados",
                    icon="📦",
                    accent_color="blue",
                ),
                kpi_card(
                    title="Ticket Médio",
                    value=DashboardState.cfo_kpis["avg_ticket"],
                    subtitle="Por pedido aprovado",
                    icon="🎯",
                    accent_color="violet",
                    prefix="R$",
                ),
                kpi_card(
                    title="Total Reembolsado",
                    value=DashboardState.cfo_kpis["total_refunded"],
                    subtitle="Cancelados/indisponíveis",
                    icon="↩️",
                    accent_color="rose",
                    prefix="R$",
                ),
                kpi_card(
                    title="Taxa de Reembolso",
                    value=DashboardState.cfo_kpis["refund_rate"],
                    subtitle="% da receita bruta",
                    icon="⚠️",
                    accent_color="amber",
                    suffix="%",
                ),
            ),
        ),

        # ── Divisor ───────────────────────────────────────────────────────
        rx.hstack(
            rx.text(
                "ANÁLISE TEMPORAL",
                font_size="11px",
                font_weight="600",
                letter_spacing="0.1em",
                color="#475569",
            ),
            rx.box(flex="1", height="1px", background="#334155", margin_left="12px"),
            align="center",
            margin_bottom="24px",
        ),

        # ── Gráficos ─────────────────────────────────────────────────────
        rx.cond(
            DashboardState.loading,
            _skeleton_charts(),
            rx.grid(
                revenue_chart(),
                payment_distribution_chart(),
                columns=rx.breakpoints(initial="1", xl="2"),
                spacing="4",
            ),
        ),

        padding="24px",
        background="#0f172a",
        min_height="100vh",
        width="100%",
        on_mount=[DashboardState.set_current_page('cfo'), DashboardState.fetch_cfo_data],
    )