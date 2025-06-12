import requests
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()
XENO_CANTO_API_KEY = os.getenv("XENOCANTO_API_KEY")

THIS_DIR = Path(__file__).resolve().parent
PROJECT_DIR = THIS_DIR.parent

RAW_DATA_PATH = PROJECT_DIR / "data" / "raw_xeno_canto.csv"
CLEAN_DATA_PATH = PROJECT_DIR / "data" / "clean_xeno_canto.csv"


def retrieve_raw_data(per_page=500, max_pages=None) -> None:
    query_params = [("fam", "parulidae"), ("cnt", "united states"), ("since", "2015-01-01")]
    recordings = []

    print("Retrieving page 1")
    first_result = query_xeno_canto(query_params=query_params, api_key=XENO_CANTO_API_KEY, per_page=per_page, page=1)
    recordings += first_result['recordings']

    if max_pages is None:
        pages = first_result['numPages']
    else:
        pages = min(first_result['numPages'], max_pages)

    for p in range(2, pages + 1):
        print("Retrieving page", p, "of", pages)
        next_result = query_xeno_canto(query_params=query_params, api_key=XENO_CANTO_API_KEY, per_page=per_page, page=p)
        recordings += next_result['recordings']

    RAW_DATA_PATH.parent.mkdir(exist_ok=True)
    pd.DataFrame(recordings).to_csv(RAW_DATA_PATH, index=False)


def query_xeno_canto(query_params: list, api_key: str, per_page: int = 100, page: int = 1) -> dict:
    """Function to make request to Xeno-Canto"""
    base_url = "https://xeno-canto.org/api/3/recordings"
    query_string = ' '.join([f'{key}:"{item}"' for key, item in query_params])
    params = {"query": query_string, "key": api_key, "per_page": per_page, "page": page}
    response = requests.get(base_url, params=params)
    if response.ok:
        return response.json()
    else:
        response.raise_for_status()


def load_clean_data() -> pd.DataFrame:
    df = pd.read_csv(RAW_DATA_PATH, index_col='id')

    df['scientific_name'] = df['gen'] + ' ' + df['sp']

    df['lat'] = df['lat'].astype('float')
    df['lon'] = df['lon'].astype('float')
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df['uploaded'] = pd.to_datetime(df['uploaded'], errors='coerce')

    df = df.dropna(subset=['lat', 'lon', 'date', 'uploaded'])

    df['q_score'] = df['q'].map({'E': 0, 'D': 1, 'C': 2, 'B': 3, 'A': 4})

    return df


if __name__ == "__main__":
    retrieve_raw_data()
