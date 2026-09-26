"""
VoltRelay Energy - Machine Learning & Interpretable Predictive Models
Includes Rider Churn Classifier, Station Failure Risk, and Risk Scoring.
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix

def train_churn_prediction_model(df_rider_mart):
    """Trains an interpretable Random Forest classifier for rider churn risk."""
    df = df_rider_mart.copy()
    
    # Impute missing values for clean training
    df['total_swaps'] = df['total_swaps'].fillna(0)
    df['failure_rate_pct'] = df['failure_rate_pct'].fillna(0)
    df['first_3_failures'] = df['first_3_failures'].fillna(0)
    df['avg_queue_sec'] = df['avg_queue_sec'].fillna(0)
    df['total_revenue'] = df['total_revenue'].fillna(0)
    df['ticket_count'] = df['ticket_count'].fillna(0)
    df['tenure_days'] = df['tenure_days'].fillna(0)
    df['is_fleet_affiliated'] = df['is_fleet_affiliated'].fillna(False).astype(int)
    df['is_churned'] = df['is_churned'].fillna(1).astype(int)
    
    # Feature matrix
    features = [
        'total_swaps',
        'failure_rate_pct',
        'first_3_failures',
        'avg_queue_sec',
        'total_revenue',
        'ticket_count',
        'tenure_days',
        'is_fleet_affiliated'
    ]
    
    X = df[features]
    y = df['is_churned']
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )
    
    # Train Random Forest
    rf = RandomForestClassifier(
        n_estimators=100, max_depth=6, min_samples_leaf=20, random_state=42
    )
    rf.fit(X_train, y_train)
    
    y_pred = rf.predict(X_test)
    y_prob = rf.predict_proba(X_test)[:, 1]
    
    metrics = {
        'accuracy': float(accuracy_score(y_test, y_pred)),
        'precision': float(precision_score(y_test, y_pred, zero_division=0)),
        'recall': float(recall_score(y_test, y_pred, zero_division=0)),
        'f1': float(f1_score(y_test, y_pred, zero_division=0)),
        'roc_auc': float(roc_auc_score(y_test, y_prob)),
        'test_size': len(y_test)
    }
    
    cm = confusion_matrix(y_test, y_pred).tolist()
    
    # Feature importance
    feat_imp = pd.DataFrame({
        'Feature': [
            'Total Swaps',
            'Failure Rate %',
            'First 3 Swaps Failures',
            'Avg Queue Wait (sec)',
            'Total Spend (INR)',
            'Support Tickets Count',
            'Tenure Days',
            'Fleet Affiliated'
        ],
        'Importance': rf.feature_importances_
    }).sort_values(by='Importance', ascending=False)
    
    # Predict on entire dataset for scoring
    all_prob = rf.predict_proba(X)[:, 1]
    df['churn_probability'] = np.round(all_prob, 3)
    
    def assign_risk(p):
        if p >= 0.70:
            return 'CRITICAL'
        elif p >= 0.45:
            return 'HIGH'
        elif p >= 0.25:
            return 'MEDIUM'
        return 'LOW'
    
    df['churn_risk_tier'] = df['churn_probability'].apply(assign_risk)
    
    # Recommendation playbook mapping
    def assign_action(row):
        if row['churn_probability'] >= 0.70:
            if row['first_3_failures'] > 0:
                return 'Issue ₹150 Proactive Swap Credit & VIP Onboarding Concierge'
            elif row['ticket_count'] > 0:
                return 'Priority Ticket Resolution + CSAT Recovery Outreach'
            return 'Targeted Retention Discount (20% off next 5 swaps)'
        elif row['churn_probability'] >= 0.45:
            return 'Send Proactive App Notification + Off-Peak Swap Incentives'
        return 'Standard Nurturing & Rewards Notification'
        
    df['recommended_intervention'] = df.apply(assign_action, axis=1)
    
    return rf, metrics, feat_imp, cm, df
