from flask import Flask, request, jsonify, render_template
import translater

app = Flask(__name__)

@app.route('/ask')
def ask():
    return render_template('translater_ui.html')

@app.route('/chat/<user_input>')
def chat(user_input):
    translated_data = translater.translate(user_input)
    return jsonify({'sentence': translated_data})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)