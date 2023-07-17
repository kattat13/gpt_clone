from flask import Flask, render_template, request
import openai
import os
from dotenv import load_dotenv


app = Flask(__name__)
load_dotenv()

api_key = os.getenv("OPENAI_KEY", None)


def talking(prompt):
    response = openai.Completion.create(
        model = 'text-davinci-003',
        prompt = prompt,
        max_tokens = 2048
    )
    return response.choices[0].text


def drawing(prompt):
    response = openai.Image.create(
        size = '512x512',
        prompt = prompt,
        n = 1,
        response_format = 'url'
    )
    return response['data'][0]['url']


@app.route("/", methods=["GET", "POST"])
def chatbot():

    if request.method == "POST" and api_key is not None:
        openai.api_key = api_key
        question = request.form['user_input']
        if question[0:4] == 'img:':
            question = question.replace('img:', '')
            answer = drawing(question)

            return render_template("index.html", ai_answer = answer, drawing=True)
        else:
            answer = talking(question)
            return render_template("index.html", ai_answer = answer)

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
