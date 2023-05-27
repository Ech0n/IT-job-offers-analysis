# IT-job-offers-analysis


## Jak uruchomić:
1. `pip install -r requirements.txt`
2. `python pracuj/scraper.py`

## TODO:
Scraper:
- [ ] Zaimplementować blackliste słów kluczowych. (Żeby przy wyszukiwaniu nie brało pod uwage pozycji takich jak np. Programista CNC, w tym wypadku CNC było by słowem wykluczonym)
- [ ] Dodać kolejne pola do scrapowanych danych
- [ ] Zaimplementować wczytywanie stanu scrapera w poprzedniej sesji, aby umożliwić wychodzenie z programu, które nie usuwa progressu.
- [ ] Umieścić writera w __init__, co może pomóc w implementacji punktu wyżej.
