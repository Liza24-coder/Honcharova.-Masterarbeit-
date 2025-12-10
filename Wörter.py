import os
import re
import numpy as np
from scipy.stats import mannwhitneyu


def silben_zaehlen(wort):
    vokale = "aeiouyäöü"
    wort = wort.lower()
    count = 0
    prev = False
    for c in wort:
        if c in vokale:
            if not prev:
                count += 1
            prev = True
        else:
            prev = False
    return max(count, 1)

def ist_komplex(wort):
    w = re.sub(r'[^A-Za-zÄÖÜäöüß]', '', wort)
    if not w:
        return False
    return len(w) > 7 or silben_zaehlen(w) > 3

def komplexitaet_text(text):
    woerter = re.findall(r'\w+', text)
    if not woerter:
        return 0
    komplexe_woerter = [w for w in woerter if ist_komplex(w)]
    return len(komplexe_woerter) / len(woerter)


ordner_mensch = r"C:/Users/LizaG/Desktop/Human"
ordner_gpt    = r"C:/Users/LizaG/Desktop/ChatGPT"


def lade_texte(ordner):
    texte = []
    for datei in os.listdir(ordner):
        if datei.lower().endswith(".txt"):
            pfad = os.path.join(ordner, datei)
            with open(pfad, "r", encoding="utf-8") as f:
                texte.append(f.read())
    return texte

texte_mensch = lade_texte(ordner_mensch)
texte_gpt    = lade_texte(ordner_gpt)

print("Geladene Mensch-Texte:", len(texte_mensch))
print("Geladene GPT-Texte:", len(texte_gpt))


komplex_mensch = [komplexitaet_text(t) for t in texte_mensch]
komplex_gpt    = [komplexitaet_text(t) for t in texte_gpt]

durchschnitt_mensch = np.mean(komplex_mensch)
durchschnitt_gpt    = np.mean(komplex_gpt)

print("\nDurchschnittliche Wortkomplexität (Mensch):", durchschnitt_mensch)
print("Durchschnittliche Wortkomplexität (GPT):", durchschnitt_gpt)



stat, p = mannwhitneyu(komplex_mensch, komplex_gpt, alternative='two-sided')

print("\nMann–Whitney-U-Statistik:", stat)
print("p-Wert:", p)



print("\n---------------- ERGEBNIS ----------------")

if durchschnitt_mensch > durchschnitt_gpt:
    print("❗ Menschliche Texte verwenden komplexere Wörter.")
elif durchschnitt_gpt > durchschnitt_mensch:
    print("❗ GPT-Texte verwenden komplexere Wörter.")
else:
    print("❗ Beide Gruppen haben die gleiche durchschnittliche Wortkomplexität.")

if p < 0.05:
    print("Das Ergebnis ist statistisch signifikant (p < 0.05).")
else:
    print("Das Ergebnis ist statistisch nicht signifikant (p ≥ 0.05).")