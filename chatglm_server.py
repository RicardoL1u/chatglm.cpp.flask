import chatglm_cpp
print('hello!!!!!!!!!!!')
pipline = chatglm_cpp.Pipeline("chatglm2-ggml.bin")

# pipline.chat(['hi'])


# use flask to create a web server
# import flask
from flask import request, jsonify,Flask


# create a Flask app
app = Flask(__name__)

# create a URL route in our chat application for "/chat"
# the input would be the prompt a string, and history a list of strings
@app.route('/chat', methods=['GET', 'POST'])
def chat():
    prompt = request.json['prompt']
    history = request.json['history']
    if history is None:
        history = []
    history.append(prompt)
    print(history)
    print(prompt)
    response = pipline.chat(
        history,
    )
    history.append(response)
    print(response)
    return {
        'response': response,
        'history': history,
    }
    
# run the Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
    
# give me a test with curl, run the following command in terminal
# curl -X POST -H "Content-Type: application/json" -d '{"prompt":"hello", "history":[]}' http://localhost:5000/chat