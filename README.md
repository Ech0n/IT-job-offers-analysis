# IT-job-offers-analysis


## Jak uruchomić:
1. `pip install -r requirements.txt`
2. `python pracuj/scraper.py`

## TODO:
Scraper:
- [ ] Zaimplementować blackliste słów kluczowych. (Żeby przy wyszukiwaniu nie brało pod uwage pozycji takich jak np. Programista CNC, w tym wypadku CNC było by słowem wykluczonym)
- [x] Dodać kolejne pola do scrapowanych danych
- [x] Zaimplementować wczytywanie stanu scrapera w poprzedniej sesji, aby umożliwić wychodzenie z programu, które nie usuwa progressu.
- [ ] Umieścić writera w __init__, co może pomóc w implementacji punktu wyżej.
- [x] Rozważyć zapis szczegółowych danych do json.
- [ ] Rozdzielac scrapowane dane w elementach takich jak np: one-column-list na elementy w liscie (https://www.pracuj.pl/praca/programista-net-zachodniopomorskie,oferta,9856998)
- [ ] Jeżeli kilka ofert takich samych jest w roznych wojewodztwach to jak je liczyc