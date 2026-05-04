from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import pandas as pd
import os
from openai import OpenAI
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
st.title("🚢 Supply Chain Dashboard")

#step4-load your data
df = pd.read_excel("shipment.xlsx",sheet_name="LA")

df = df.rename(columns={
    "LINER\n船司":"carrier",
    "Revised \nETA Seaport":"eta",
    "ATA Seaport":"ata"})
df["carrier"] = (
    df["carrier"]
    .astype(str)
    .str.replace(r"\s+","",regex=True)
    .str.strip()
    .str.upper()
)

df["eta"] = pd.to_datetime(df["eta"])
df["ata"] = pd.to_datetime(df["ata"])

df["delay_days"] = (df["ata"]-df["eta"]).dt.days

df =df.dropna(subset=["delay_days"])

threshold = df["delay_days"].mean()+2*df["delay_days"].std()
df["is_anomaly"] = df["delay_days"]>threshold

carrier = st.selectbox("Select Carrier",["All"]+list(df["carrier"].unique()))

#df_all-->full dataset
#df_filtered -->selected carrier
df_all = df.copy()

if carrier != "All":
    df_filtered = df[df["carrier"] == carrier]
else:
    df_filtered = df

st.write(f"Showing data for: {carrier}")
def generate_ai_summary(df_filtered,df_all):
    carrier_delay = (
        df.groupby("carrier")["delay_days"]
        .mean()
        .sort_values(ascending=False)
    )

    total_shipments = len(df)
    severe_delay_rate = (df["delay_days"] > 3).mean()
    carrier_stats = (
        df.groupby("carrier")["delay_days"]
        .agg(["mean", "count"])
        .sort_values(by="mean", ascending=False)
    )
    filtered_stats = df_filtered["delay_days"].mean()
    overall_stats = df["delay_days"].mean()
    anomaly_count = df_filtered["is_anomaly"].sum()

    prompt = f"""
You are a supply chain analyst.

Selected carrier average delay: {filtered_stats:.2f} days
Overall average delay: {overall_stats:.2f} days
Number of anomalous shipments: {anomaly_count}

Explain:
1. Performance vs average
2. Whether anomalies indicate operational issues?
3. Recommended action

Important interpretation rules:
- Negative delay = early arrival
- Positive delay = late arrival
- Only treat anomalies as serious risk

Keep it concise and business-focused.
"""

    response = client.responses.create(
        model="gpt-4o-mini",
        input=prompt,
    )

    return response.output_text
#step5-KPIs(very important)
total = len(df)
delay_rate = len(df[df["delay_days"]>3])/total
avg_delay = df["delay_days"].mean()

col1,col2,col3 = st.columns(3)

col1.metric("Total Shipment",total)
col2.metric("Delay Rate(>3 days)",f"{delay_rate:.2%}")
#f"..." ->f-string
# .2f->2 decimal float
# .2%->percentage with 2 decimals
col3.metric("Avg Delay (days)",round(avg_delay,2))

#step6-carrier chart
st.markdown("##📊 Carrier Performance")
carrier_delay = df.groupby("carrier")["delay_days"].mean().sort_values(ascending=False)
st.subheader("Average Delay by Carrier")
st.bar_chart(carrier_delay)

#step7-delay categories
def delay_category(x):
    if x<= 0:
        return "On time / Early"
    elif x<= 3:
        return "Slight delay"
    else:
        return "Severe delay"

df["delay_category"] = df["delay_days"].apply(delay_category)
#.apply() : lambda function
#st.subheader("Delay Distribution")
st.markdown("## ⏱ Delay Distribution")
st.bar_chart(df["delay_category"].value_counts())

#step8-severe delay by carrier
st.markdown("##🚨 Severe Delays by Carrier")
severe = df[df["delay_category"] =="Severe delay"]
#st.subheader("Severe Delays by Carrier")
st.bar_chart(severe["carrier"].value_counts())

worst_carrier = df.groupby("carrier")["delay_days"].mean().idxmax()
#idxmax() is “Give me the index (name) of the maximum value”
st.write(f"Worst Carrier: {worst_carrier}")

#step9-Anomaly detection
st.markdown("##⚠️ Anomaly Shipments")

anomalies = df[df["is_anomaly"]]

st.write(f"Number of anomalies: {len(anomalies)}")
st.dataframe(anomalies[["carrier", "delay_days"]])

st.markdown("## 🤖 AI Insights")
st.caption("Generate an AI-written operations summary based on current filtered shipment data.")
if st.button("Generate AI Summary"):
    if not os.environ.get("OPENAI_API_KEY"):
        st.error("API key not found")
    else:
        with st.spinner("Thinking..."):
            summary = generate_ai_summary(df_filtered,df_all)
        st.markdown(summary)

st.write("BOTTOM OF APP")