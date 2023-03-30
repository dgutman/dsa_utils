### Attempting to interview a basic data view component that allows me to quickly
## View a set of thumbnail images
import dash_mantine_components as dmc
from dash import dcc, html
import dash_bootstrap_components as dbc


style = {
    "border": f"1px solid {dmc.theme.DEFAULT_COLORS['indigo'][4]}",
    "textAlign": "center",
    "width": 200,
    "height": 200,
}


def generate_dataview_components(componentId="image=grid"):
    ## Max value needs to be set based on the number of elements in the dataframe
    ## So need to bind that..

    sg = html.Div(
        [
            dbc.Pagination(
                id="image-grid-pager",
                max_value=10,
                fully_expanded=False,
                first_last=True,
                previous_next=True,
                style={"visibility": "hidden"},
            ),
            dmc.SimpleGrid(
                cols=5,
                spacing="sm",
                id=componentId,
                breakpoints=[
                    {"maxWidth": 980, "cols": 3, "spacing": "md"},
                    {"maxWidth": 755, "cols": 2, "spacing": "sm"},
                    {"maxWidth": 600, "cols": 1, "spacing": "sm"},
                ],
                children=[
                    # This is where the images get dumped
                    html.Div(" "),
                ],
            ),
        ]
    )
    return sg


# , style=style NO STYLING ON LOAD
