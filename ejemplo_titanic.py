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
# Graficamos una tabla
st.table(df.head())

st.title("Análisis de supervivencia del Titanic por género")

archivo = st.file_uploader("database_titanic.csv", type=["csv"])

df = pd.read_csv("data/titanic.csv")

st.title("🚢 Supervivientes del Titanic por Género")
st.markdown("---")

# Cargar los datos
# Nota: Asumimos que el archivo 'database_titanic.csv' está en el mismo directorio.
try:
    df = pd.read_csv('database_titanic.csv')
except FileNotFoundError:
    st.error("Error: El archivo 'database_titanic.csv' no fue encontrado.")
    st.stop()

# --- Preprocesamiento y Cálculo ---

# 1. Filtrar solo a los sobrevivientes (Survived = 1)
survivors_df = df[df['Survived'] == 1]

# 2. Contar la cantidad de sobrevivientes por género ('Sex')
# Esto nos da una Series de Pandas con el conteo de 'female' y 'male'.
survival_counts = survivors_df['Sex'].value_counts().reset_index()
survival_counts.columns = ['Gender', 'Count']

# --- Creación del Gráfico (Usando Altair, ya que es la librería recomendada por Streamlit) ---

# El número de "bins" o categorías para este gráfico de barras es 2 (hombres y mujeres),
# lo cual es inherentemente el mínimo necesario para mostrar estos datos discretos.
# Altair/Streamlit manejan automáticamente esto sin una configuración explícita de "bins=1".

chart = alt.Chart(survival_counts).mark_bar().encode(
    # Eje X: Género (Variable Nominal)
    x=alt.X('Gender', axis=alt.Axis(title='Género')),
    
    # Eje Y: Cantidad de Sobrevivientes
    y=alt.Y('Count', axis=alt.Axis(title='Cantidad de Sobrevivientes')),
    
    # Color de las barras según el Género
    color=alt.Color('Gender', scale=alt.Scale(domain=['female', 'male'], 
                                              range=['#FF69B4', '#1E90FF']),
                    legend=alt.Legend(title="Género")),
    
    # Tooltip para mostrar los valores al pasar el ratón
    tooltip=['Gender', 'Count']
).properties(
    title='Cantidad de Sobrevivientes Hombres y Mujeres'
).interactive() # Permite hacer zoom y pan

# 3. Mostrar el Dataframe de los resultados
st.header("🔢 Conteo de Sobrevivientes")
st.dataframe(survival_counts)

# 4. Mostrar el gráfico en Streamlit
st.header("📈 Gráfico de Supervivencia")
st.altair_chart(chart, use_container_width=True)

# 5. Información adicional
st.markdown("""
***
* **Hombres sobrevivientes:** El género **male** (masculino).
* **Mujeres sobrevivientes:** El género **female** (femenino).
""")
