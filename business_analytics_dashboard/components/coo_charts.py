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


def orders_volume_chart() -> rx.Component:
    return rx.box(
        chart_header("Volume de Pedidos", "Total por status"),
        rx.recharts.area_chart(
            rx.recharts.area(data_key="total_orders",    name="Total",    stroke="#60a5fa", stroke_width=2, fill="#60a5fa", fill_opacity=0.12, dot=False),
            rx.recharts.area(data_key="delivered_orders",name="Entregues",stroke="#34d399", stroke_width=2, fill="#34d399", fill_opacity=0.12, dot=False),
            rx.recharts.area(data_key="failed_orders",   name="Falhas",   stroke="#f43f5e", stroke_width=1, fill="#f43f5e", fill_opacity=0.08, dot=False),
            rx.recharts.x_axis(data_key="purchase_date", stroke="#475569", tick={"fill":"#94a3b8","fontSize":11}, tick_line=False, axis_line=False, interval="preserveStartEnd"),
            rx.recharts.y_axis(stroke="#475569", tick={"fill":"#94a3b8","fontSize":11}, tick_line=False, axis_line=False, width=50),
            rx.recharts.cartesian_grid(stroke_dasharray="3 3", stroke="#334155"),
            rx.recharts.legend(wrapper_style={"paddingTop":"12px"}, icon_type="circle", icon_size=8),
            rx.recharts.graphing_tooltip(content_style={"backgroundColor":"#1e293b","border":"1px solid #334155","borderRadius":"8px","color":"#f1f5f9","fontSize":"12px"}),
            data=DashboardState.orders_volume_agg,
            height=280, width="100%",
        ),
        background="#1e293b", border_radius="12px", border="1px solid #334155", padding="20px",
    )


def delivery_breakdown_chart() -> rx.Component:
    return rx.box(
        chart_header("Tempo de Entrega", "Média de dias por etapa"),
        rx.recharts.bar_chart(
            rx.recharts.bar(data_key="days_to_approval", name="Aprovação", fill="#a78bfa", stack_id="a"),
            rx.recharts.bar(data_key="days_to_post",     name="Postagem",  fill="#60a5fa", stack_id="a"),
            rx.recharts.bar(data_key="days_to_customer", name="Entrega",   fill="#34d399", stack_id="a"),
            rx.recharts.x_axis(data_key="purchase_date", stroke="#475569", tick={"fill":"#94a3b8","fontSize":11}, tick_line=False, axis_line=False, interval="preserveStartEnd"),
            rx.recharts.y_axis(stroke="#475569", tick={"fill":"#94a3b8","fontSize":11}, tick_line=False, axis_line=False, width=40),
            rx.recharts.cartesian_grid(stroke_dasharray="3 3", stroke="#334155"),
            rx.recharts.legend(wrapper_style={"paddingTop":"12px"}, icon_type="circle", icon_size=8),
            rx.recharts.graphing_tooltip(content_style={"backgroundColor":"#1e293b","border":"1px solid #334155","borderRadius":"8px","color":"#f1f5f9","fontSize":"12px"}),
            data=DashboardState.delivery_breakdown_agg,
            height=280, width="100%",
        ),
        background="#1e293b", border_radius="12px", border="1px solid #334155", padding="20px",
    )