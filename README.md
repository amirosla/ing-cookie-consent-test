# ING Cookie Consent – Automated Test

Automat testowy sprawdza, czy na stronie **ing.pl** można wyrazić zgodę wyłącznie na ciasteczka analityczne i czy po kliknięciu *Zaakceptuj wybrane* odpowiednie ciasteczka zostają zapisane w przeglądarce.

## Wymagania

- Python 3.11+
- pip

## Instalacja

```bash
# 1. Sklonuj repozytorium
git clone <URL_REPOZYTORIUM>
cd ing_zadanie

# 2. (Opcjonalnie) utwórz wirtualne środowisko
python3 -m venv .venv
source .venv/bin/activate   # Linux / macOS
.venv\Scripts\activate      # Windows

# 3. Zainstaluj zależności Python
pip install -r requirements.txt

# 4. Zainstaluj przeglądarki Playwright
playwright install --with-deps
```

## Uruchomienie testów

### Wszystkie przeglądarki jednocześnie (chromium, firefox, webkit)

```bash
pytest --browser chromium --browser firefox --browser webkit
```

### Wybrana przeglądarka

```bash
pytest --browser chromium
pytest --browser firefox
pytest --browser webkit
```

### Tryb z widocznym oknem przeglądarki

```bash
pytest --browser chromium --headed
```

### Tryb powolny (przydatny do debugowania)

```bash
pytest --browser chromium --headed --slowmo 500
```

## Struktura projektu

```
ing_zadanie/
├── tests/
│   └── test_ing_cookies.py   # Główny test
├── .github/
│   └── workflows/
│       └── tests.yml         # Pipeline GitHub Actions
├── requirements.txt
├── pytest.ini                # Konfiguracja pytest (wszystkie 3 przeglądarki)
└── README.md
```

## Opis testu

1. Otwiera `https://www.ing.pl`
2. Klika przycisk **Dostosuj** w banerze cookie
3. Włącza przełącznik ciasteczek **analitycznych** (jeśli nie jest już zaznaczony)
4. Klika **Zaakceptuj wybrane**
5. Weryfikuje, że banner zniknął oraz że w przeglądarce zapisane zostały ciasteczka świadczące o wyrażeniu zgody na analitykę (np. `OptanonConsent` z grupą C0002, `_ga`, `_gid`)

## Pipeline CI/CD (GitHub Actions)

Workflow `.github/workflows/tests.yml` uruchamia testy **równolegle** na trzech przeglądarkach przy każdym pushu i pull requeście:

```
chromium ──┐
firefox  ──┼──► (równolegle, ubuntu-latest)
webkit   ──┘
```

Logi i wyniki są dostępne w zakładce **Actions** na GitHubie.
