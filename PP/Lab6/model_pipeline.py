import sys
import json
import joblib
import os
import pandas as pd

def process_and_predict(data):
    try:
        weight = float(data['weight'])
        height = float(data['height'])

        X_input = pd.DataFrame([[weight, height]], columns=['weight', 'height']) 

        file_path = os.path.join(os.path.dirname(__file__), "knn.pkl")
        model = joblib.load(file_path)

        prediction = model.predict(X_input)[0]

        mapping = {0: "normal", 1: "overweight", -1: "underweight"}
            
        return {"status": "success", "prediction": mapping[prediction]}
    
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    input_data = json.loads(sys.argv[1])
    result = process_and_predict(input_data)
    print(json.dumps(result))
