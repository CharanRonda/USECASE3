from flask import Flask, render_template, request, send_file
import agents
import pandas as pd

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/input")
def input_page():
    return render_template("input.html")


@app.route("/predict", methods=["POST"])
def predict():

    premium = int(request.form["premium"])
    accidents = int(request.form["accidents"])
    age = int(request.form["age"])
    miles = int(request.form["miles"])

    risk = agents.risk_profiler(accidents)
    conversion = agents.conversion_predictor()
    advice = agents.premium_advisor(premium)
    decision = agents.decision_router(risk, conversion)

    # Save result for download
    df = pd.DataFrame({
        "Risk":[risk],
        "Conversion":[conversion],
        "Advice":[advice],
        "Decision":[decision]
    })

    df.to_csv("result.csv", index=False)

    return render_template(
        "result.html",
        risk=risk,
        conversion=conversion,
        advice=advice,
        decision=decision
    )


@app.route("/download")
def download():
    return send_file("result.csv", as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
