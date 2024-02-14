import streamlit as st 
import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns

st.set_page_config(page_title="Vrinda Store Sales Dashboard",
                   page_icon=":shopping_bags:",
                   layout="wide"
)

# Read the CSV file 
df = pd.read_csv("Sales data.csv")

st.title(":orange[Vrinda Store Anuual Report 2022] :shopping_bags: :bar_chart:")
st.markdown("Vrinda store wants to create an annual sales report for 2022.  So that,Vrinda can understand their customers and grow more sales in 2023.")
st.sidebar.header(" :blue[Please Filter Here]")
month = st.sidebar.multiselect(
        "Select the Month:",
        options=df["Month"].unique(),
        default=df["Month"].unique()
    )

channel = st.sidebar.multiselect(
        "Select the Channel:",
        options=df["Channel"].unique(),
        default=df["Channel"].unique()
    )

category = st.sidebar.selectbox(
        "Select the Category:",
        options=df["Category"].unique(),
    )

df_selection = df.query(
        "Month == @month & Category == @category & Channel == @channel"
    )

tab1, tab2 = st.tabs([":clipboard: Sales data", ":bar_chart: Dashboard"])
with tab1:
    st.markdown("### :clipboard: :green[Vrinda Store Dataset ]")
    

    st.dataframe(df_selection)

with tab2:
    st.title(":shopping_bags: :green[Sales Dashboard]")
    st.markdown("##")
    
    total_sales = int(df_selection["Amount"].sum())
    average_sale_by_transaction = round(df_selection["Amount"].mean(), 1)

    col1, col2 = st.columns(2)
    with col1:
       st.subheader(":pushpin: :red[Total Sales:]")
       st.subheader(f"Rs. {total_sales}")

    with col2:
       st.subheader(":pushpin:  :red[Average Sales Per Transaction:]")
       st.subheader(f"Rs. {average_sale_by_transaction}")

    st.markdown("---")

    #graph

    def graphs():
        #total_sales=int(df_selection["Amount"]).sum()

        #simple bar graph
        sales_by_state=(
            df_selection.groupby(by=["ship-state"]).count()[["Amount"]].sort_values(by="Amount")
             )
        fig_states=px.bar(
            sales_by_state,
            x="Amount" ,
            y=sales_by_state.index,
            orientation="h",
            title="<b> Sales: Top 5 States </b>",
            color_discrete_sequence=["#0083b8"]*len(sales_by_state),
            template="plotly_white",
             )
  
        fig_states.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False)      
         )

        #simple bar graph
        sales_by_gender=df_selection.groupby("Age Group")["Amount"].sum().reset_index()
        fig_gender=px.bar(
            sales_by_gender,
            x="Age Group", 
            y="Amount",
            title="<b> Sales by Age Group </b>",
            color_discrete_sequence=["#0083b8"],
            template="plotly_white",
         )

        fig_gender.update_layout(
            xaxis=dict(tickmode = "linear"),
            plot_bgcolor="rgba(0,0,0,0)",
            yaxis=(dict(showgrid=False))     
         )
        left,right=st.columns(2)
        left.plotly_chart(fig_gender,use_container_width=True)
        right.plotly_chart(fig_states,use_container_width=True)

    graphs()

    #Line Chart of Profit by States
    sales_profit = df_selection.groupby("Month")["Amount"].sum().reset_index()
    fig_sales=px.line(
        sales_profit,
        x="Month",
        y="Amount",
        title="<b> Orders Vs Sales </b>",
        color_discrete_sequence=["#0083b8"],
        template="gridon",
        )
    st.plotly_chart(fig_sales,use_container_width=True)

    col1,col2,col3 =st.columns(3)
    with col2:
         status_category = df_selection.groupby("Status")["Cust ID"].sum().reset_index()
         fig_status=px.pie(
           status_category,
           values="Cust ID",
           names="Status",
           title="<b> Orders Status </b>",
          )
         st.plotly_chart(fig_status,use_container_width=True)

    with col1:
        sales_by_gender = df_selection.groupby("Gender")["Amount"].sum().reset_index()
        fig_gender=px.pie(
           sales_by_gender,
           values="Amount",
           names="Gender",
           title="<b> Sales: Men Vs Women </b>",
          )
        st.plotly_chart(fig_gender,use_container_width=True)
        
       
    with col3:
         order_channel = df_selection.groupby("Channel")["Cust ID"].sum().reset_index()
         fig_channel=px.pie(
           order_channel,
           values="Cust ID",
           names="Channel",
           title="<b> Orders: Channel </b>",
          )
         st.plotly_chart(fig_channel,use_container_width=True) 
          
















 













