import requests
from bs4 import BeautifulSoup
from flask import abort

from model.Vaccine import Vaccine
from model.VaccinesList import VaccinesList

URL = "https://wwwnc.cdc.gov/travel/destinations/traveler/none/"
VACCINES_AND_MEDICINES_HTML_ID = "vaccines-and-medicines"
CLINICIAN_DISEASES_HTML_CLASS_NAME = "clinician-disease"
CLINICIAN_RECOMMENDATIONS_HTML_CLASS_NAME = "clinician-recomendations"


def getVaccines(country: str) -> VaccinesList:
    destinationUrl = URL + country
    page = requests.get(destinationUrl)

    if (page.status_code == 404):
        abort(404, response=f"Country with the name {country} could not be found.")

    # Find the "Vaccines and Medicines" table
    soup = BeautifulSoup(page.content, "html.parser")
    vaccinesAndMedicinesTable = soup.find(id=VACCINES_AND_MEDICINES_HTML_ID)
    
    # Get a list of each entry under "Vaccine for disease" in the table
    clinicianDiseases = vaccinesAndMedicinesTable.find_all(
        "td", class_=CLINICIAN_DISEASES_HTML_CLASS_NAME
    )

    # Get a list of each entry under "Recommendations" in the table
    clinicianRecommendations = vaccinesAndMedicinesTable.find_all(
        "td", class_=CLINICIAN_RECOMMENDATIONS_HTML_CLASS_NAME
    )

    # Find the disease name within each table cell
    vaccinesList = []
    for x in range(len(clinicianDiseases)):
        diseaseName = clinicianDiseases[x].text.strip()
        # TODO: For each <p> concatenate and set as recommendation
        recommendation = clinicianRecommendations[x].text.strip()
            
        vaccinesList.append(Vaccine(diseaseName, recommendation).__dict__)
    # TODO: Missing Yellow fever recommendation
    return VaccinesList(destinationUrl, vaccinesList).__dict__
