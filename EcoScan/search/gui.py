from dash import Dash, html, dcc, Input, Output, State
import gpt

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
                dcc.Input(id="query-input", type="text", placeholder="Enter query..."),
                html.Button("Submit", id="submit-button"),
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
    [State("query-input", "value")],
    prevent_initial_call=True,
)
def update_output(n_clicks, query):
    if n_clicks is not None:
        if query:
            response = get_gpt_response(query)
            return response
        else:
            return "Please enter a query."
    else:
        return ""


if __name__ == "__main__":
     app.run_server(host = '0.0.0.0', port=8050)

