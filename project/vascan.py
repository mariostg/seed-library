# a function to query VASCAN website https://data.canadensys.net/vascan/api/0.1/search.json?q=Actaea%20racemosa where the query string is the plant's latin name.
# the vascan API returns a JSON response with information about the plant, including its distribution, habitat, and conservation status.

# import requests

# vascan sample json return response:
# json_data = {
#     "apiVersion": "0.1",
#     "lastUpdatedDate": "2024-12-18",
#     "results": [
#         {
#             "searchedTerm": "Tiarella stolonifera",
#             "numMatches": 1,
#             "matches": [
#                 {
#                     "taxonID": 32794,
#                     "scientificName": "Tiarella stolonifera G.L. Nesom",
#                     "scientificNameAuthorship": "G.L. Nesom",
#                     "canonicalName": "Tiarella stolonifera",
#                     "taxonRank": "species",
#                     "taxonomicAssertions": [
#                         {
#                             "acceptedNameUsage": "Tiarella stolonifera G.L. Nesom",
#                             "acceptedNameUsageID": 32794,
#                             "nameAccordingTo": "Nesom, G.L. 2021. Taxonomy of Tiarella (Saxifragaceae) in the eastern USA. Phytoneuron 2021-31: 1-61",
#                             "nameAccordingToID": "https://www.phytoneuron.net/wp-content/uploads/2021/08/31PhytoN-Tiarella.pdf",
#                             "taxonomicStatus": "accepted",
#                             "parentNameUsageID": 1760,
#                             "higherClassification": "Equisetopsida;Magnoliidae;Saxifraganae;Saxifragales;Saxifragaceae;Tiarella",
#                         }
#                     ],
#                     "vernacularNames": [
#                         {
#                             "vernacularName": "stoloniferous foamflower",
#                             "language": "en",
#                             "source": "Anions, M., Proposition de nom anglais (pers. comm.)",
#                             "preferredName": true,
#                         },
#                         {
#                             "vernacularName": "tiarelle stolonifère",
#                             "language": "fr",
#                             "source": "Favreau, M. Proposition de nom français.",
#                             "preferredName": true,
#                         },
#                         {
#                             "vernacularName": "northern foamflower",
#                             "language": "en",
#                             "source": "Weakley, A.S. and Southeastern Flora Team. 2023. Flora of the southeastern United States. University of North Carolina Herbarium, North Carolina Botanical Garden, Chapel Hill, U.S.A. 2015p.",
#                             "preferredName": false,
#                         },
#                     ],
#                     "distribution": [
#                         {
#                             "locationID": "ISO 3166-2:CA-QC",
#                             "locality": "QC",
#                             "establishmentMeans": "native",
#                             "occurrenceStatus": "native",
#                         },
#                         {
#                             "locationID": "ISO 3166-2:CA-NS",
#                             "locality": "NS",
#                             "establishmentMeans": "native",
#                             "occurrenceStatus": "native",
#                         },
#                         {
#                             "locationID": "ISO 3166-2:CA-NB",
#                             "locality": "NB",
#                             "establishmentMeans": "native",
#                             "occurrenceStatus": "native",
#                         },
#                         {
#                             "locationID": "ISO 3166-2:CA-ON",
#                             "locality": "ON",
#                             "establishmentMeans": "native",
#                             "occurrenceStatus": "native",
#                         },
#                     ],
#                 }
#             ],
#         }
#     ],
# }

import json
import urllib.parse
import urllib.request


def vascan_query(latin_name: str):

    url = "https://data.canadensys.net/vascan/api/0.1/search.json"
    params = {"q": latin_name}

    query_string = urllib.parse.urlencode(params)
    full_url = f"{url}?{query_string}"
    with urllib.request.urlopen(full_url) as response:
        if response.status == 200:
            return json.loads(response.read().decode("utf-8"))
        else:
            return None


def extract_taxon_id(vascan_response):
    """
    Extract the taxonID from a VASCAN API response.

    Args:
        vascan_response (dict): The JSON response from the VASCAN API

    Returns:
        int: The taxonID if found, None otherwise
    """
    if not vascan_response or "results" not in vascan_response:
        return None

    for result in vascan_response["results"]:
        if "matches" in result and result["matches"]:
            for match in result["matches"]:
                if "taxonID" in match:
                    return match["taxonID"]
                else:
                    return None


def extract_english_name(vascan_response):
    # the english name is the value of the vernacularName where the language is "en"
    if not vascan_response or "results" not in vascan_response:
        return None

    for result in vascan_response["results"]:
        if "matches" in result and result["matches"]:
            for match in result["matches"]:
                if "vernacularNames" in match:
                    for vernacular in match["vernacularNames"]:
                        if vernacular.get("language") == "en":
                            return vernacular["vernacularName"]

    return None


def extract_french_name(vascan_response):
    # the french name is the value of the vernacularName where the language is "fr"
    if not vascan_response or "results" not in vascan_response:
        return None

    for result in vascan_response["results"]:
        if "matches" in result and result["matches"]:
            for match in result["matches"]:
                if "vernacularNames" in match:
                    for vernacular in match["vernacularNames"]:
                        if vernacular.get("language") == "fr":
                            return vernacular["vernacularName"]

    return None
