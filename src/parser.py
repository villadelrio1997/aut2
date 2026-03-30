import os
from pypdf import PdfReader
from dotenv import load_dotenv
import json

load_dotenv()

class DecretoParser:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.reader = PdfReader(pdf_path)

    def extract_range(self, start_page, end_page):
        """Extrae texto bruto de un rango de páginas (ajustado a índice 0)."""
        text = ""
        for page_num in range(start_page - 1, end_page):
            page = self.reader.pages[page_num]
            text += f"\n--- PÁGINA {page_num + 1} ---\n"
            text += page.extract_text()
        return text

    def save_raw(self, text, filename):
        os.makedirs("data/processed", exist_ok=True)
        path = f"data/processed/{filename}.txt"
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
        return path

if __name__ == "__main__":
    # Localización de Ciencias de la Naturaleza en el Decreto 209/2022
    # Nota: En este decreto, Primaria empieza tras la parte administrativa.
    # Ciencias de la Naturaleza suele estar entre la 115 y la 135 aproximadamente.
    parser = DecretoParser(os.getenv("DECRETO_PATH"))
    
    print("✂️ Extrayendo bloque de Ciencias de la Naturaleza...")
    # Vamos a extraer un rango amplio primero para localizarlo bien
    raw_text = parser.extract_range(115, 140) 
    
    saved_path = parser.save_raw(raw_text, "ciencias_naturales_raw")
    print(f"✅ Texto guardado en {saved_path}")
    print("👉 Próximo paso: Pasar este fragmento al LLM para convertirlo en JSON.")