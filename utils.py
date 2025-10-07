import pandas as pd
import spacy
from spellchecker import SpellChecker
from pathlib import Path

BASE_DIR = Path(__file__).parent
SYMPTOMS_CSV = BASE_DIR / "diseases_and_symptoms.csv"
DESCRIPTIONS_CSV = BASE_DIR / "disease_descriptions.csv"

if not SYMPTOMS_CSV.exists():
    SYMPTOMS_CSV = BASE_DIR / "data" / "diseases_and_symptoms.csv"
if not DESCRIPTIONS_CSV.exists():
    DESCRIPTIONS_CSV = BASE_DIR / "data" / "disease_descriptions.csv"

# Load spaCy + SpellChecker
nlp = spacy.load("en_core_web_sm")
spell = SpellChecker()

def load_symptoms_df():
    return pd.read_csv(SYMPTOMS_CSV, on_bad_lines="skip")

def load_descriptions_df():
    return pd.read_csv(DESCRIPTIONS_CSV, on_bad_lines="skip")

def extract_multi_word_symptoms(symptoms_df):
    multi_word_symptoms = set()
    for _, row in symptoms_df.iterrows():
        for i in range(1, 5):
            symptom = row.get(f"Symptom{i}")
            if isinstance(symptom, str) and len(symptom.split()) > 1:
                multi_word_symptoms.add(symptom.lower())
    return multi_word_symptoms

def process_user_input(user_input, multi_word_symptoms):
    words = user_input.split()
    corrected_words = [spell.correction(w) or w for w in words]
    corrected = " ".join(corrected_words).lower()
    words = corrected.split()

    matched = []
    def check_combo(word_list, n):
        combos = []
        for i in range(len(word_list) - n + 1):
            combo = " ".join(word_list[i:i+n])
            if combo in multi_word_symptoms:
                combos.append(combo)
        return combos
    matched.extend(check_combo(words, 2))
    matched.extend(check_combo(words, 3))

    words.extend(matched)
    return list(set(words))

def find_disease(symptoms, df):
    for _, row in df.iterrows():
        disease_symptoms = {str(row[f"Symptom{i+1}"]).lower() for i in range(4) if pd.notna(row[f"Symptom{i+1}"])}
        matches = len(set(symptoms).intersection(disease_symptoms))
        if matches >= 3:
            return row["Disease"]
    return None

def get_description(disease, lang, df):
    row = df[(df["Disease"].str.lower() == str(disease).lower()) & (df["Language Code"] == lang)]
    if not row.empty:
        return row.iloc[0]["Description"]
    return None
