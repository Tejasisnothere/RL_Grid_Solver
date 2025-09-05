
import pickle

model = {"weights": [1, 2, 3], "bias": 0.5}



with open("model_pickle.pkl", "wb") as f:
    pickle.dump(model, f)

with open("model_pickle.pkl", "rb") as f:
    loaded_model_pickle = pickle.load(f)
print(loaded_model_pickle)
