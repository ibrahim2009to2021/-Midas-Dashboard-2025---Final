from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import joblib, sys, os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from config import CONVERSION_MODEL_PATH
from app.predictive_engine.data_prepper import get_feature_engineered_data

def train_and_save_model():
    print("--- Starting Model Training ---")
    df = get_feature_engineered_data()
    if df.empty or len(df) < 20 or len(df['has_converted'].unique()) < 2:
        print("Not enough data or only one class present. Aborting training.")
        return
    X, y = df[['spend', 'ctr', 'cpc']], df['has_converted']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    model = LogisticRegression(random_state=42, class_weight='balanced')
    model.fit(X_train, y_train)
    print("\nModel Evaluation:", classification_report(y_test, model.predict(X_test)), sep='\n')
    joblib.dump(model, CONVERSION_MODEL_PATH)
    print(f"Model saved successfully to {CONVERSION_MODEL_PATH}")

if __name__ == '__main__':
    train_and_save_model()