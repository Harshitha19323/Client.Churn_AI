# ClientChurnAI 

ClientChurnAI is a full-fledged machine learning project designed to predict whether a customer is likely to churn based on their profile, usage behavior, and service preferences. The project includes Exploratory Data Analysis (EDA), model training, and deployment using Flask — all wrapped in a simple web interface.


 # Project Highlights

**End-to-End EDA** to understand churn patterns  
**Model training** using scikit-learn  
**Flask API deployment** to serve predictions  
**Web interface** for input and result display  

---

##  Repository Structure

**EDA Notebook**  
`Churn Analysis - EDA.ipynb`  
> Explores key patterns, visualizations, and insights on which customers are more likely to churn (e.g., monthly contract users, those using electronic check, etc.)

 **Model Building Notebook**  
`Churn Analysis - Model Building.ipynb`  
> Preprocesses data, handles encoding, and trains a machine learning model for churn prediction (Random Forest / Decision Tree used here).

**Deployment Script**  
`app.py`  
> Flask-based backend that serves the trained model for prediction.

---

## Flask API Overview

```python
# Initialize the app
app = Flask(__name__)

# Load the HTML front-end
@app.route("/")
def loadPage():
    return render_template('page.html', query="")

# Handle prediction on form submission
@app.route("/", methods=['POST'])
def predict():
    # Read form inputs, preprocess, and predict using the loaded model
    ...
