"""Simulateur de l'application OMEGA : génère un fichier de vols par jour."""
import argparse
import csv
import random
from datetime import date, datetime, timedelta
from pathlib import Path

COMPAGNIES = ["AF", "KL", "DL", "LH", "BA", "EK", "U2", "TO", "AT", "HF"]
AEROPORTS = ["JFK", "LHR", "FRA", "AMS", "DXB", "ABJ", "CMN", "DSS", "MAD", "FCO"]
TERMINAUX = {"1": "A", "2E": "K", "2F": "F", "3": "C"}
STATUTS = ["REALISE"] * 95 + ["ANNULE"] * 3 + ["DETOURNE"] * 2

COLONNES = [
    "numero_vol", "date_vol", "code_compagnie", "sens", "aeroport_provenance_destination",
    "terminal", "porte", "heure_programmee", "heure_reelle", "statut", "nb_passagers",
]


def generer_vols(jour: date, nb_vols: int) -> list[dict]:
    vols = []
    for _ in range(nb_vols):
        compagnie = random.choice(COMPAGNIES)
        terminal = random.choice(list(TERMINAUX))
        prog = datetime.combine(jour, datetime.min.time()) + timedelta(minutes=random.randint(330, 1410))
        statut = random.choice(STATUTS)
        retard = max(0, int(random.gauss(8, 20)))
        vols.append({
            "numero_vol": f"{compagnie}{random.randint(100, 9999)}",
            "date_vol": jour.isoformat(),
            "code_compagnie": compagnie,
            "sens": random.choice("AD"),
            "aeroport_provenance_destination": random.choice(AEROPORTS),
            "terminal": terminal,
            "porte": f"{TERMINAUX[terminal]}{random.randint(1, 40)}",
            "heure_programmee": prog.isoformat(timespec="minutes"),
            "heure_reelle": "" if statut == "ANNULE" else (prog + timedelta(minutes=retard)).isoformat(timespec="minutes"),
            "statut": statut,
            "nb_passagers": 0 if statut == "ANNULE" else random.randint(40, 380),
        })
    return vols


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--days", type=int, default=7, help="Nombre de jours à générer")
    parser.add_argument("--vols-par-jour", type=int, default=300)
    parser.add_argument("--sortie", type=Path, default=Path("data/landing/omega"))
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    random.seed(args.seed)
    args.sortie.mkdir(parents=True, exist_ok=True)
    debut = date.today() - timedelta(days=args.days)
    for i in range(args.days):
        jour = debut + timedelta(days=i)
        fichier = args.sortie / f"omega_vols_{jour:%Y%m%d}.csv"
        with fichier.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=COLONNES, delimiter=";")
            writer.writeheader()
            writer.writerows(generer_vols(jour, args.vols_par_jour))
        print(f"✔ {fichier}")


if __name__ == "__main__":
    main()
