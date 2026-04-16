import reflex as rx


def kpi_card(
    title: str,
    value: rx.Var,
    subtitle: str = "",
    icon: str = "",
    accent_color: str = "emerald",
    prefix: str = "",
    suffix: str = "",
) -> rx.Component:
    accent_colors = {
        "emerald": "#34d399",
        "blue":    "#60a5fa",
        "amber":   "#f59e0b",
        "rose":    "#f43f5e",
        "violet":  "#a78bfa",
    }
    color = accent_colors.get(accent_color, "#34d399")

    return rx.box(
        # Barra lateral colorida
        rx.box(
            width="4px",
            height="100%",
            background=color,
            position="absolute",
            left="0",
            top="0",
            border_radius="8px 0 0 8px",
        ),
        # Conteúdo
        rx.box(
            # Header
            rx.hstack(
                rx.cond(icon != "", rx.text(icon, font_size="18px"), rx.fragment()),
                rx.text(
                    title,
                    font_size="11px",
                    font_weight="600",
                    letter_spacing="0.1em",
                    text_transform="uppercase",
                    color="#94a3b8",
                ),
                spacing="2",
                align="center",
                margin_bottom="10px",
            ),
            # Valor — usa flex nativo via rx.box para align="flex-end"
            rx.box(
                rx.cond(
                    prefix != "",
                    rx.text(
                        prefix,
                        font_size="13px",
                        font_weight="500",
                        color=color,
                        padding_bottom="4px",
                    ),
                    rx.fragment(),
                ),
                rx.text(value, font_size="28px", font_weight="700", color="white", line_height="1"),
                rx.cond(
                    suffix != "",
                    rx.text(
                        suffix,
                        font_size="13px",
                        font_weight="500",
                        color=color,
                        padding_bottom="4px",
                    ),
                    rx.fragment(),
                ),
                display="flex",
                flex_direction="row",
                align_items="flex-end",
                gap="4px",
            ),
            # Subtítulo
            rx.cond(
                subtitle != "",
                rx.text(subtitle, font_size="11px", color="#64748b", margin_top="6px"),
                rx.fragment(),
            ),
            padding="16px 20px",
        ),
        position="relative",
        background="#1e293b",
        border_radius="12px",
        border="1px solid #334155",
        overflow="hidden",
        _hover={
            "border_color": "#475569",
            "transform": "translateY(-2px)",
            "box_shadow": "0 8px 24px rgba(0,0,0,0.3)",
        },
        transition="all 0.2s ease",
    )


def kpi_grid(*cards) -> rx.Component:
    return rx.grid(
        *cards,
        columns=rx.breakpoints(initial="1", sm="2", lg="3", xl="5"),
        spacing="4",
        margin_bottom="32px",
    )