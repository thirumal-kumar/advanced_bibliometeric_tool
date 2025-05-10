import requests
import pandas as pd
import xml.etree.ElementTree as ET

def fetch_pubmed(query, from_year=None, to_year=None, article_type=None, journal=None, email=None):
    base = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
    search_url = base + "esearch.fcgi"
    fetch_url = base + "efetch.fcgi"
    term = query
    if from_year and to_year:
        term += f" AND ({from_year}[PDAT] : {to_year}[PDAT])"
    if article_type:
        term += f" AND {article_type}[Publication Type]"
    if journal:
        term += f" AND {journal}[Journal]"

    # Get total count
    params = {"db": "pubmed", "term": term, "retmode": "json", "retmax": 0}
    r = requests.get(search_url, params=params)
    r.raise_for_status()
    total = int(r.json()["esearchresult"]["count"])

    # Fetch all IDs in batches
    ids = []
    batch_size = 10000
    for start in range(0, total, batch_size):
        params = {
            "db": "pubmed",
            "term": term,
            "retmode": "json",
            "retstart": start,
            "retmax": batch_size
        }
        r = requests.get(search_url, params=params)
        r.raise_for_status()
        ids.extend(r.json()["esearchresult"]["idlist"])

    if not ids:
        return pd.DataFrame()

    # Fetch full records
    fetch_params = {"db": "pubmed", "retmode": "xml", "id": ",".join(ids)}
    r = requests.get(fetch_url, params=fetch_params)
    r.raise_for_status()
    root = ET.fromstring(r.text)

    records = []
    for article in root.findall(".//PubmedArticle"):
        title = article.findtext(".//ArticleTitle") or ""
        journal_name = article.findtext(".//Journal/Title") or ""
        year = article.findtext(".//PubDate/Year") or ""
        authors = "; ".join(
            a.findtext("LastName", "") + " " + a.findtext("ForeName", "")
            for a in article.findall(".//Author")
        )
        pmid = article.findtext(".//PMID") or ""
        doi = article.findtext(".//ArticleId[@IdType='doi']") or ""
        records.append({
            "Title": title,
            "Author": authors,
            "Journal": journal_name,
            "Date": year,
            "DOI": doi,
            "PMID": pmid,
            "Source": "PubMed"
        })
    return pd.DataFrame(records)

# Placeholder for other fetchers: fetch_scopus, fetch_ieee, fetch_openalex, fetch_europe_pmc, fetch_biorxiv, fetch_crossref
# They should accept similar filter arguments and return a pandas DataFrame with a 'Source' column.
