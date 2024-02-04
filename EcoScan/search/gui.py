from dash import Dash, html, dcc, Input, Output, State
from dash_camera import DccCamera
from dash.exceptions import PreventUpdate
import gpt
import brandclassifier as bc

external_stylesheets = [
    {"rel": "stylesheet", "href": "assets/styles.css"},
]

app = Dash(__name__, external_stylesheets=external_stylesheets)
app.css.config.serve_locally = True

# Function to get the GPT response
def get_gpt_response(query):
    try:
        response = gpt.get_gpt_response(query)
        return response
    except Exception as e:
        return f"Error: {str(e)}"

app.layout = html.Div(
    id="main-div",
    children=[
        html.H1("EcoScan", id="main-title"),
        html.Div(
            id="search-div",
            children=[
                dcc.Input(id="query-input", type="text", placeholder="Enter brand name..."),
                html.Button("Submit", id="submit-button"),
                dcc.Upload(
                    id="upload-data",
                    children=html.Div([
                        'Drag and Drop or ',
                        html.A('Select Files')
                    ]),
                    multiple=False,
                ),
                dcc.Camera(
                    id="camera",
                    audio=False,
                    width=640,
                    height=480,
                    screenshot_format="jpeg",
                ),
                dcc.Loading(
                    id="loading-output",
                    type="circle",
                    children=[
                        html.Div(
                            id="response-div",
                            children=[
                                html.P(id="output-text")
                            ]
                        )
                    ]
                ),
            ]
        ),
    ]
)

@app.callback(
    Output("output-text", "children"),
    [Input("submit-button", "n_clicks")],
    [State("query-input", "value"), State("upload-data", "contents"), State("camera", "screenshot")],
    prevent_initial_call=True,
)
def update_output(n_clicks, query, uploaded_image, camera_screenshot):
    if n_clicks is None:
        raise PreventUpdate

    if not query and not uploaded_image and not camera_screenshot:
        return "Please enter a query, upload an image, or take a picture."

    if camera_screenshot:
        query = bc.get_brand_from_uploaded_image(camera_screenshot)
    elif uploaded_image:
        query = bc.get_brand_from_uploaded_image(uploaded_image)

    response = get_gpt_response(query)
    return response

if __name__ == "__main__":
    app.run_server(host='0.0.0.0', port=8050)
