# app.py
from flask import Flask, render_template, request
import pickle

# Initialize Flask application
app = Flask(__name__)

# Load the pre-trained machine learning model
model = pickle.load(open("model.pkl", "rb"))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Extract data from form inputs
        data = [float(x) for x in request.form.values()]
        # Predict using the loaded model
        prediction = model.predict([data])[0]
        # Return the result to the HTML page
        return render_template('index.html', prediction_text=f"Predicted Price: {round(prediction, 2)}")
    except Exception as e:
        return render_template('index.html', prediction_text=f"Error: {str(e)}")

if __name__ == "__main__":
    app.run(debug=True)
