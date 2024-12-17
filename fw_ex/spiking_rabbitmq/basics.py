from flask import Flask, request, render_template_string
from producer import send_task

app = Flask(__name__)

html_template = """
<!DOCTYPE html>
<html>
    <head>
        <title>Spiking RabbitMQ</title>
    </head>
    <body>
        <h1>Spiking RabbitMQ</h1>
        <form action="/" method="post">
            <label for="message">Message:</label>
            <input type="text" name="message" id="message" required>
            <button type="submit">Submit Message</button>
        </form>
        <p><strong>Message:</strong> {% if message %}{{ message }}{% endif %}</strong></p>
    </body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def submit_message():
    message = None
    if request.method == "POST":
        message = request.form["message"]
        send_task(message)
        message = f"Sent {message}"
    return render_template_string(html_template, message=message)


if __name__ == "__main__":
    app.run(debug=True)
