import streamlit as st
import pandas as pd
import numpy as np
from scipy import stats
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px

@st.cache_data
def load_data(link):
    return pd.read_csv(link, index_col=0)
data = load_data('https://bigmacindexdata2023.s3.amazonaws.com/bigmacdata_processed.csv')

countrylist = list(np.unique(data.country))
USBMEX = data.pivot(index='date',columns='country',values='BigMac Exchange Rate').round(2)
USEX = data.pivot(index='date',columns='country',values='Actual Exchange Rate').round(2)
EXEVAL = data.pivot(index='date',columns='country',values='Evaluation').round(2)
EXEVAL.index = pd.to_datetime(EXEVAL.index)
EXEVAL = EXEVAL.groupby(EXEVAL.to_period("Y").index).mean()
EXEVAL.index = EXEVAL.index.strftime("%Y")

datelist = list(USBMEX.index)

def create_plotly_ex(country):
    fig = make_subplots(rows=2, cols=1, start_cell="bottom-left",vertical_spacing = 0.05)
    fig.add_trace(go.Scatter(x=datelist, y=USEX[country].tolist(),name="Actual"),
                row=2, col=1)
    fig.add_trace(go.Scatter(x=datelist, y=USBMEX[country].tolist(),name="BigMac"),
                row=2, col=1)
    fig.add_trace(go.Bar(x=EXEVAL.index, y=EXEVAL[country].to_list(), 
                        name="Evaluation",
                        marker_color=np.where(EXEVAL[country]<0, 'red', 'blue')),
                row=1, col=1)
    fig.update_xaxes(title_text="year", row=1, col=1)
    fig.update_yaxes(title_text="Exchange Rate", row=2, col=1)
    fig.update_yaxes(title_text="Evaluation (%)", row=1, col=1)
    fig.update_layout(height=600, width=900,
        title_text="BigMac Exchange Rate versus Actual Exchange Rate")
    return fig

def create_plot_map(date, measure):
    df = data[data.date==date]
    map = {"BigMac Price ($)":"dollar_price","Evaluation (%)":"Evaluation"}
    fig = px.choropleth(df, locations="iso_alpha3",
                    color=map[measure], 
                    hover_name="country", 
                    color_continuous_scale=px.colors.sequential.Plasma)
    fig.update_layout(height=600, width=900,
        title_text="World map for BigMac data")
    return fig

def create_plotly_price(date):
    df = data[data.date==date].dropna()
    temp = df.sort_values(by=['dollar_price'],ascending=False).dropna().head(20).set_index("country")
    fig = make_subplots(rows=2, cols=1, start_cell="bottom-left",vertical_spacing = 0.05)
    fig.add_trace(go.Bar(x=temp.index, y=temp["dollar_price"].tolist(),name="Bigmac Price"),
                row=2, col=1)
    fig.add_trace(go.Bar(x=temp.index, y=temp["GDP_dollar"].tolist(),name="GDP per person"),
                row=1, col=1)
    fig.update_xaxes(showticklabels=False, row=2, col=1)
    fig.update_yaxes(title_text="BigMac price ($)", row=2, col=1)
    fig.update_xaxes(title_text="Country", row=1, col=1)
    fig.update_yaxes(title_text="GDP per person ($)", row=1, col=1)
    fig.update_layout(height=600, width=900,
        title_text="Top 20 countries of BigMac Price and GDP per person")
    return fig

def create_plotly_price_relation(date):
    df = data[data.date==date].dropna()
    y = df["dollar_price"].values
    x = df["GDP_dollar"].values
    res = stats.linregress(x, y)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode='markers',name="data points"))
    fig.add_trace(go.Scatter(x=x,y=res.intercept + res.slope*x, name="regression line"))
    fig.update_xaxes(title_text="Bigmac Price ($)")
    fig.update_yaxes(title_text="GDP per person ($)")
    fig.update_layout(height=600, width=900,
    title_text="GDP per person versus BigMac Price on {}".format(date))
    return fig, '{:0.2e}'.format(res.intercept), '{:0.2e}'.format(res.slope), round(res.rvalue**2,2)

st.title('Storytelling of Big Mac Index')
st.subheader("Background")
st.write("In 1986, the Economist introduced the Big Mac index to compare with the market exchange rate [1]. \
    According to the theory of purchasing-power parity, the exchange rate between two currencies should be obtained  \
    by buying the same value of goods using their currencies. For example, you spend 0.75 pound \
    to buy a Big Mac in the UK, while you need to pay 1 dollar to buy a Big Mac. Then, the Big Mac exchange rate is 0.75. \
    If the actual exchange rate is higher(lower) than the Big Mac exchange rate, then this suggests that it is under(over)-valued.")
st.subheader("Outline")
st.write("In this report, we present the data from the Economist [2]. We provide the visualization of the Big Mac exchange rate \
    for the different countries. We also compare the price of a Big Mac and the wealth of the different countries.")
    
st.subheader("Comparison between the actual and BigMac exchange rates")
st.write("We compare the actual and BigMac exchange rates with the base currency, US dollar.")
country = st.selectbox("Country", tuple(countrylist))

fig1 = create_plotly_ex(country)
st.plotly_chart(fig1)

st.subheader("Big Mac data in the world")
st.write("We show the Big Mac data in the different regions, where the Big Mac data are given as:")
st.markdown("- BigMac Price ($)")
st.markdown("- Evaluation (%)")
date = st.selectbox("Date", tuple(datelist))
measure = st.selectbox("Measure", tuple(["BigMac Price ($)","Evaluation (%)"]))

fig2 = create_plot_map(date, measure)
st.plotly_chart(fig2)

st.subheader("Do people in rich countries get a more expensive Big Mac?")
st.write("We compare the 20 countries with the highest price of a BigM ac and their GDP per person. This helps us to see the \
    relationship between the price of a Big Mac and its GDP.")
date2 = st.selectbox("Choose date", tuple(datelist))
fig3 = create_plotly_price(date2)
st.plotly_chart(fig3)

st.write("We study the linear regression between the Big Mac price and GDP per person in a given period.")
fig4, intercept, slope, rsquared = create_plotly_price_relation(date2)
st.plotly_chart(fig4)
st.write("The linear relationship between Big Mac price, y, and GDP per person, x, is made by using the linear regression, where \
    y = {} + {} x. The R-squared error is {}.".format(intercept, slope, rsquared))

st.subheader("Reference")
st.markdown("1. The Big Mac index. [link](https://www.economist.com/big-mac-index)")
st.markdown("2. The methodology and data source. [link](https://github.com/TheEconomist/big-mac-data)")
