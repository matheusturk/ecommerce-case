import reflex as rx
from business_analytics_dashboard.states.dashboard_state import DashboardState
from business_analytics_dashboard.components.granularity_toggle import granularity_toggle


def chart_header(title: str, subtitle: str = "") -> rx.Component:
    return rx.hstack(
        rx.vstack(
            rx.text(title, font_size="16px", font_weight="700", color="white"),
            rx.cond(
                subtitle != "",
                rx.text(subtitle, font_size="12px", color="#64748b"),
                rx.fragment(),
            ),
            spacing="1",
            align="start",
        ),
        granularity_toggle(),
        justify="between",
        align="center",
        margin_bottom="16px",
    )


def reviews_trend_chart() -> rx.Component:
    return rx.box(
        chart_header("Nota Média ao Longo do Tempo", "On time vs entregas atrasadas"),
        rx.recharts.line_chart(
            rx.recharts.line(data_key="avg_score_on_time", name="No Prazo", stroke="#34d399", stroke_width=2, dot=False, connect_nulls=True),
            rx.recharts.line(data_key="avg_score_late",    name="Atrasado", stroke="#f43f5e", stroke_width=2, dot=False, connect_nulls=True),
            rx.recharts.x_axis(data_key="purchase_date", stroke="#475569", tick={"fill":"#94a3b8","fontSize":11}, tick_line=False, axis_line=False, interval="preserveStartEnd"),
            rx.recharts.y_axis(stroke="#475569", tick={"fill":"#94a3b8","fontSize":11}, tick_line=False, axis_line=False, domain=[1, 5], width=40),
            rx.recharts.cartesian_grid(stroke_dasharray="3 3", stroke="#334155"),
            rx.recharts.reference_line(y=4, stroke="#475569", stroke_dasharray="4 4", label="Meta 4.0"),
            rx.recharts.legend(wrapper_style={"paddingTop":"12px"}, icon_type="circle", icon_size=8),
            rx.recharts.graphing_tooltip(content_style={"backgroundColor":"#1e293b","border":"1px solid #334155","borderRadius":"8px","color":"#f1f5f9","fontSize":"12px"}),
            data=DashboardState.reviews_trend_agg,
            height=280, width="100%",
        ),
        background="#1e293b", border_radius="12px", border="1px solid #334155", padding="20px",
    )


def reviews_distribution_chart() -> rx.Component:
    return rx.box(
        chart_header("Distribuição de Notas", "Volume de reviews por score (1–5)"),
        rx.recharts.bar_chart(
            rx.recharts.bar(data_key="score_1", name="⭐ 1", fill="#f43f5e", stack_id="a"),
            rx.recharts.bar(data_key="score_2", name="⭐ 2", fill="#f97316", stack_id="a"),
            rx.recharts.bar(data_key="score_3", name="⭐ 3", fill="#f59e0b", stack_id="a"),
            rx.recharts.bar(data_key="score_4", name="⭐ 4", fill="#60a5fa", stack_id="a"),
            rx.recharts.bar(data_key="score_5", name="⭐ 5", fill="#34d399", stack_id="a"),
            rx.recharts.x_axis(data_key="purchase_date", stroke="#475569", tick={"fill":"#94a3b8","fontSize":11}, tick_line=False, axis_line=False, interval="preserveStartEnd"),
            rx.recharts.y_axis(stroke="#475569", tick={"fill":"#94a3b8","fontSize":11}, tick_line=False, axis_line=False, width=50),
            rx.recharts.cartesian_grid(stroke_dasharray="3 3", stroke="#334155"),
            rx.recharts.legend(wrapper_style={"paddingTop":"12px"}, icon_type="circle", icon_size=8),
            rx.recharts.graphing_tooltip(content_style={"backgroundColor":"#1e293b","border":"1px solid #334155","borderRadius":"8px","color":"#f1f5f9","fontSize":"12px"}),
            data=DashboardState.reviews_distribution_agg,
            height=280, width="100%",
        ),
        background="#1e293b", border_radius="12px", border="1px solid #334155", padding="20px",
    )