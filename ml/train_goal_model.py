import os
import joblib
import numpy as np

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report


np.random.seed(42)

N = 2000

# ---------------------------------------------------------
# Generate realistic synthetic historical goal behaviour
# ---------------------------------------------------------

income = np.random.uniform(20000, 200000, N)

expense_ratio = np.random.uniform(0.4, 0.95, N)

expenses = income * expense_ratio

savings_rate = 1 - expense_ratio

target_amount = np.random.uniform(20000, 1000000, N)

goal_progress = np.random.uniform(0, 100, N)

months_remaining = np.random.randint(1, 61, N)

contribution_frequency = np.random.randint(0, 13, N)

average_contribution = np.random.uniform(0, 50000, N)

# ---------------------------------------------------------
# Create a realistic synthetic abandonment signal
# ---------------------------------------------------------

risk_score = (
    (expense_ratio > 0.80) * 2
    + (savings_rate < 0.15) * 2
    + (goal_progress < 20) * 2
    + (contribution_frequency < 3) * 2
    + (months_remaining < 3) * 1
    + (average_contribution < 5000) * 1
)

abandoned = (risk_score >= 4).astype(int)

# ---------------------------------------------------------
# Features
# ---------------------------------------------------------

X = np.column_stack([
    income,
    expenses,
    savings_rate,
    target_amount,
    goal_progress,
    months_remaining,
    contribution_frequency,
    average_contribution
])

y = abandoned

# ---------------------------------------------------------
# Train / Test
# ---------------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

model = RandomForestClassifier(
    n_estimators=150,
    max_depth=8,
    random_state=42
)

model.fit(X_train, y_train)

# ---------------------------------------------------------
# Evaluation
# ---------------------------------------------------------

predictions = model.predict(X_test)

accuracy = accuracy_score(
    y_test,
    predictions
)

print("Goal Abandonment Model")
print("=" * 50)

print(
    "Accuracy:",
    round(accuracy, 4)
)

print("\nClassification Report:")
print(
    classification_report(
        y_test,
        predictions
    )
)

# ---------------------------------------------------------
# Save model
# ---------------------------------------------------------

os.makedirs("models", exist_ok=True)

joblib.dump(
    model,
    "models/goal_abandonment_model.pkl"
)

print("\nModel saved successfully!")
