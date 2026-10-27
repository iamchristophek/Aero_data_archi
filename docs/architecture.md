# Architecture détaillée

## 1. Batch : applications sources

Les applications sont simulées par les scripts de `ingestion/generators/`. Chacune dépose des fichiers dans `data/landing/<source>/`.

| Source (simulée) | Rôle | Flux | Format |
|---|---|---|---|
| SPA | Calendrier : jours fériés et vacances | F1 | CSV |
| OMEGA | Vols programmés et réalisés | F1, F2 (référentiels) | CSV |
| EMS | Flux passagers aux points de contrôle | F1 | JSON |
| MDM | Référentiels : compagnies, aéroports, terminaux, portes | F1 | CSV |

## 2. Staging (1 table par interface)

- Schéma `staging`, chargement **tel quel** (toutes colonnes en texte) avec des métadonnées techniques : `_load_id`, `_load_ts`, `_source_file`.
- Aucune règle métier. Purge possible après intégration dans le Raw Vault.

## 3. Raw Vault (Bronze)

Modélisation **Data Vault 2.0**, *insert-only*, historisée.

| Type | Objets prévus |
|---|---|
| Hubs | `hub_vol`, `hub_compagnie`, `hub_aeroport`, `hub_porte`, `hub_point_controle` |
| Links | `lnk_vol_compagnie`, `lnk_vol_aeroport` (origine / destination), `lnk_vol_porte` |
| Satellites | `sat_vol_programme`, `sat_vol_realise`, `sat_compagnie_details`, `sat_passage_controle` |

Clés de hachage MD5 sur les clés métier, `load_date`, `record_source`, `hashdiff` pour la détection des changements.

## 4. Business Vault (Silver)

- **PIT** (*Point-In-Time*, D4) : `pit_vol` pour figer l'état des satellites à une date.
- **Bridge** (D6) : `brg_vol_compagnie_porte` pour accélérer les jointures.
- Règles métier calculées : retard en minutes, statut de ponctualité (à l'heure si le retard est ≤ 15 min), jour férié.

## 5. Exposition (Gold)

Modèle en étoile consommé par la BI :

- Faits : `fct_vols`, `fct_passages_controle`
- Dimensions : `dim_date`, `dim_compagnie`, `dim_aeroport`, `dim_porte`
- Agrégats KPI : `kpi_ponctualite_jour`, `kpi_occupation_portes`

## 6. Blocs transverses

| Bloc | Mise en œuvre |
|---|---|
| Traçabilité | Table `audit.load_log` (un enregistrement par run et par interface), `dbt docs` pour le lignage |
| Référentiels et paramétrages | Seeds dbt (`dbt/seeds/`) : seuils, mappings, libellés |
| Ordonnanceur | Dagster : un job quotidien, des assets dbt |
| Portail d'administration | Streamlit : dépôt de fichiers correctifs dans la zone landing, déclenchement d'un run, consultation de `audit.load_log` |
| CI/CD | GitHub Actions : lint SQLFluff, `dbt build` sur un PostgreSQL de service |

## 7. Transposition Microsoft Fabric

| Composant local | Équivalent Fabric |
|---|---|
| `data/landing` | Lakehouse (dossier Files) |
| Staging / Raw Vault | Lakehouse (tables Delta) ou Warehouse |
| dbt | dbt-fabric ou notebooks PySpark |
| Dagster | Data Factory Pipelines |
| Gold + Power BI | Warehouse + modèle sémantique en mode Direct Lake |
