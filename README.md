# IT-job-offers-analysis


## Jak uruchomić:
1. `pip install -r requirements.txt`
2. `python pracuj/detailed.py`

## TODO:
Wykresy z Pracuj:
- [ ] sprawdzić, czy dla ostatecznych danych nie wyjdą jakieś nieprzewidziane luki
- [ ] dokończyć wykres "requirements" - usunąć ostrzeżenia i spróbować, zrobić tak, żeby domyślnie wyświetlały się tylko te najpopularniejsze (typu C, C++, Python, SQL...)
- [ ] zmienić typ wykresów słupkowych z lokalizacją na mapy
      
Scraper:
- [ ] Zaimplementować blackliste słów kluczowych. (Żeby przy wyszukiwaniu nie brało pod uwage pozycji takich jak np. Programista CNC, w tym wypadku CNC było by słowem wykluczonym)
- [x] Dodać kolejne pola do scrapowanych danych
- [x] Zaimplementować wczytywanie stanu scrapera w poprzedniej sesji, aby umożliwić wychodzenie z programu, które nie usuwa progressu.
- [ ] Umieścić writera w __init__, co może pomóc w implementacji punktu wyżej.
- [x] Rozważyć zapis szczegółowych danych do json.
- [x] Rozdzielac scrapowane dane w elementach takich jak np: one-column-list na elementy w liscie (https://www.pracuj.pl/praca/programista-net-zachodniopomorskie,oferta,9856998)
- [x] Jeżeli kilka ofert takich samych jest w roznych wojewodztwach to jak je liczyc

Wykresy ze Stack-Overflow:
- [x] Uogólnić import danych z CSV, aby nie znajdował się w funkcji realizującej konkretny wykres
- [x] Zaimportować pliki z lat 2011-2016 => zaimportowano od 2014, bo wcześniej nie ma żadnych rekordów o Polakach
