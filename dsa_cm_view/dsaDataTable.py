import dash_bootstrap_components as dbc
from dash import Dash, dcc, html, dash_table
import json


dsaBaseUrl = "https://styx.neurology.emory.edu/girder/api/v1"


def gen_DSA_DataTable(df, summaryColumns=[], columns_to_ignore=[], addlColSet=[]):
    """This will return a data table element that's tuned for the DSA so that the call back functions
    know how to deal with images

    addlColSet allows me to add additional graphs that live right under the data table..


    """


    rowBelowDataTable = addlColSet + [
        dbc.Col(html.Div(id="cur-hover-image"), width=2),
        dbc.Col(dbc.Row(id="datatable-interactivity-container"), width=6),
    ]
    ### TO DO: Think about the width for the interactivity container

    table = html.Div(
        [
            dbc.Accordion(
            [
            dbc.AccordionItem(dash_table.DataTable(
                id="datatable-interactivity",
                columns=[
                    {"name": i, "id": i, "deletable": False, "selectable": True}
                    for i in df.columns
                    if i not in columns_to_ignore
                ],
                data=df.to_dict("records"),
                editable=True,
                filter_action="native",
                sort_action="native",
                sort_mode="multi",
                column_selectable="single",
                row_selectable="multi",
                row_deletable=True,
                selected_columns=[],
                selected_rows=[],
                page_action="native",
                page_current=0,
                page_size=10,
            ),title="DSA DataTable")]
            ,start_collapsed=True),



            dbc.Row(rowBelowDataTable),
        ]
    )
    return table


def display_click_data(active_cell, table_data, dsaBaseUrl):
    if active_cell:
        cell = json.dumps(active_cell, indent=2)
        row = active_cell["row"]
        col = active_cell["column_id"]
        value = table_data[row][col]
        out = "%s\n%s" % (cell, value)
        imgId = table_data[row]["imageId"]
        # Create an Image From this as well
        thumbUrl = f"{dsaBaseUrl}/item/{imgId}/tiles/thumbnail"

    else:
        out = "no cell selected"
    return [json.dumps(out, indent=2), html.Img(src=thumbUrl)]
