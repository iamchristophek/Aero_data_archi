# Dictionnaire de données (v0)

## Interface OMEGA : vols (`omega_vols_YYYYMMDD.csv`)

| Colonne | Type | Description |
|---|---|---|
| numero_vol | texte | Code IATA du vol (ex. AF1234) |
| date_vol | date | Date programmée du vol |
| code_compagnie | texte | Code IATA de la compagnie |
| sens | texte | `A` (arrivée) ou `D` (départ) |
| aeroport_provenance_destination | texte | Code IATA de l'aéroport distant |
| terminal | texte | Terminal (ex. 2E) |
| porte | texte | Porte d'embarquement |
| heure_programmee | horodatage | Heure programmée |
| heure_reelle | horodatage | Heure réalisée (vide si annulé) |
| statut | texte | `REALISE`, `ANNULE`, `DETOURNE` |
| nb_passagers | entier | Nombre de passagers |

## Interface MDM : compagnies (`mdm_compagnies.csv`)

| Colonne | Type | Description |
|---|---|---|
| code_compagnie | texte | Code IATA |
| nom_compagnie | texte | Raison sociale |
| pays | texte | Pays de rattachement |
| alliance | texte | SkyTeam, Star Alliance, oneworld ou aucune |
