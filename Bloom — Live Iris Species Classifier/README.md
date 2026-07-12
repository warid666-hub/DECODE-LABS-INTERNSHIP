
# Bloom — Live Iris Species Classifier

A desktop app that predicts an Iris flower's species in real time as you adjust its measurements — built with a K-Nearest Neighbors model trained with scikit-learn, wrapped in a live CustomTkinter GUI.

## Preview

*(Add a short screen recording or GIF here of the sliders moving and the prediction updating live — this is the most compelling part of the project.)*

## What It Does

- Loads the classic Iris dataset (150 samples, 3 species, 4 features)
- Trains a K-Nearest Neighbors classifier on it
- Lets you adjust sepal/petal measurements with sliders
- Predicts the species **instantly**, live, as you drag — no submit button needed
- Shows a confidence breakdown across all three species, updating in real time
- Includes a "Random Sample" button to pull a real flower from the dataset and see it classified live

## Machine Learning Pipeline

1. **Load & explore the dataset** — `sklearn.datasets.load_iris()`
2. **Train/test split** — 80/20, shuffled and stratified so both sets have a fair class balance
3. **Feature scaling** — `StandardScaler`, since KNN relies on distance and unscaled features would bias results
4. **Model training** — `KNeighborsClassifier(n_neighbors=5)`
5. **Evaluation** — accuracy, confusion matrix, and classification report (precision/recall/F1) on the held-out test set — not just raw accuracy, since that alone can be misleading

```python
model = KNeighborsClassifier(n_neighbors=5)
model.fit(X_train_scaled, y_train)
predictions = model.predict(X_test_scaled)
```

## Tech Stack

- **Python 3**
- **scikit-learn** — dataset, preprocessing, model, evaluation metrics
- **CustomTkinter** — live GUI
- **NumPy**

## Installation & Usage

```bash
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>/project-2-iris-classifier

pip install -r requirements.txt

python iris_classifier_gui.py
```

## What This Project Demonstrates

- Supervised learning fundamentals (train/test split, avoiding data leakage)
- Why feature scaling matters for distance-based algorithms
- Proper model evaluation beyond raw accuracy
- Turning a trained ML model into an interactive, usable application — not just a notebook

## Roadmap

- [ ] Add a K-value tuner to visualize the accuracy "elbow curve"
- [ ] Compare KNN against Logistic Regression / Decision Tree
- [ ] Export/save the trained model (`joblib`) so it doesn't retrain on every launch

## License

Open for learning and reference purposes.
