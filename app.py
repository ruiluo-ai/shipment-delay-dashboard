import streamlit as st
import pandas as pd

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

carrier = st.selectbox("Select Carrier",["All"]+list(df["carrier"].unique()))

if carrier != "All":
    df = df[df["carrier"] == carrier]

st.write(f"Showing data for: {carrier}")
#step5-KPIs(very important)
total = len(df)
delay_rate = len(df[df["delay_days"]>3])/total
avg_delay = df["delay_days"].mean()

st.metric("Total Shipment",total)
st.metric("Delay Rate(>3 days)",f"{delay_rate:.2%}")
#f"..." ->f-string
# .2f->2 decimal float
# .2%->percentage with 2 decimals
st.metric("Avg Delay (days)",round(avg_delay,2))

#step6-carrier chart
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
st.subheader("Delay Distribution")
st.bar_chart(df["delay_category"].value_counts())

#step8-severe delay by carrier
severe = df[df["delay_category"] =="Severe delay"]
st.subheader("Severe Delays by Carrier")
st.bar_chart(severe["carrier"].value_counts())

worst_carrier = df.groupby("carrier")["delay_days"].mean().idxmax()
#idxmax() is “Give me the index (name) of the maximum value”
st.write(f"Worst Carrier: {worst_carrier}")

