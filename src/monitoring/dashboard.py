import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time


def generate_sample_metrics():
    """Generate sample monitoring metrics"""
    dates = pd.date_range(start=datetime.now() - timedelta(days=30), end=datetime.now(), freq='D')
    
    metrics_data = {
        'date': dates,
        'accuracy': np.random.normal(0.85, 0.05, len(dates)),
        'latency': np.random.normal(0.2, 0.05, len(dates)),
        'throughput': np.random.poisson(100, len(dates)),
        'drift_score': np.random.exponential(0.1, len(dates))
    }
    
    return pd.DataFrame(metrics_data)


def main():
    st.set_page_config(page_title="Audio Sentiment Model Monitoring", layout="wide")
    
    st.title("🎵 Audio Sentiment Analysis - Model Monitoring Dashboard")
    
    # Sidebar
    st.sidebar.header("Dashboard Controls")
    auto_refresh = st.sidebar.checkbox("Auto Refresh (30s)", value=False)
    
    if auto_refresh:
        time.sleep(30)
        st.experimental_rerun()
    
    # Generate sample data
    df = generate_sample_metrics()
    
    # Main metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Current Accuracy", f"{df['accuracy'].iloc[-1]:.3f}", f"{df['accuracy'].diff().iloc[-1]:.3f}")
    
    with col2:
        st.metric("Avg Latency (s)", f"{df['latency'].iloc[-1]:.3f}", f"{df['latency'].diff().iloc[-1]:.3f}")
    
    with col3:
        st.metric("Daily Requests", int(df['throughput'].iloc[-1]), int(df['throughput'].diff().iloc[-1]))
    
    with col4:
        drift_status = "🟢 Normal" if df['drift_score'].iloc[-1] < 0.1 else "🔴 Alert"
        st.metric("Data Drift", drift_status, f"{df['drift_score'].diff().iloc[-1]:.3f}")
    
    # Charts
    st.subheader("Model Performance Trends")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_acc = px.line(df, x='date', y='accuracy', title='Model Accuracy Over Time')
        fig_acc.add_hline(y=0.8, line_dash="dash", line_color="red", annotation_text="Min Threshold")
        st.plotly_chart(fig_acc, use_container_width=True)
    
    with col2:
        fig_latency = px.line(df, x='date', y='latency', title='Response Latency')
        st.plotly_chart(fig_latency, use_container_width=True)
    
    # Data drift monitoring
    st.subheader("Data Drift Monitoring")
    fig_drift = go.Figure()
    fig_drift.add_trace(go.Scatter(x=df['date'], y=df['drift_score'], name='Drift Score'))
    fig_drift.add_hline(y=0.1, line_dash="dash", line_color="orange", annotation_text="Warning Threshold")
    fig_drift.add_hline(y=0.2, line_dash="dash", line_color="red", annotation_text="Critical Threshold")
    fig_drift.update_layout(title='Data Drift Score Over Time')
    st.plotly_chart(fig_drift, use_container_width=True)
    
    # Predictions distribution
    st.subheader("Recent Predictions Distribution")
    sentiment_dist = pd.DataFrame({
        'sentiment': ['positive', 'negative', 'neutral'],
        'count': np.random.multinomial(1000, [0.4, 0.3, 0.3])
    })
    
    fig_pie = px.pie(sentiment_dist, values='count', names='sentiment', title='Sentiment Distribution (Last 24h)')
    st.plotly_chart(fig_pie)
    
    # Recent logs
    st.subheader("Recent Activity Log")
    logs = [
        {"timestamp": datetime.now() - timedelta(minutes=5), "event": "Model prediction", "status": "✅ Success"},
        {"timestamp": datetime.now() - timedelta(minutes=15), "event": "Data drift check", "status": "✅ Normal"},
        {"timestamp": datetime.now() - timedelta(hours=1), "event": "Model health check", "status": "✅ Healthy"},
        {"timestamp": datetime.now() - timedelta(hours=6), "event": "Batch inference", "status": "✅ Completed"},
    ]
    
    logs_df = pd.DataFrame(logs)
    st.dataframe(logs_df, use_container_width=True)


if __name__ == "__main__":
    main()
