import reflex as rx
from business_analytics_dashboard.states.dashboard_state import DashboardState


def section_title(title: str, subtitle: str = "") -> rx.Component:
    return rx.vstack(
        rx.text(title, font_size="16px", font_weight="700", color="white"),
        rx.cond(
            subtitle != "",
            rx.text(subtitle, font_size="12px", color="#64748b"),
            rx.fragment(),
        ),
        spacing="1",
        align="start",
        margin_bottom="16px",
    )


def top_categories_chart() -> rx.Component:
    return rx.box(
        section_title("Top 15 Categorias", "Por receita no período"),
        rx.recharts.bar_chart(
            rx.recharts.bar(
                data_key="total_revenue",
                name="Receita (R$)",
                fill="#34d399",
                radius=[0, 4, 4, 0],
            ),
            rx.recharts.x_axis(
                type_="number",
                stroke="#475569",
                tick={"fill": "#94a3b8", "fontSize": 10},
                tick_line=False,
                axis_line=False,
            ),
            rx.recharts.y_axis(
                type_="category",
                data_key="product_category",
                stroke="#475569",
                tick={"fill": "#94a3b8", "fontSize": 10},
                tick_line=False,
                axis_line=False,
                width=160,
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
            data=DashboardState.top_categories,
            layout="vertical",
            height=420,
            width="100%",
        ),
        background="#1e293b",
        border_radius="12px",
        border="1px solid #334155",
        padding="20px",
    )


def top_sellers_chart() -> rx.Component:
    return rx.box(
        section_title("Top 15 Sellers", "Por receita no período"),
        rx.recharts.bar_chart(
            rx.recharts.bar(
                data_key="total_revenue",
                name="Receita (R$)",
                fill="#60a5fa",
                radius=[0, 4, 4, 0],
            ),
            rx.recharts.x_axis(
                type_="number",
                stroke="#475569",
                tick={"fill": "#94a3b8", "fontSize": 10},
                tick_line=False,
                axis_line=False,
            ),
            rx.recharts.y_axis(
                type_="category",
                data_key="seller_id",
                stroke="#475569",
                tick={"fill": "#94a3b8", "fontSize": 10},
                tick_line=False,
                axis_line=False,
                width=100,
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
            data=DashboardState.top_sellers,
            layout="vertical",
            height=420,
            width="100%",
        ),
        background="#1e293b",
        border_radius="12px",
        border="1px solid #334155",
        padding="20px",
    )