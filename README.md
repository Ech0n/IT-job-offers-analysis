# IT-job-offers-analysis


## Jak uruchomić:
1. `pip install -r requirements.txt`
2. `python pracuj/detailed.py`

## Zrobione wykresy:
- trend średnich zarobków
- średnia ilość ofert w poszczególnych miesiącach
- rozmiar firmy
- poziom stanowiska (intern/junior/mid/senior)
- średnie zarobki w województwach
- liczba ogłoszeń w województwach
- procent ofert wymagających wyksztalcenia wyższego
- inne wymagania - prawo jazdy i angielski
- W TRAKCIE ROBIENIA : minimalne lata doświadczenia

## TODO:
- [ ] Przenieść wykresy z pracuj/pracuj_charts.py do DASH-a
Wykresy z Pracuj:
- [ ] naprawić wczytywanie danych na przykładzie z C i R
- [ ] sprawdzić, czy dla ostatecznych danych nie wyjdą jakieś nieprzewidziane luki
- [ ] dokończyć wykres "requirements" - spróbować, zrobić tak, żeby domyślnie wyświetlały się tylko te najpopularniejsze (typu C, C++, Python, SQL...)
- [x] zmienić typ wykresów słupkowych z lokalizacją na mapy
- [ ] naprawić mapę
      
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


