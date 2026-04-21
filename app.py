import streamlit as st
import pandas as pd
import os

# Configuration de la page
st.set_page_config(page_title="AIDA - Filtrage Risque Clients", layout="wide")
st.title("🎯 AIDA - Gestion des Risques Clients")

# Charger les données
@st.cache_data
def load_data():
    return pd.read_csv('business_data.csv')

df = load_data()

# Normaliser la colonne risque_churn
df['risque_churn'] = df['risque_churn'].str.lower().str.strip()

# Sidebar pour les filtres
st.sidebar.header("⚙️ Filtres")

# Filtre par niveau de risque
risque_options = sorted(df['risque_churn'].unique())
risques_selectionnees = st.sidebar.multiselect(
    "Sélectionner le(s) niveau(x) de risque:",
    options=risque_options,
    default=risque_options  # Affiche tous les risques par défaut
)

# Filtre supplémentaire par statut client
statuts = df['statut_client'].unique()
statuts_selectionnes = st.sidebar.multiselect(
    "Sélectionner le(s) statut(s) client:",
    options=statuts,
    default=statuts
)

# Appliquer les filtres
df_filtered = df[
    (df['risque_churn'].isin(risques_selectionnees)) &
    (df['statut_client'].isin(statuts_selectionnes))
]

# Afficher les statistiques
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Clients Filtrés", len(df_filtered))
    
with col2:
    total_ca = df_filtered['chiffre_affaires'].sum()
    st.metric("CA Total (€)", f"{total_ca:,.2f}")
    
with col3:
    satisfaction_moyenne = df_filtered['satisfaction'].mean()
    st.metric("Satisfaction Moyenne", f"{satisfaction_moyenne:.1f}/10")
    
with col4:
    cout_total = df_filtered['cout_support'].sum()
    st.metric("Coût Support Total (€)", f"{cout_total:,.2f}")

# Ajouter un séparateur
st.divider()

# Afficher les données filtrées
st.subheader("📊 Liste des Clients")

# Réorganiser les colonnes pour mieux les voir
colonnes_affichage = [
    'id_client', 'segment', 'risque_churn', 'statut_client',
    'chiffre_affaires', 'satisfaction', 'nb_commandes', 
    'dernier_achat_jours', 'potentiel_upsell', 'cout_support'
]

df_affichage = df_filtered[colonnes_affichage].copy()

# Appliquer la coloration selon le risque
def colorer_risque(val):
    if val == 'élevé':
        return 'background-color: #ff6b6b'
    elif val == 'moyen':
        return 'background-color: #ffd93d'
    elif val == 'faible':
        return 'background-color: #6bcf7f'
    return ''

styled_df = df_affichage.style.applymap(
    colorer_risque,
    subset=['risque_churn']
).format({
    'chiffre_affaires': '{:,.2f}',
    'satisfaction': '{:.1f}',
    'potentiel_upsell': '{:.1f}',
    'cout_support': '{:,.2f}'
})

st.dataframe(styled_df, use_container_width=True)

# Analyse par niveau de risque
st.divider()
st.subheader("📈 Analyse par Niveau de Risque")

risque_summary = df_filtered.groupby('risque_churn').agg({
    'id_client': 'count',
    'chiffre_affaires': ['sum', 'mean'],
    'satisfaction': 'mean',
    'cout_support': 'sum'
}).round(2)

risque_summary.columns = ['Nombre Clients', 'CA Total', 'CA Moyen', 'Satisfaction Moyenne', 'Coût Support Total']
st.dataframe(risque_summary, use_container_width=True)

# Export des données
st.divider()
st.subheader("📥 Export")

col1, col2 = st.columns(2)

with col1:
    csv = df_filtered.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Télécharger en CSV",
        data=csv,
        file_name="clients_filtres.csv",
        mime="text/csv"
    )

with col2:
    excel = df_filtered.to_excel(index=False, engine='openpyxl')
    st.download_button(
        label="📥 Télécharger en Excel",
        data=excel,
        file_name="clients_filtres.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    ) if 'openpyxl' in dir() else None
