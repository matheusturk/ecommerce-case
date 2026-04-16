import reflex as rx
from business_analytics_dashboard.components.sidebar import sidebar
from business_analytics_dashboard.pages.cfo_page import cfo_page
from business_analytics_dashboard.pages.coo_page import coo_page
from business_analytics_dashboard.pages.cs_page import cs_page
from business_analytics_dashboard.pages.marketplace_page import marketplace_page


def layout(content: rx.Component) -> rx.Component:
    return rx.hstack(
        sidebar(),
        rx.box(content, flex="1", overflow_y="auto"),
        spacing="0",
        align="start",
        width="100%",
        min_height="100vh",
        background="#0f172a",
    )


def cfo_route()         -> rx.Component: return layout(cfo_page())
def coo_route()         -> rx.Component: return layout(coo_page())
def cs_route()          -> rx.Component: return layout(cs_page())
def marketplace_route() -> rx.Component: return layout(marketplace_page())


app = rx.App(
    theme=rx.theme(appearance="dark"),
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap",
    ],
)

app.add_page(cfo_route,         route="/")
app.add_page(cfo_route,         route="/cfo")
app.add_page(coo_route,         route="/coo")
app.add_page(cs_route,          route="/cx")
app.add_page(marketplace_route, route="/marketplace")