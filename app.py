import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(
    page_title="Agent Performance Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

DATA_PATH = "artifacts/feature_engineering/agent_performance_summary.csv"

@st.cache_data(persist=True, show_spinner=False)
def load_data():
    try:
        df = pd.read_csv(DATA_PATH)
        df['call_date'] = pd.to_datetime(df['call_date'])
        df['connect_rate_float'] = df['connect_rate'].str.rstrip('%').astype(float)
        return df
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None

def generate_slack_summary(df):
    report_date = df['call_date'].iloc[0].strftime('%Y-%m-%d')
    total_active_agents = len(df[df['presence'] == 1])
    avg_duration_min = df['avg_call_duration'].mean()
    top_performer = df.loc[df['connect_rate_float'].idxmax()]
    
    message = f"""
*Agent Summary for {report_date}*\n
:star: *Top Performer*: {top_performer['users_first_name']} {top_performer['users_last_name']} ({top_performer['connect_rate']} connect rate)
:busts_in_silhouette: *Total Active Agents*: {total_active_agents}
:stopwatch: *Average Duration*: {avg_duration_min:.1f} min\n
*Performance Highlights*:
- Highest Connect Rate: {top_performer['connect_rate']} ({top_performer['users_first_name']} {top_performer['users_last_name']})
- Most Calls Made: {df['total_calls'].max()} (Agent ID: {df.loc[df['total_calls'].idxmax(), 'agent_id']})
- Longest Avg Duration: {df['avg_call_duration'].max():.1f} min (Agent ID: {df.loc[df['avg_call_duration'].idxmax(), 'agent_id']})
"""
    return message

def main():
    st.title("Agent Performance Dashboard")
    
    with st.spinner('Loading agent performance data...'):
        df = load_data()
    
    if df is not None:
        if 'data_loaded' not in st.session_state:
            st.session_state.data_loaded = False
        
        with st.expander("View Raw Data", expanded=False):
            if not st.session_state.data_loaded:
                display_df = df.copy()
                display_df['call_date'] = display_df['call_date'].dt.strftime('%Y-%m-%d')
                display_df['avg_call_duration'] = display_df['avg_call_duration'].round(2).astype(str) + " min"
                display_df['connect_rate_float'] = display_df['connect_rate_float'].round(2).astype(str) + "%"
                
                st.dataframe(display_df, height=400, use_container_width=True)
                st.session_state.data_loaded = True

        st.subheader("Slack Summary")
        slack_message = generate_slack_summary(df)
        st.markdown(slack_message)

        if st.button("📋 Copy Summary to Clipboard"):
            st.session_state.slack_message = slack_message
            st.toast("Summary copied to clipboard!", icon="✅")

        st.subheader("Performance Visualizations")
        tab1, tab2, tab3 = st.tabs(["Connect Rates", "Call Volume", "Duration Analysis"])
        
        with tab1:
            st.write("### Connect Rate by Agent")
            st.bar_chart(df.set_index('agent_id')['connect_rate_float'], color="#FF6B6B", height=400)
        
        with tab2:
            st.write("### Call Volume by Agent")
            st.bar_chart(df.set_index('agent_id')['total_calls'], color="#4ECDC4", height=400)
        
        with tab3:
            st.write("### Duration Analysis")
            col1, col2 = st.columns(2)
            with col1:
                st.write("Average Duration by Agent")
                st.bar_chart(df.set_index('agent_id')['avg_call_duration'], color="#FFD166", height=400)
            with col2:
                st.write("Duration vs Call Volume")
                st.scatter_chart(df, x='total_calls', y='avg_call_duration', color='org_id', height=400)

        st.download_button(
            label="📥 Download Full Report",
            data=df.to_csv(index=False).encode('utf-8'),
            file_name=f"agent_performance_report_{datetime.now().strftime('%Y%m%d')}.csv",
            mime='text/csv'
        )

st.markdown("""
<style>
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    div[data-testid="stExpander"] div[role="button"] p {
        font-size: 16px;
        font-weight: bold;
        color: #1e3a8a;
    }
    .stMetric {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 15px;
        border-left: 4px solid #3b82f6;
    }
</style>
""", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
