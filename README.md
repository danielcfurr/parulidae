

  1. Obtain a Xeno-canto API key. Create a file named .env and store the key as `XENOCANTO_API_KEY=xxxx`.
  2. Update the data from Xeno-canto if necessary.
     ```bash
     python run app_utils/data.py
     ```
  3. Run the app.
     ```bash
     streamlit run Welcome.py
     ```
