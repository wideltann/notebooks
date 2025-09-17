# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo==0.13.15",
#     "altair==4.2.0",
#     "pandas==2.3.0",
#     "numpy==2.3.0"
# ]
# ///
import marimo

__generated_with = "0.10.9"
app = marimo.App(width="medium")

with app.setup:
    import numpy as np
    import altair as alt
    import pandas as pd
    import marimo as mo


@app.cell
def _():
    mo.md(
        """
        # Interactive Data Visualization

        <img src="public/logo.png" width="200" />

        This notebook demonstrates a simple interactive visualization using Altair.
        Try selecting the points!
        """
    )
    return


@app.cell
def _():
    # Create sample data
    data = pd.DataFrame({"x": np.arange(100), "y": np.random.normal(0, 1, 100)})

    # Create interactive chart
    chart = mo.ui.altair_chart(
        (
            alt.Chart(data)
            .mark_circle()
            .encode(x="x", y="y", size=alt.value(100), color=alt.value("steelblue"))
            .properties(height=400, title="Interactive Scatter Plot")
        )
    )
    chart
    return chart


@app.cell
def _(chart):
    chart.value
    return


if __name__ == "__main__":
    app.run()
