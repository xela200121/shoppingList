import streamlit as st
from collections import defaultdict
import psycopg2
from dotenv import load_dotenv
import os

# Fetch variables
USER = st.secrets["DB_USERNAME"]
PASSWORD = st.secrets["DB_PASSWORD"]
HOST = st.secrets["DB_HOST"]
PORT = st.secrets["DB_PORT"]
DBNAME = st.secrets["DB_NAME"]

# Connect to the database
try:
    connection = psycopg2.connect(
        user=USER,
        password=PASSWORD,
        host=HOST,
        port=PORT,
        dbname=DBNAME
    )
    print("Connection successful!")
    
    # Create a cursor to execute SQL queries
    cursor = connection.cursor()
    
    # Example query
    cursor.execute("SELECT NOW();")
    result = cursor.fetchone()
    print("Current Time:", result)

    # Close the cursor and connection
    cursor.close()
    connection.close()
    print("Connection closed.")

except Exception as e:
    print(f"Failed to connect: {e}")

# Inizializza la lista della spesa nella sessione di Streamlit
if 'shopping_list' not in st.session_state:
    st.session_state.shopping_list = defaultdict(int)

# Titolo dell'app
st.title("🛒 Lista della Spesa")

# Unità di misura disponibili
units = ["g", "ml", "cucchiai", "pz"]

# Funzione per aggiungere un alimento
def add_food(food, quantity, unit):
    key = f"{food} ({unit})"  # Aggiunge l'unità di misura al nome dell'alimento
    st.session_state.shopping_list[key] += quantity

# Funzione per rimuovere un alimento
def remove_food(food):
    if food in st.session_state.shopping_list:
        del st.session_state.shopping_list[food]

# Funzione per modificare un alimento
def edit_food(old_food, new_food, new_quantity, new_unit):
    if old_food in st.session_state.shopping_list:
        remove_food(old_food)
        add_food(new_food, new_quantity, new_unit)

# Input per aggiungere un alimento
st.header("Aggiungi un alimento")
col1, col2 = st.columns([3, 1])  # Divide l'input in due colonne

with col1:
    food_input = st.text_input("Inserisci l'alimento:")

with col2:
    unit = st.selectbox("Unità di misura:", units)

quantity = st.number_input("Quantità:", min_value=0)

if st.button("Aggiungi"):
    if food_input and quantity > 0:
        add_food(food_input, quantity, unit)
        st.success(f"Aggiunto: {food_input} {quantity}{unit}")
    else:
        st.error("Inserisci un alimento e una quantità validi.")

# Visualizza la lista della spesa
st.header("Lista della Spesa")
if st.session_state.shopping_list:
    for food, quantity in st.session_state.shopping_list.items():
        st.write(f"- {food}: {quantity}")
else:
    st.write("La lista della spesa è vuota.")

# Pulsante per resettare la lista
if st.button("Resetta la lista"):
    st.session_state.shopping_list = defaultdict(int)
    st.success("Lista della spesa resettata!")

# Modifica di un alimento
st.header("Modifica un alimento")
if st.session_state.shopping_list:
    # Selezione dell'alimento da modificare
    food_to_edit = st.selectbox("Seleziona l'alimento da modificare:", list(st.session_state.shopping_list.keys()))
    
    # Estrae il nome e l'unità di misura dall'alimento selezionato
    if "(" in food_to_edit:
        old_food, old_unit = food_to_edit.split(" (")
        old_unit = old_unit[:-1]  # Rimuove la parentesi chiusa
    else:
        old_food, old_unit = food_to_edit, "g"

    # Input per il nuovo nome, la nuova quantità e la nuova unità di misura
    new_food = st.text_input("Nuovo nome dell'alimento:", value=old_food)
    new_quantity = st.number_input("Nuova quantità:", value=st.session_state.shopping_list[food_to_edit], min_value=0)
    new_unit = st.selectbox("Nuova unità di misura:", units, index=units.index(old_unit))

    if st.button("Modifica"):
        if new_food and new_quantity >= 0:
            edit_food(food_to_edit, new_food, new_quantity, new_unit)
            st.success(f"Modificato: {new_food} {new_quantity}{new_unit}")
            st.rerun()  # Ricarica l'applicazione per aggiornare la lista
        else:
            st.error("Inserisci un nome e una quantità validi.")
else:
    st.write("Nessun alimento da modificare.")