from flask import Flask, request, jsonify
import pickle

app = Flask(__name__)

# Load model
model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

@app.route("/")
def home():
    return "Spam Detection API Running"

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    text = data["text"]

    vect = vectorizer.transform([text])
    prediction = model.predict(vect)[0]

    return jsonify({"prediction": prediction})

if __name__ == "__main__":
    app.run(debug=True, port=5000)