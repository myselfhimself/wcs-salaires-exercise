import json

# On permet la validation du JSON brut si le module jsonschema est bien dans l'environnement Python courant.
try:
    from jsonschema import validate, ValidationError

    CAN_CHECK_SCHEMA = True
except:
    print(
        "Module 'jsonschema' non trouvé. Il n'y aura pas de validation de schéma JSON des données source."
    )
    CAN_CHECK_SCHEMA = False

import csv

# Nom du fichier JSON avec données brutes de salaire hebdomaire par filiale et employé.
DONNEES_IMPUTATIONS_BRUT: str = "employes-data-6ab4f4869d438034200738.json"
# Nom du fichier de validation JSONSchema
DONNEES_JSONSCHEMA: str = "employes-data.schema.json"
# Chemin d'écriture du fichier CSV de résumé
CSV_OUTPUT_FILENAME: str = "resume-rh.csv"


def validate_json_data(data: dict, jsonschema_filename: str) -> bool:
    """Valide les données d'un dictionnaire issu de JSON selon un JSON Schema.

    Args:
        data (dict): Données d'un JSON non encore validé.
        jsonschema_filename (dict): Nom de fichier du schéma JSON à utiliser.

    Returns:
        bool: True si le dictionnaire est valide, False avec des explications autrement.
    """
    try:
        with open(jsonschema_filename) as f:
            json_schema = json.load(f)
    except Exception as e:
        print(
            f"Impossible d'ouvrir le fichier de schéma JSON {jsonschema_filename}. Validation impossible. ({e})"
        )
        return False

    try:
        validate(instance=data, schema=json_schema)
        return True
    except ValidationError as e:
        print("❌ Erreur de validation détectée :")
        print(f"Message : {e.message}")
        print(
            f"Emplacement dans le JSON : {' -> '.join(str(p) for p in e.absolute_path)}"
        )
        return False


def generate_statistics(json_filename: str) -> dict:
    """Génère et retourne des statistiques à partir du fichier JSON fourni.

    Args:
        json_filename (str): Fichier JSON de salaires pour le groupe, ses filiales et employées.

    Returns:
        dict: Un dictionnaire reprenant les données du JSON, enrichies de statistiques. {} en cas d'échec d'ouverture du json
    """
    try:
        with open(json_filename, "r") as f:
            donnees_imputation = json.load(f)
    except Exception as e:
        print(f"Could not load file: {json_filename} (Details: {e})")
        return {}

    if CAN_CHECK_SCHEMA and not validate_json_data(
        donnees_imputation, DONNEES_JSONSCHEMA
    ):
        print(
            "Echec de validation du fichier de données. Abandon du travail statistique."
        )
        return {}

    for filiale, employes in donnees_imputation.items():
        masse_salariale_mensuelle = 0
        salaire_mensuel_moyen = 0
        salaire_mensuel_maximum = 0
        salaire_mensuel_minimum = 999999
        for employe in employes:
            salaire_hebdomadaire_hors_heures_sup = (
                employe["hourly_rate"] * employe["contract_hours"]
            )
            extra_hebdomadaire_heures_sup = (
                employe["hourly_rate"]
                * 1.5
                * (employe["weekly_hours_worked"] - employe["contract_hours"])
            )
            salaire_mensuel = (
                salaire_hebdomadaire_hors_heures_sup + extra_hebdomadaire_heures_sup
            ) * 4
            employe["salaire_mensuel"] = salaire_mensuel
            masse_salariale_mensuelle += salaire_mensuel
            if salaire_mensuel > salaire_mensuel_maximum:
                salaire_mensuel_maximum = salaire_mensuel
            if salaire_mensuel < salaire_mensuel_minimum:
                salaire_mensuel_minimum = salaire_mensuel
        salaire_mensuel_moyen = masse_salariale_mensuelle / (len(employes))

        donnees_imputation[filiale] = {
            "imputations": employes,
            "statistiques": {
                "salaire_moyen": salaire_mensuel_moyen,
                "salaire_max": salaire_mensuel_maximum,
                "salaire_min": salaire_mensuel_minimum,
                "nb_employes": len(employes),
            },
        }

    donnees_groupe = {"filiales": donnees_imputation, "statistiques": {}}
    # import pprint; pprint.pprint(donnees_groupe)

    salaire_moyen_groupe_acc = 0
    salaire_minimum_groupe = 99999999
    salaire_maximum_groupe = 0
    nb_employes = 0

    for _, donnees_filiale in donnees_groupe["filiales"].items():
        statistiques_filiale = donnees_filiale["statistiques"]
        salaire_moyen_groupe_acc += statistiques_filiale["salaire_moyen"]
        if salaire_minimum_groupe > statistiques_filiale["salaire_min"]:
            salaire_minimum_groupe = statistiques_filiale["salaire_min"]
        if salaire_maximum_groupe < statistiques_filiale["salaire_max"]:
            salaire_maximum_groupe = statistiques_filiale["salaire_max"]
        nb_employes += statistiques_filiale["nb_employes"]

    nb_filiales = len(donnees_groupe["filiales"])
    donnees_groupe["statistiques"]["salaire_moyen"] = (
        salaire_moyen_groupe_acc / nb_filiales
    )
    donnees_groupe["statistiques"]["salaire_min"] = salaire_minimum_groupe
    donnees_groupe["statistiques"]["salaire_max"] = salaire_maximum_groupe
    donnees_groupe["statistiques"]["nb_employes"] = nb_employes

    return donnees_groupe


def print_bar() -> None:
    """Affiche une barre horizontale"""
    print("=" * 70)


def print_employees_salaries(employes: list[dict]) -> None:
    """Affiche en colonnes le nom, poste, salaire mensuel d'un bloc d'employés.

    Args:
        employes (list[dict]): Liste de dictionnaires d'employés, chacun ayant pour clé "job", "name", "salaire_mensuel".
    """
    for employe in employes:
        print(
            f"{employe["name"].ljust(15)} | {employe["job"].ljust(20)}| Salaire mensuel: {employe["salaire_mensuel"]:.2f}€"
        )


def print_hr_statistics(stats: dict, entite: str) -> None:
    """Affiche les statistiques RH d'un bloc de données statistiques.

    Args:
        stats (dict): Bloc de données statistiques, avec les clés "salaire_moyen", "salaire_max", "salaire_min", "nb_employes".
        entite (str): Nom du groupe de l'entité, commençant par un déterminant le/la/l'.
    """
    print_bar()
    print()
    print(f"Statistiques des salaires pour {entite}:")
    print(f"Salaire moyen: {stats["salaire_moyen"]:.2f}€")
    print(f"Salaire le plus élevé: {stats["salaire_max"]:.2f}€")
    print(f"Salaire le plus bas: {stats["salaire_min"]:.2f}€")
    print(f"Nombre d'employés: {stats["nb_employes"]}")
    print()
    print_bar()


def print_group_statistics(donnees_groupe: dict) -> None:
    """Affiche les statistiques de tout le groupe.

    Args:
        donnees_groupe (dict): Dictionnaire profond des salaires & statistiques du groupe et ses filiales.
    """
    print("Groupe")
    print()
    print_hr_statistics(donnees_groupe["statistiques"], "le groupe")
    print()

    for nom_filiale, donnees_filiale in donnees_groupe["filiales"].items():
        print(f"Entreprise: {nom_filiale}")
        print()
        print_employees_salaries(donnees_filiale["imputations"])
        print()
        print_hr_statistics(
            donnees_filiale["statistiques"], f"l'entreprise {nom_filiale}"
        )

def generate_csv_summary(group_stats):
    with open(CSV_OUTPUT_FILENAME, "w") as csvfile:
        writer = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL) 
        writer.writerow(["Filiale", "")


def main():
    group_stats = generate_statistics(DONNEES_IMPUTATIONS_BRUT)
    print_group_statistics(group_stats)
    # generate_csv_summary()


if __name__ == "__main__":
    main()
