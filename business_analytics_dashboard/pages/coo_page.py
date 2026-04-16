import reflex as rx
from business_analytics_dashboard.states.dashboard_state import DashboardState
from business_analytics_dashboard.components.kpi_card import kpi_card, kpi_grid
from business_analytics_dashboard.components.coo_charts import orders_volume_chart, delivery_breakdown_chart
from business_analytics_dashboard.components.date_filter import date_filter


def _skeleton_cards(n: int = 6) -> rx.Component:
    return rx.grid(
        *[rx.box(height="112px", background="#334155", border_radius="12px") for _ in range(n)],
        columns=rx.breakpoints(initial="1", sm="2", lg="3", xl="6"),
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


def _delivery_time_cards() -> rx.Component:
    """Mini cards com o breakdown de tempo médio de entrega."""
    def time_card(label: str, value: rx.Var, color: str, icon: str) -> rx.Component:
        return rx.box(
            rx.vstack(
                rx.hstack(
                    rx.text(icon, font_size="16px"),
                    rx.text(label, font_size="11px", font_weight="600",
                            letter_spacing="0.08em", text_transform="uppercase", color="#64748b"),
                    spacing="2", align="center",
                ),
                rx.hstack(
                    rx.text(value, font_size="24px", font_weight="700", color="white"),
                    rx.text("dias", font_size="12px", color=color, align_self="flex-end",
                            padding_bottom="3px"),
                    spacing="1",
                    display="flex",
                    align_items="flex-end",
                ),
                spacing="2",
                align="start",
            ),
            background="#1e293b",
            border="1px solid #334155",
            border_left=f"4px solid {color}",
            border_radius="10px",
            padding="14px 18px",
        )

    return rx.grid(
        time_card("Aprovação",       DashboardState.coo_kpis["avg_days_to_approval"],    "#a78bfa", "📋"),
        time_card("Postagem",        DashboardState.coo_kpis["avg_days_to_post"],        "#60a5fa", "📬"),
        time_card("Entrega",         DashboardState.coo_kpis["avg_days_to_customer"],    "#34d399", "🚚"),
        time_card("Total (compra→entrega)", DashboardState.coo_kpis["avg_total_delivery_time"], "#f59e0b", "⏱️"),
        columns=rx.breakpoints(initial="1", sm="2", xl="4"),
        spacing="3",
        margin_bottom="32px",
    )


def coo_page() -> rx.Component:
    return rx.box(
        # ── Cabeçalho ────────────────────────────────────────────────────
        rx.hstack(
            rx.hstack(
                rx.text("⚙️", font_size="24px"),
                rx.vstack(
                    rx.text("COO Dashboard", font_size="22px", font_weight="700",
                            color="white", line_height="1"),
                    rx.text("Operações e logística", font_size="13px",
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

        # ── KPI Cards principais ──────────────────────────────────────────
        rx.cond(
            DashboardState.loading,
            _skeleton_cards(6),
            kpi_grid(
                kpi_card(
                    title="Total de Pedidos",
                    value=DashboardState.coo_kpis["total_orders"],
                    subtitle="Período selecionado",
                    icon="📦",
                    accent_color="blue",
                ),
                kpi_card(
                    title="Entregues",
                    value=DashboardState.coo_kpis["total_delivered"],
                    subtitle="Pedidos entregues",
                    icon="✅",
                    accent_color="emerald",
                ),
                kpi_card(
                    title="Taxa de Entrega",
                    value=DashboardState.coo_kpis["delivered_rate"],
                    subtitle="% dos pedidos",
                    icon="📈",
                    accent_color="emerald",
                    suffix="%",
                ),
                kpi_card(
                    title="Falhas",
                    value=DashboardState.coo_kpis["total_failed"],
                    subtitle="Cancelados/indisponíveis",
                    icon="❌",
                    accent_color="rose",
                ),
                kpi_card(
                    title="Taxa de Falha",
                    value=DashboardState.coo_kpis["failure_rate"],
                    subtitle="% dos pedidos",
                    icon="⚠️",
                    accent_color="amber",
                    suffix="%",
                ),
                kpi_card(
                    title="Em Progresso",
                    value=DashboardState.coo_kpis["total_in_progress"],
                    subtitle="Pedidos em andamento",
                    icon="🔄",
                    accent_color="violet",
                ),
            ),
        ),

        # ── Divisor: Tempo de entrega ─────────────────────────────────────
        rx.hstack(
            rx.text("TEMPO MÉDIO DE ENTREGA", font_size="11px", font_weight="600",
                    letter_spacing="0.1em", color="#475569"),
            rx.box(flex="1", height="1px", background="#334155", margin_left="12px"),
            align="center",
            margin_bottom="16px",
        ),

        # ── Mini cards de tempo ───────────────────────────────────────────
        rx.cond(
            DashboardState.loading,
            rx.grid(
                *[rx.box(height="80px", background="#334155", border_radius="10px") for _ in range(4)],
                columns=rx.breakpoints(initial="1", sm="2", xl="4"),
                spacing="3",
                margin_bottom="32px",
            ),
            _delivery_time_cards(),
        ),

        # ── Divisor: Análise temporal ─────────────────────────────────────
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
                orders_volume_chart(),
                delivery_breakdown_chart(),
                columns=rx.breakpoints(initial="1", xl="2"),
                spacing="4",
            ),
        ),

        padding="24px",
        background="#0f172a",
        min_height="100vh",
        width="100%",
        on_mount=[DashboardState.set_current_page('coo'), DashboardState.fetch_coo_data],
    )