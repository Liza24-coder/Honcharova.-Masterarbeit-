import os
import tiktoken


ordner = r"C:/Users/LizaG/Desktop/Texts"


REKURSIV = True
ANZEIGE_BEISPIELE = 20


have_docx = False
have_pdf = False
try:
    import docx
    have_docx = True
except Exception:
    pass

try:
    import PyPDF2
    have_pdf = True
except Exception:
    pass

print("Verwendeter Ordner:", ordner)
print("Rekursive Dateisuche:", REKURSIV)
print("Unterstützung für .docx:", have_docx, " .pdf:", have_pdf)
print()


alle_pfade = []
if REKURSIV:
    for wurzel, ordner_list, dateien in os.walk(ordner):
        for d in dateien:
            alle_pfade.append(os.path.join(wurzel, d))
else:
    for d in os.listdir(ordner):
        alle_pfade.append(os.path.join(ordner, d))

print("Gefundene Dateien insgesamt (alle Typen):", len(alle_pfade))


print("\nDie ersten {} Dateien:".format(min(ANZEIGE_BEISPIELE, len(alle_pfade))))
for p in alle_pfade[:ANZEIGE_BEISPIELE]:
    print(" -", p)
print()


def text_aus_datei(path):
    lower = path.lower()
    if lower.endswith(".txt"):
        try:
            with open(path, "r", encoding="utf-8", errors="replace") as f:
                return f.read()
        except Exception as e:
            print("Fehler beim Lesen der .txt-Datei:", path, ":", e)
            return ""
    if lower.endswith(".docx") and have_docx:
        try:
            doc = docx.Document(path)
            return "\n".join(absatz.text for absatz in doc.paragraphs)
        except Exception as e:
            print("Fehler beim Lesen der .docx-Datei:", path, ":", e)
            return ""
    if lower.endswith(".pdf") and have_pdf:
        try:
            textseiten = []
            with open(path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    textseiten.append(page.extract_text() or "")
            return "\n".join(textseiten)
        except Exception as e:
            print("Fehler beim Lesen der .pdf-Datei:", path, ":", e)
            return ""
    return None


texte = []
übersprungen = 0
nicht_unterstützt = 0
for p in alle_pfade:
    txt = text_aus_datei(p)
    if txt is None:
        nicht_unterstützt += 1
        continue
    if txt == "":
        übersprungen += 1
        continue
    texte.append(txt)

print("Erfolgreich gelesene Dateien:", len(texte))
print("Übersprungene Dateien (leer/Fehler):", übersprungen)
print("Nicht unterstützte Dateitypen:", nicht_unterstützt)
print()

if len(texte) == 0:
    print("Keine Textdateien wurden erfolgreich gelesen. Pfad/Dateitypen prüfen!")
    raise SystemExit


enc = tiktoken.encoding_for_model("gpt-4o")
token_anzahlen = [len(enc.encode(t)) for t in texte]

print("In die Tokenberechnung einbezogene Dateien:", len(token_anzahlen))
print("Gesamtzahl der Token:", sum(token_anzahlen))
print("Durchschnittliche Tokenzahl pro Datei:", sum(token_anzahlen)/len(token_anzahlen))


token_anzahlen_sortiert = sorted(token_anzahlen)
_min = token_anzahlen_sortiert[0]
_max = token_anzahlen_sortiert[-1]
_mid = token_anzahlen_sortiert[len(token_anzahlen_sortiert)//2]
print("Minimalzahl der Token in einer Datei:", _min)
print("Median (ungefähr):", _mid)
print("Maximalzahl der Token in einer Datei:", _max)