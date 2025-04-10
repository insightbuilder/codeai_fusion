from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    bmi = None
    category = None

    if request.method == "POST":
        weight = float(request.form.get("weight", 0))
        height = float(request.form.get("height", 0)) / 100  # convert cm to meters

        if height > 0:
            bmi = round(weight / (height**2), 2)
            if bmi < 18.5:
                category = "Underweight"
            elif bmi < 25:
                category = "Normal weight"
            elif bmi < 30:
                category = "Overweight"
            else:
                category = "Obese"

    return render_template("index.html", bmi=bmi, category=category)


if __name__ == "__main__":
    app.run(debug=True)
