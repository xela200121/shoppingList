import streamlit as st
from collections import defaultdict

# Inizializza la lista della spesa nella sessione di Streamlit
if 'shopping_list' not in st.session_state:
    st.session_state.shopping_list = defaultdict(int)

# Titolo dell'app
st.title("🛒 Lista della Spesa")

# Funzione per aggiungere un alimento
def add_food(food, quantity):
    st.session_state.shopping_list[food] += quantity

# Funzione per rimuovere un alimento
def remove_food(food):
    if food in st.session_state.shopping_list:
        del st.session_state.shopping_list[food]

# Funzione per modificare un alimento
def edit_food(old_food, new_food, new_quantity):
    if old_food in st.session_state.shopping_list:
        remove_food(old_food)
        add_food(new_food, new_quantity)

# Input per aggiungere un alimento
st.header("Aggiungi un alimento")
food_input = st.text_input("Inserisci l'alimento e la quantità (es. mozzarella 100g):")

if st.button("Aggiungi"):
    if food_input:
        try:
            # Separa l'alimento dalla quantità
            food, quantity = food_input.rsplit(' ', 1)
            quantity_value = int(''.join(filter(str.isdigit, quantity)))  # Estrae il numero dalla quantità
            add_food(food, quantity_value)
            st.success(f"Aggiunto: {food} {quantity_value}g")
        except ValueError:
            st.error("Formato non valido. Usa il formato 'alimento quantità' (es. mozzarella 100g).")
    else:
        st.error("Inserisci un alimento e una quantità.")

# Visualizza la lista della spesa
st.header("Lista della Spesa")
if st.session_state.shopping_list:
    for food, quantity in st.session_state.shopping_list.items():
        st.write(f"- {food}: {quantity}g")
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
    
    # Input per il nuovo nome e la nuova quantità
    new_food = st.text_input("Nuovo nome dell'alimento:", value=food_to_edit)
    new_quantity = st.number_input("Nuova quantità (in grammi):", value=st.session_state.shopping_list[food_to_edit], min_value=0)

    if st.button("Modifica"):
        if new_food and new_quantity >= 0:
            edit_food(food_to_edit, new_food, new_quantity)
            st.success(f"Modificato: {new_food} {new_quantity}g")
        else:
            st.error("Inserisci un nome e una quantità validi.")
else:
    st.write("Nessun alimento da modificare.")