import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Carga el archivo CSV "database_titanic.csv" en un DataFrame de pandas.
df = pd.read_csv("database_titanic.csv")

# Muestra un título y una descripción en la aplicación Streamlit.
st.write("""
# Mi primera aplicación interactiva
## Gráficos usando la base de datos del Titanic
""")

# Usando la notación "with" para crear una barra lateral en la aplicación Streamlit.
with st.sidebar:
    # Título para la sección de opciones en la barra lateral.
    st.write("# Opciones")
    
    # Crea un control deslizante (slider) que permite al usuario seleccionar un número de bins
    # en el rango de 0 a 10, con un valor predeterminado de 2.
    div = st.slider('Número de bins:', 0, 10, 2)
    
    # Muestra el valor actual del slider en la barra lateral.
    st.write("Bins=", div)

# Desplegamos un histograma con los datos del eje X
fig, ax = plt.subplots(1, 2, figsize=(10, 3))
ax[0].hist(df["Age"], bins=div)
ax[0].set_xlabel("Edad")
ax[0].set_ylabel("Frecuencia")
ax[0].set_title("Histograma de edades")

# Tomando datos para hombres y contando la cantidad
df_male = df[df["Sex"] == "male"]
cant_male = len(df_male)

# Tomando datos para mujeres y contando la cantidad
df_female = df[df["Sex"] == "female"]
cant_female = len(df_female)

ax[1].bar(["Masculino", "Femenino"], [cant_male, cant_female], color = "red")
ax[1].set_xlabel("Sexo")
ax[1].set_ylabel("Cantidad")
ax[1].set_title('Distribución de hombres y mujeres')

# Desplegamos el gráfico
st.pyplot(fig)

st.write("""
## Muestra de datos cargados
""")
st.table(df.head())

st.title("🚢 Supervivientes del Titanic por Género (Simple)")
st.markdown("---")

# Cargar los datos
try:
    df = pd.read_csv('database_titanic.csv')
except FileNotFoundError:
    st.error("Error: El archivo 'database_titanic.csv' no fue encontrado.")
    st.stop()

# --- Cálculo de Supervivientes por Género ---

# 1. Filtra las filas donde 'Survived' es 1 y agrupa por 'Sex', contando las ocurrencias.
survival_counts = (
    df[df['Survived'] == 1]
    ['Sex']
    .value_counts()
    .reset_index(name='Count')
)
survival_counts.columns = ['Género', 'Cantidad']

# --- Mostrar Resultados en Streamlit ---

st.header("🔢 Conteo de Sobrevivientes")
st.dataframe(survival_counts, hide_index=True)

st.header("📈 Gráfico de Barras")
# Streamlit usa su función integrada bar_chart, que acepta el DataFrame
# directamente y es más simple que configurar Altair.
st.bar_chart(
    survival_counts,
    x='Género',
    y='Cantidad',
    color='#FF69B4' # Un color fijo para simplificar
)
