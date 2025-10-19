# 🎮 Rezolvator Spânzurătoare - Solver Automat cu Funcție Hash


# Rezolvator Spânzurătoare - Algoritm procedural fără clase

## Descriere

Acest proiect rezolvă automat jocul Hangman pentru limba română, folosind un algoritm procedural (fără clase) și funcții simple. Algoritmul:

1. Primește un cuvânt-șablon (ex: `a______i_`).
2. Pentru fiecare cuvânt din test, filtrează lista de cuvinte din DEX (din fișierul de dicționar) după lungime și literele deja cunoscute pe poziții, eliminând candidații care au litere încercate pe poziții necunoscute.
3. Solverul continuă să ghicească litere până identifică univoc cuvântul, fără propuneri directe de cuvânt.
4. Încearcă să ghicească o vocală nefolosită (cea mai frecventă în candidați). Dacă nu mai sunt vocale, trece la consoane nefolosite (cea mai frecventă).
5. Adaugă litera ghicită la secvența de încercări și la setul de litere încercate. Dacă litera ghicită e deja în pattern, elimină candidații care o au pe alte poziții decât cele cunoscute. Dacă nu, elimină candidații care nu conțin litera ghicită.
6. Actualizează patternul doar dacă cuvântul țintă este cunoscut (la testare). Dacă nu, patternul rămâne neschimbat.
7. Repetă pașii până când cuvântul este complet sau nu mai există variante.

## Structura proiectului

```
hangman-solver/
├── src/
│   ├── script_principal.py      # Script principal (CLI, fără clase)
│   ├── utilitati_hash.py         # Funcții hash și filtrare
│   └── rezolvator_spanzuratoare.py        # Algoritm procedural
├── data/
│   ├── resource.txt          # Dicționar local (DEX)
│   └── test.csv              # Fișier de test
├── results/
│   └── output.csv            # Rezultate
└── README.md
```

## Rulare

### Configurare mediu virtual (.venv) și rulare în PyCharm sau terminal

1. Deschide terminalul în folderul proiectului (`spanzuratoare-bot`).
2. Creează un mediu virtual Python:

```bash
python -m venv .venv
```

3. Activează mediul virtual:

- **Windows:**
  ```cmd
  .venv\Scripts\activate
  ```
- **Linux/Mac:**
  ```bash
  source .venv/bin/activate
  ```

4. (Opțional) Instalează pachetele din `requirements.txt` (dacă există):

```bash
pip install -r requirements.txt
```

5. Rulează rezolvatorul:

```bash
python src/script_principal.py --input data/test.csv --output results/output.csv --dict data/resource.txt
```

6. În PyCharm:

- Setează interpreterul la `.venv` (File > Settings > Project > Python Interpreter)
- Rulează scriptul cu parametrii de mai sus.

### Instrucțiuni pentru rulare în PyCharm

1. Deschide PyCharm și selectează folderul proiectului (`spanzuratoare-bot`).
2. Asigură-te că ai Python 3.8+ instalat și setat ca interpret pentru proiect (File > Settings > Project: ... > Python Interpreter).
3. Creează o nouă configurație de rulare:

- Click pe Rulare > Editare Configurații...
- Adaugă o nouă configurație de tip "Python"
  - Cale script: `src/script_principal.py`
  - Parametri: `--input data/test.csv --output results/output.csv --dict data/resource.txt`
- Director de lucru: folderul principal al proiectului

4. Rulează scriptul cu butonul verde Rulare sau cu Shift+F10.
5. Vezi rezultatele în terminalul PyCharm și în fișierul `results/output.csv`.

### Exemplu linie de comandă (CLI)

```bash
python src/script_principal.py \
  --input data/test.csv \
  --output results/out.csv \
  --dict data/resource.txt
```

1. Generează dicționarul (sau folosește unul existent cu 10.000+ cuvinte din DEX, ex: resource.txt).
2. Rulează rezolvatorul:

```bash
python src/script_principal.py --input data/test.csv --output results/output.csv --dict data/resource.txt
```

Comandă rapidă pentru rulare:

```bash
python src/script_principal.py --input data/test.csv --output results/output.csv --dict data/resource.txt
```

## Algoritmul procedural

- Algoritmul procedural implementat:
  1.  Filtrează candidații: selectează doar cuvintele care au lungimea potrivită și literele pe pozițiile cunoscute, elimină cuvintele care au litere încercate pe poziții necunoscute.
  2.  Solverul continuă să ghicească litere până identifică univoc cuvântul, fără propuneri directe de cuvânt.
  3.  Încearcă să ghicească o vocală nefolosită (cea mai frecventă în candidați). Dacă nu mai sunt vocale, trece la consoane nefolosite (cea mai frecventă).
  4.  Adaugă litera ghicită la secvența de încercări și la setul de litere încercate.
  5.  Dacă litera ghicită e deja în pattern, elimină candidații care o au pe alte poziții decât cele cunoscute. Dacă nu, elimină candidații care nu conțin litera ghicită.
  6.  Actualizează patternul doar dacă target_word e cunoscut (la testare). Dacă nu, patternul rămâne neschimbat.
  7.  Repetă pașii până când cuvântul este complet sau nu mai există variante.
  8.  La final, dacă există candidați, returnează primul; altfel, returnează tiparul curent.

## Format date

### Exemplu fișier de intrare CSV

```csv
game_id,pattern_initial,cuvant_tinta
1,st****t,student
2,*a***ă,cărare
```

### Exemplu fișier de ieșire CSV

```csv
game_id,total_incercari,cuvant_gasit,status,secventa_incercari
1,6,student,OK,e n u d s t
2,7,cărare,OK,r e ă c d a t
```
## 🎯 Performanță

- **Țintă**: < 1200 încercări totale pentru fișierul de test
- **Acuratețe**: 100% cuvinte identificate corect
