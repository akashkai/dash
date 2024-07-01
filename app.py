# Importing all dependencies
import pandas as pd  
import plotly.express as px  
import streamlit as st  

# Defining page configuration
st.set_page_config(page_title="Sales Dashboard", page_icon=":bar_chart:", layout="wide")

# ---- READ EXCEL file ( Dataset ) ----
@st.cache_data
def get_data_from_excel():
    df = pd.read_excel(
        io="supermarkt_sales.xlsx",
        engine="openpyxl",
        sheet_name="Sales",
        skiprows=3,
        usecols="B:R",
        nrows=1000,
    )
    # Add 'hour' column to dataframe
    df["hour"] = pd.to_datetime(df["Time"], format="%H:%M:%S").dt.hour
    return df

df = get_data_from_excel()

# ------------------------------------------------------------------------------------
# ---- SIDEBAR ----
st.sidebar.header("🛒 Choose required attribute")
city = st.sidebar.multiselect(
    "🌎 Select Cities:",
    options=df["City"].unique(),
    default=df["City"].unique()
)

customer_type = st.sidebar.multiselect(
    "👤 Select customer type:",
    options=df["Customer_type"].unique(),
    default=df["Customer_type"].unique(),
)

gender = st.sidebar.multiselect(
    "👨/👩 Select the Gender:",
    options=df["Gender"].unique(),
    default=df["Gender"].unique()
)
 
branch = st.sidebar.multiselect(
    "🏢 Select Branch:",
    options=df["Branch"].unique(),
    default=df["Branch"].unique()
)

payment_mode= st.sidebar.multiselect(
    "💵 Select payment mode:",
    options=df["Payment"].unique(),
    default=df["Payment"].unique()
)

#  ------------------------------------------------------------------------------------

df_selection = df.query("City == @city  & Customer_type == @customer_type & Gender == @gender & Branch == @branch & Payment==@payment_mode ")


# Check if the dataframe is empty:
if df_selection.empty:
    st.warning("No data available based on the current filter settings!")
    st.stop() # This will halt the app from further execution.

#  ------------------------------------------------------------------------------------
#  ---- MAINPAGE ----

st.title(":bar_chart: Sales Dashboard")
st.markdown("##")

# TOP KPI's
total_sales = int(df_selection["Total"].sum())
average_rating = round(df_selection["Rating"].mean(), 1)
star_rating = ":star:" * int(round(average_rating, 0))
average_sale_by_transaction = round(df_selection["Total"].mean(), 2)

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("💰 Total Sales:")
    st.subheader(f"US $ {total_sales:,}")
with middle_column:
    st.subheader("Average Rating:")
    st.subheader(f"{average_rating} {star_rating}")
with right_column:
    st.subheader("💵 Average Sales Per Transaction:")
    st.subheader(f"US $ {average_sale_by_transaction}")

st.markdown("""---""")

# ----------------------------------[ Graphs ]--------------------------------------------------
# SALES BY PRODUCT LINE [BAR CHART]
sales_by_product_line = df_selection.groupby(by=["Product_line"])[["Total"]].sum().sort_values(by="Total")
fig_product_sales = px.bar(
    sales_by_product_line,
    x="Total",
    y=sales_by_product_line.index,
    orientation="h",
    title="<b>🔖 Sales by Product type</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_product_line),
    template="plotly_white",
)
fig_product_sales.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

# SALES BY HOUR [BAR CHART]
sales_by_hour = df_selection.groupby(by=["hour"])[["Total"]].sum()
fig_hourly_sales = px.bar(
    sales_by_hour,
    x=sales_by_hour.index,
    y="Total",
    title="<b>⏳ Sales by hours</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_hour),
    template="plotly_white",
)
fig_hourly_sales.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
)

# Pie chart

fig = px.pie(df_selection, values = "Total", names = "Gender", hole = 0.5,title="Gender wise sales")
fig.update_traces(text = df_selection["Gender"], textposition = "outside",)


# Scatter Plot
data1 = px.scatter(df_selection, x = "Total", y = "gross income")
data1['layout'].update(title="Relationship between Total and gross income using Scatter Plot.",xaxis = dict(title="Total"),
                       yaxis = dict(title = "Gross Income"))


#pie2
fig1 = px.pie(df_selection, values = "Total", names = "Product_line",title="Product type wise sales")
fig1.update_traces(text = df_selection["Product_line"], textposition = "outside",)

#pie2
fig2 = px.pie(df_selection, values = "Total", names = "City",title="Customer type wise sales")
fig2.update_traces(text = df_selection["City"], textposition = "outside",)


left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_hourly_sales, use_container_width=True)
right_column.plotly_chart(fig_product_sales, use_container_width=True)

cl1,cl2=st.columns(2)
cl1.plotly_chart(fig,use_container_width=True)
cl2.plotly_chart(data1,use_container_width=True)

cl3,cl4=st.columns(2)
cl3.plotly_chart(fig1,use_container_width=True)
cl4.plotly_chart(fig2,use_container_width=True)
# ------------------------------------------------------------------------------------

# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)




st.markdown("---")
st.image('dash12.png', width=1000)

st.markdown("---")
st.markdown("## Dataset")

st.dataframe(df_selection)
