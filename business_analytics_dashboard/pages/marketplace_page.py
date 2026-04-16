import reflex as rx
from business_analytics_dashboard.states.dashboard_state import DashboardState
from business_analytics_dashboard.components.kpi_card import kpi_card, kpi_grid
from business_analytics_dashboard.components.marketplace_charts import top_categories_chart, top_sellers_chart
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
        rx.box(height="480px", background="#334155", border_radius="12px"),
        rx.box(height="480px", background="#334155", border_radius="12px"),
        columns=rx.breakpoints(initial="1", xl="2"),
        spacing="4",
    )


def _top_category_banner() -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.text("🏆", font_size="20px"),
            rx.vstack(
                rx.text("Categoria Líder no Período",
                        font_size="11px", font_weight="600",
                        text_transform="uppercase", letter_spacing="0.08em",
                        color="#64748b"),
                rx.text(
                    DashboardState.marketplace_kpis["top_category"],
                    font_size="18px", font_weight="700", color="#f59e0b",
                ),
                spacing="1",
                align="start",
            ),
            spacing="3",
            align="center",
        ),
        background="#1e293b",
        border="1px solid #334155",
        border_left="4px solid #f59e0b",
        border_radius="10px",
        padding="14px 18px",
        margin_bottom="32px",
    )


def marketplace_page() -> rx.Component:
    return rx.box(
        # ── Cabeçalho ────────────────────────────────────────────────────
        rx.hstack(
            rx.hstack(
                rx.text("🏪", font_size="24px"),
                rx.vstack(
                    rx.text("Marketplace Dashboard", font_size="22px", font_weight="700",
                            color="white", line_height="1"),
                    rx.text("Sellers & Categorias", font_size="13px",
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

        # ── KPI Cards ────────────────────────────────────────────────────
        rx.cond(
            DashboardState.loading,
            _skeleton_cards(4),
            kpi_grid(
                kpi_card(
                    title="Total de Sellers",
                    value=DashboardState.marketplace_kpis["total_sellers"],
                    subtitle="Vendedores ativos no período",
                    icon="🏪",
                    accent_color="emerald",
                ),
                kpi_card(
                    title="Receita Total",
                    value=DashboardState.marketplace_kpis["total_revenue"],
                    subtitle="Soma dos itens vendidos",
                    icon="💵",
                    accent_color="blue",
                    prefix="R$",
                ),
                kpi_card(
                    title="Ticket Médio",
                    value=DashboardState.marketplace_kpis["avg_ticket"],
                    subtitle="Receita por pedido",
                    icon="🎯",
                    accent_color="violet",
                    prefix="R$",
                ),
                kpi_card(
                    title="Frete Médio",
                    value=DashboardState.marketplace_kpis["avg_freight"],
                    subtitle="Por item vendido",
                    icon="🚚",
                    accent_color="amber",
                    prefix="R$",
                ),
            ),
        ),

        # ── Banner: Top categoria ─────────────────────────────────────────
        rx.cond(
            DashboardState.loading,
            rx.box(height="60px", background="#334155", border_radius="10px",
                   margin_bottom="32px"),
            _top_category_banner(),
        ),

        # ── Divisor ───────────────────────────────────────────────────────
        rx.hstack(
            rx.text("RANKING DO PERÍODO", font_size="11px", font_weight="600",
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
                top_categories_chart(),
                top_sellers_chart(),
                columns=rx.breakpoints(initial="1", xl="2"),
                spacing="4",
            ),
        ),

        padding="24px",
        background="#0f172a",
        min_height="100vh",
        width="100%",
        on_mount=[DashboardState.set_current_page('marketplace'), DashboardState.fetch_marketplace_data],
    )