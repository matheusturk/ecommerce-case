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


def revenue_chart() -> rx.Component:
    return rx.box(
        chart_header("Receita ao Longo do Tempo", "Receita bruta agregada"),
        rx.recharts.area_chart(
            rx.recharts.area(
                data_key="gross_revenue",
                stroke="#34d399",
                stroke_width=2,
                fill="#34d399",
                fill_opacity=0.15,
                dot=False,
                is_animation_active=True,
            ),
            rx.recharts.x_axis(
                data_key="order_date",
                stroke="#475569",
                tick={"fill": "#94a3b8", "fontSize": 11},
                tick_line=False,
                axis_line=False,
                interval="preserveStartEnd",
            ),
            rx.recharts.y_axis(
                stroke="#475569",
                tick={"fill": "#94a3b8", "fontSize": 11},
                tick_line=False,
                axis_line=False,
                width=70,
            ),
            rx.recharts.cartesian_grid(stroke_dasharray="3 3", stroke="#334155"),
            rx.recharts.graphing_tooltip(
                content_style={
                    "backgroundColor": "#1e293b",
                    "border": "1px solid #334155",
                    "borderRadius": "8px",
                    "color": "#f1f5f9",
                    "fontSize": "12px",
                },
            ),
            data=DashboardState.revenue_over_time_agg,
            height=280,
            width="100%",
        ),
        background="#1e293b",
        border_radius="12px",
        border="1px solid #334155",
        padding="20px",
    )


def payment_distribution_chart() -> rx.Component:
    return rx.box(
        chart_header("Distribuição de Pagamentos", "Por tipo de método de pagamento"),
        rx.recharts.bar_chart(
            rx.recharts.bar(data_key="credit_card", name="Cartão de Crédito", fill="#34d399", stack_id="a"),
            rx.recharts.bar(data_key="boleto",       name="Boleto",            fill="#60a5fa", stack_id="a"),
            rx.recharts.bar(data_key="voucher",      name="Voucher",           fill="#f59e0b", stack_id="a"),
            rx.recharts.bar(data_key="debit_card",   name="Débito",            fill="#f472b6", stack_id="a"),
            rx.recharts.x_axis(
                data_key="order_date",
                stroke="#475569",
                tick={"fill": "#94a3b8", "fontSize": 11},
                tick_line=False,
                axis_line=False,
                interval="preserveStartEnd",
            ),
            rx.recharts.y_axis(
                stroke="#475569",
                tick={"fill": "#94a3b8", "fontSize": 11},
                tick_line=False,
                axis_line=False,
                width=60,
            ),
            rx.recharts.cartesian_grid(stroke_dasharray="3 3", stroke="#334155"),
            rx.recharts.legend(wrapper_style={"paddingTop": "12px"}, icon_type="circle", icon_size=8),
            rx.recharts.graphing_tooltip(
                content_style={
                    "backgroundColor": "#1e293b",
                    "border": "1px solid #334155",
                    "borderRadius": "8px",
                    "color": "#f1f5f9",
                    "fontSize": "12px",
                },
            ),
            data=DashboardState.payment_distribution_agg,
            height=280,
            width="100%",
        ),
        background="#1e293b",
        border_radius="12px",
        border="1px solid #334155",
        padding="20px",
    )