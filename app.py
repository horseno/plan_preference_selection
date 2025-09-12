from flask import Flask, render_template, request, jsonify
import pandas as pd
import os
import utils
import ast  # Import module to safely parse the string list

app = Flask(__name__)

# Load the spreadsheet
### modify input data file as needed

DATA_FILE = os.environ.get('DATA_FILE', 'input/pilot.csv')
SHOW_REWRITE = True

input_name = os.path.basename(DATA_FILE).split('.')[0]

user_name = os.environ.get("USER", os.environ.get("USERNAME"))

SELECTIONS_FILE = f"aug_{input_name}_selections_{user_name}.csv"

out_path = "output"

if not os.path.exists(out_path):
    os.makedirs(out_path)  # Creates the folder if it doesn't exist

output_path = os.path.join(out_path, SELECTIONS_FILE)
if not os.path.exists(output_path):
    pd.DataFrame(columns=["index", "choice"]).to_csv(output_path, index=False)


df = pd.read_csv(DATA_FILE)
selections = []


@app.route("/")
def index():
    return render_template("index.html", total=len(df), show_rewrite=SHOW_REWRITE)


@app.route("/get_row/<int:row_id>")
def get_row(row_id):
    if row_id >= len(df):
        return jsonify({"done": True})

    row = df.iloc[row_id]
    conversation_str = row["conversation"]

    # Convert string representation of list to actual list
    try:
        conversation_list = ast.literal_eval(
            conversation_str
        )  # Safely parse string into list
    except (SyntaxError, ValueError):
        conversation_list = ["Error parsing conversation"]
    diagramA = utils.convert_to_markdown(row["planA"])
    diagramB = utils.convert_to_markdown(row["planB"])

    if row["shuffle_key"] == "A":
        rewriteA = row["rewrite1"]
        rewriteB = row["rewrite2"]
    else: 
        rewriteA = row["rewrite2"]
        rewriteB = row["rewrite1"]

    return jsonify(
        {
            "index": row_id,
            "conversation": conversation_list,
            "imageA": diagramA,
            "imageB": diagramB,
            "rewriteA": rewriteA,
            "rewriteB": rewriteB,
        }
    )


@app.route("/select", methods=["POST"])
def select():
    data = request.json
    row_id = data["index"]
    choice = data["choice"]

    # Save selection to CSV immediately
    new_selection = pd.DataFrame([[row_id, choice]], columns=["index", "choice"])
    new_selection.to_csv(output_path, mode="a", header=False, index=False)

    return jsonify({"success": True})


if __name__ == "__main__":
    app.run(debug=True)
