import os
from model.chatbot.kogpt2 import chatbot as ch_kogpt2
from model.chatbot.kobert import chatbot as ch_kobert
from flask import Flask, request, jsonify
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

headers = {'Content-Type': 'application/json; charset=utf-8'}


@app.route('/')
def hello():
    return "ChatBot server running"

@app.route('/chatbot/g')
def reactChatbotV1():
    sentence = request.args.get("s")
    if sentence is None or len(sentence) == 0 or sentence == '\n':
        return jsonify({
            "answer": "듣고 있어요. 더 말씀해주세요~ (끄덕끄덕)"
        })

    answer = ch_kogpt2.predict(sentence)
    print(answer)

    return jsonify({
        "answer": answer
    })


@app.route('/chatbot/b')
def reactChatbotV2():
    sentence = request.args.get("s")
    if sentence is None or len(sentence) == 0 or sentence == '\n':
        return jsonify({
            "answer": "듣고 있어요. 더 말씀해주세요~ (끄덕끄덕)"
        })

    answer, category, desc, softmax = ch_kobert.chat(sentence)
    print(answer)
    return jsonify({
        "answer": answer,
        "category": category,
        "category_info": desc
    })


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
