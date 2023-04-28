import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Dashboard de ventas",
                   page_icon=":bar_chart:",
                   layout="wide",
                   initial_sidebar_state="collapsed"

)

# con st.cache = evitamos estar llamando constamente el archivo excel. sive para que se renderize la informacion mas rapido
@st.cache_data
def get_data_from_excel():
    df = pd.read_excel(
        io = 'datos.xlsx',
        engine = 'openpyxl',
        sheet_name='ventas',
        skiprows=1,
        usecols='C:N',
        nrows=1000,
    )
    df["Fecha"]= pd.to_datetime(df["Fecha"], format="%DD:%MM%YY").dt.date
    return df
df = get_data_from_excel()

st.sidebar.header("Por favor filtra aqui")
sucursal = st.sidebar.multiselect(
    "Selecciona una sucursal: ",
    options=df["Sucursal"].unique(),
    default=df["Sucursal"].unique(),
)

producto = st.sidebar.multiselect(
    "Selecciona el producto: ",
    options=df["Producto"].unique(),
    default=df["Producto"].unique()
)

fecha = st.sidebar.multiselect(
    "Selecciona la fecha: ",
    options = df["Fecha"].unique(),
    default=df["Fecha"].unique()
)

df_selection = df.query(
    "Sucursal == @sucursal & Producto == @producto & Fecha == @fecha"
)

# MAINPAGE
st.title(":bar_chart: Dashboard de Ventas" )


# TOP KPI
ico_ganancias = "💰"
ventas_totales = int(df_selection["Importe Pendiente"].sum())
ico_ventas = "📈"
ganancias = int(df_selection["Importe Total"].sum())
ico_box = "📦"
surtido = int(df_selection["Cantidad Surtida"].sum())
left_column, middle_column, right_column = st.columns(3)

with left_column:
    st.subheader("Ganancias")
    st.subheader(f" {ico_ganancias} MX $ {ganancias:,}")

with middle_column:
    st.subheader("Ventas totales")
    st.subheader(f" {ico_ventas} MX $ {ventas_totales:,}")

with right_column:
    st.subheader("Cajas vendidas")
    st.subheader(f" {ico_box} {surtido}")

st.markdown("---")

# PRIMER GRAFICO

venta_por_fecha = (
    df_selection.groupby(by=["Fecha"]).sum()[["Importe Total"]].sort_values(by="Importe Total")
)

fig_fecha = px.bar(
    venta_por_fecha,
    x = "Importe Total",
    y = venta_por_fecha.index,
    orientation="h",
    title = "<b>Ganancias por fecha</b>",
    color_discrete_sequence=["#0083B8"] * len(venta_por_fecha),
    template = "plotly_white",
)

fig_fecha.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

# SEGUNDO GRAFICO

venta_por_producto = df_selection.groupby(by=["Producto"]).sum()[["Importe Total"]]
fig_productos = px.bar(
    venta_por_producto,
    x=venta_por_producto.index,
    y="Importe Total",
    title = "<b>Ganancias por producto</b>",
    color_discrete_sequence=["#0083B8"] * len(venta_por_producto),
    template="plotly_white",
)
fig_productos.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
)

# TERCER GRAFICO
ventas_totales_grafico = df_selection.groupby(by=["Producto"]).sum()[["Importe Pendiente"]]
fig_ventas = px.pie(
    ventas_totales_grafico,
    names=ventas_totales_grafico.index,
    values = "Importe Pendiente",
    title="Ventas totales",
    hole = .3, 
    color= ventas_totales_grafico.index,
    color_discrete_sequence=px.colors.sequential.Aggrnyl_r
)

left_column, right_column, pie_chart = st.columns(3)
pie_chart.plotly_chart(fig_ventas, use_container_width=True)
left_column.plotly_chart(fig_fecha, use_container_width=True)
right_column.plotly_chart(fig_productos, use_container_width=True)

# OCULTAR EL ESTILO POR DEFECTO DE STREAMLIT
hide_st_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden}
    </style>
    """
st.markdown(hide_st_style, unsafe_allow_html=True)