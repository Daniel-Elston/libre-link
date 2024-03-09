from __future__ import annotations

import pandas as pd
from flask import Flask
from flask import render_template
from visualise import plots

from database.database_management import DatabaseManagement
from utils.setup_env import setup_project_env

# Environment setup
project_dir, config, setup_logs, db_config = setup_project_env()

app = Flask(__name__)


@app.route('/')
def plot():
    database_manager = DatabaseManagement(db_config)
    data = database_manager.fetch_data()
    df = pd.json_normalize(data)
    df.set_index('timestamp', inplace=True)

    # Generate the plot and get HTML div
    plot_div = plots(df, to_html=True)

    # Pass the plot HTML div to the template correctly
    return render_template("index.html", plot=plot_div)


if __name__ == "__main__":
    app.run(debug=True)
