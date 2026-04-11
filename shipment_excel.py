import pandas as pd
import matplotlib.pyplot as plt
df = pd.read_excel("shipment.xlsx")
print(df.head())
print(df.columns)
print(len(df))
print(df["LINER\n船司"].unique())
print(df["LINER\n船司"].value_counts())

xls = pd.ExcelFile("shipment.xlsx")
print(xls.sheet_names)
df_la=pd.read_excel("shipment.xlsx",sheet_name="LA")
print(df_la.columns)
#the difference between read_excel and ExcelFile
#use read_excel when you know the sheet,you just want the data. --analysis
#use ExcelFile when you don’t know sheet names,you want to explore structure, you will read multiple sheets --inspect
for sheet in xls.sheet_names:
    df_temp = pd.read_excel("shipment.xlsx",sheet_name=sheet)
    print(f"\nSheet:{sheet}")
    print(df_temp.columns)

df=pd.read_excel("shipment.xlsx",sheet_name="LA")
df["ATA Seaport"] = pd.to_datetime(df["ATA Seaport"])
df["Revised \nETA Seaport"] = pd.to_datetime(df["Revised \nETA Seaport"])
df["delay_days"] = (df["ATA Seaport"]-df["Revised \nETA Seaport"]).dt.days
df[df["delay_days"]>3]
df["LINER\n船司"].value_counts()
print(df.groupby("LINER\n船司")["delay_days"].mean().sort_values(ascending=False))

df["LINER\n船司"] = df["LINER\n船司"].str.strip()
df = df.dropna(subset=["delay_days"])
#dropna() drop rows with ANY missing
#dropna(subset=["col"]) only care about this column
print(df.groupby("LINER\n船司")["delay_days"].mean().sort_values(ascending=False))

print(df.isna().sum())
print(df[df["delay_days"].isna()])

delay_rate=len(df[df["delay_days"]>3])/len(df)
print(delay_rate)

def delay_category(x):
    if x<=0:
        return "On time / Early"
    elif x<= 3:
        return "Slight delay"
    else:
        return "Severe delay"

df["delay_category"] = df["delay_days"].apply(delay_category)
#.apply() means "loop through each row and process it"
print(df["delay_category"].value_counts())

carrier_delay = df.groupby("LINER\n船司")["delay_days"].mean().sort_values(ascending=False)

#carrier_delay.plot(kind="bar")
#plt.title("Average Delay by Carrier")
#plt.ylabel("Delay (Days)")
#plt.xlabel("Carrier")
#plt.show()

df["delay_category"].value_counts().plot(kind="bar")
plt.title("Delay Category Distribution")
plt.ylabel("Number of Shipments")
plt.xlabel("Category")
plt.show()

severe = df[df["delay_category"] == "Severe delay"]
#severe是一个dataframe
severe["LINER\n船司"].value_counts().plot(kind="bar")
#severe["LINER\n船司"]是从severe这个表里，取出“carrier”这一列，value_counts()统计每个carrier出现多少次。
#df[...]选行
#df["col"]选列
#df[条件]过滤行
#df[条件]["col"] 先过滤，再选列
plt.title("Severe Delays by Carrier")
plt.ylabel("Number of Shipments")
plt.xlabel("Carrier")
plt.show()

import streamlit as st
