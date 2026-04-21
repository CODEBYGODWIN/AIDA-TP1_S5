"""
Module de filtrage des clients par niveau de risque (version standalone)
Sans dépendances externes - utilise uniquement la stdlib Python
"""
import csv
from typing import List, Optional, Dict
from collections import defaultdict

class FiltreRisqueClientStandalone:
    """Classe pour filtrer les clients par niveau de risque (version standalone)"""
    
    def __init__(self, chemin_csv: str = 'business_data.csv'):
        """Charger les données clients depuis le CSV"""
        self.clients = []
        self.load_csv(chemin_csv)
    
    def load_csv(self, chemin_csv: str):
        """Charger les données depuis le CSV"""
        with open(chemin_csv, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Normaliser le risque (mapper les variations)
                risque_raw = row['risque_churn'].lower().strip()
                # Mapper les variations possibles vers les niveaux standards
                normalisation = {
                    'élevé': 'élevé', 'eleve': 'élevé', 'high': 'élevé',
                    'moyen': 'moyen', 'moy': 'moyen', 'medium': 'moyen',
                    'faible': 'faible', 'low': 'faible'
                }
                row['risque_churn'] = normalisation.get(risque_raw, risque_raw)
                
                # Convertir les valeurs numériques avec gestion des valeurs vides
                try:
                    row['chiffre_affaires'] = float(row['chiffre_affaires']) if row['chiffre_affaires'].strip() else 0.0
                    row['satisfaction'] = float(row['satisfaction']) if row['satisfaction'].strip() else 5.0
                    row['cout_support'] = float(row['cout_support']) if row['cout_support'].strip() else 0.0
                    row['nb_commandes'] = int(row['nb_commandes']) if row['nb_commandes'].strip() else 0
                    row['dernier_achat_jours'] = int(row['dernier_achat_jours']) if row['dernier_achat_jours'].strip() else 0
                    row['potentiel_upsell'] = float(row['potentiel_upsell']) if row['potentiel_upsell'].strip() else 0.0
                    
                    self.clients.append(row)
                except (ValueError, KeyError) as e:
                    print(f"⚠️  Ligne ignorée (données invalides): {row.get('id_client', 'UNKNOWN')} - {e}")
                    continue
    
    def filtrer_par_risque(self, 
                          niveaux_risque: Optional[List[str]] = None,
                          statuts: Optional[List[str]] = None) -> List[Dict]:
        """Filtrer les clients par niveau de risque et statut"""
        resultat = self.clients.copy()
        
        if niveaux_risque:
            niveaux = [r.lower().strip() for r in niveaux_risque]
            resultat = [c for c in resultat if c['risque_churn'] in niveaux]
        
        if statuts:
            resultat = [c for c in resultat if c['statut_client'] in statuts]
        
        # Trier par risque (élevé en premier)
        ordre_risque = {'élevé': 0, 'moyen': 1, 'faible': 2}
        resultat.sort(key=lambda x: ordre_risque.get(x['risque_churn'], 3))
        
        return resultat
    
    def obtenir_prioritaires(self, seuil: str = 'élevé') -> List[Dict]:
        """Obtenir les clients prioritaires"""
        risques_prioritaires = {
            'élevé': ['élevé'],
            'moyen': ['moyen', 'élevé'],
            'faible': ['faible', 'moyen', 'élevé']
        }
        
        niveaux = risques_prioritaires.get(seuil.lower(), ['élevé'])
        statuts_prioritaires = ['Inactif', 'À relancer']
        
        return self.filtrer_par_risque(niveaux, statuts_prioritaires)
    
    def statistiques_par_risque(self) -> Dict:
        """Calculer les statistiques par niveau de risque"""
        stats = defaultdict(lambda: {
            'nb_clients': 0,
            'ca_total': 0,
            'ca_moyen': 0,
            'satisfaction_total': 0,
            'satisfaction_moyenne': 0,
            'cout_support_total': 0,
            'cout_support_moyen': 0,
            'commandes_total': 0,
            'commandes_moyennes': 0
        })
        
        # Grouper par risque
        for client in self.clients:
            risque = client['risque_churn']
            stats[risque]['nb_clients'] += 1
            stats[risque]['ca_total'] += client['chiffre_affaires']
            stats[risque]['satisfaction_total'] += client['satisfaction']
            stats[risque]['cout_support_total'] += client['cout_support']
            stats[risque]['commandes_total'] += client['nb_commandes']
        
        # Calculer les moyennes
        for risque in stats:
            nb = stats[risque]['nb_clients']
            stats[risque]['ca_moyen'] = stats[risque]['ca_total'] / nb
            stats[risque]['satisfaction_moyenne'] = stats[risque]['satisfaction_total'] / nb
            stats[risque]['cout_support_moyen'] = stats[risque]['cout_support_total'] / nb
            stats[risque]['commandes_moyennes'] = stats[risque]['commandes_total'] / nb
        
        return dict(stats)
    
    def exporter_csv(self, clients: List[Dict], nom_fichier: str):
        """Exporter les clients filtrés en CSV"""
        if not clients:
            print(f"⚠️  Aucun client à exporter")
            return
        
        # Utiliser les clés du premier client
        fieldnames = list(clients[0].keys()) if clients else []
        
        try:
            with open(nom_fichier, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames, restval='')
                writer.writeheader()
                writer.writerows(clients)
            
            print(f"✅ {len(clients)} client(s) exporté(s) vers {nom_fichier}")
        except Exception as e:
            print(f"⚠️  Erreur lors de l'export: {e}")
    
    def afficher_rapport(self, niveaux_risque: Optional[List[str]] = None,
                         statuts: Optional[List[str]] = None):
        """Afficher un rapport formaté"""
        clients_filtres = self.filtrer_par_risque(niveaux_risque, statuts)
        
        print("\n" + "="*80)
        print("RAPPORT DE FILTRAGE - CLIENTS PAR NIVEAU DE RISQUE")
        print("="*80)
        
        print(f"\n📊 Total clients filtrés: {len(clients_filtres)}")
        
        if clients_filtres:
            ca_total = sum(c['chiffre_affaires'] for c in clients_filtres)
            satisfaction_moy = sum(c['satisfaction'] for c in clients_filtres) / len(clients_filtres)
            
            print(f"💰 Chiffre d'affaires total: {ca_total:,.2f}€")
            print(f"⭐ Satisfaction moyenne: {satisfaction_moy:.1f}/10")
        
        # Statistiques par niveau
        print("\n" + "-"*80)
        print("Statistiques par niveau de risque:")
        print("-"*80)
        
        stats = self.statistiques_par_risque()
        
        for risque in sorted(stats.keys(), key=lambda x: {'élevé': 0, 'moyen': 1, 'faible': 2}.get(x, 3)):
            s = stats[risque]
            print(f"\n{risque.upper()}:")
            print(f"  • Clients: {s['nb_clients']}")
            print(f"  • CA: {s['ca_total']:,.2f}€ (moy: {s['ca_moyen']:,.2f}€)")
            print(f"  • Satisfaction: {s['satisfaction_moyenne']:.1f}/10")
            print(f"  • Commandes: {s['commandes_moyennes']:.1f} en moyenne")
        
        # Prioritaires
        print("\n" + "-"*80)
        prioritaires = self.obtenir_prioritaires('élevé')
        print(f"Clients PRIORITAIRES (risque élevé/moyen + Inactif/À relancer):")
        print("-"*80)
        
        if prioritaires:
            print(f"⚠️  {len(prioritaires)} client(s) nécessite(nt) une action immédiate!\n")
            
            # Afficher les premiers prioritaires
            try:
                for i, client in enumerate(prioritaires[:10], 1):
                    id_c = client.get('id_client', '?')
                    seg = client.get('segment', '?')[:15]
                    risque = client.get('risque_churn', '?')
                    statut = client.get('statut_client', '?')[:12]
                    ca = client.get('chiffre_affaires', 0)
                    sat = client.get('satisfaction', 0)
                    
                    print(f"{i}. {id_c:8} | {seg:15} | {risque:8} | "
                          f"{statut:12} | CA: {ca:10,.2f}€ | Sat: {sat:.1f}")
                
                if len(prioritaires) > 10:
                    print(f"... et {len(prioritaires) - 10} autres")
            except Exception as e:
                print(f"Erreur lors de l'affichage: {e}")
                for client in prioritaires[:5]:
                    print(f"  - {client.get('id_client', '?')}")
        else:
            print("✅ Aucun client prioritaire")
        
        print("\n" + "="*80 + "\n")


# Exemple d'utilisation
if __name__ == "__main__":
    print("🚀 Initialisation du filtre de risque...\n")
    
    try:
        filtre = FiltreRisqueClientStandalone()
        
        # Afficher rapport complet
        filtre.afficher_rapport()
        
        # Filtrer par risque élevé
        print("\n📋 CLIENTS AVEC RISQUE ÉLEVÉ:")
        print("-" * 80)
        clients_eleves = filtre.filtrer_par_risque(['élevé'])
        print(f"Nombre: {len(clients_eleves)}")
        
        if clients_eleves:
            for i, client in enumerate(clients_eleves[:5], 1):
                id_c = client.get('id_client', '?')
                seg = client.get('segment', '?')[:15]
                ca = client.get('chiffre_affaires', 0)
                sat = client.get('satisfaction', 0)
                
                print(f"{i}. {id_c:8} | {seg:15} | "
                      f"CA: {ca:10,.2f}€ | Sat: {sat:.1f}")
            if len(clients_eleves) > 5:
                print(f"... et {len(clients_eleves) - 5} autres")
        
        # Exporter les prioritaires
        prioritaires = filtre.obtenir_prioritaires('élevé')
        if prioritaires:
            filtre.exporter_csv(prioritaires, 'clients_prioritaires.csv')
        
        print("\n✅ Analyse complétée avec succès!")
        
    except FileNotFoundError:
        print("❌ Erreur: Fichier 'business_data.csv' non trouvé")
    except Exception as e:
        print(f"❌ Erreur: {e}")
