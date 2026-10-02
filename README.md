# Draw It! — Narysuj to!

Imprezowa gra z rysowanymi rebusami dla 2–20 drużyn. Ten sam wygląd i inicjacja co w „Pokaż to!”. PHP 8.1+, JavaScript, bez bazy danych i zależności.

Uruchom `php -S 127.0.0.1:8018` i otwórz http://127.0.0.1:8018/. Na hostingu wgraj projekt do osobnego katalogu `drawIt`, z PHP i HTTPS. Katalog `data` musi być zapisywalny przez PHP dla licznika gier.

Wybierz kategorie, dodaj drużyny, ustaw 15–300 sekund i przetestuj dźwięk. „Nowa gra” zeruje wyniki. Podaj telefon osobie rysującej i przygotuj papier oraz pisak. START odsłania jedno hasło i uruchamia czas. Rysuj bez mówienia, liter i cyfr. Przycisk „Zgadnięte!” przyznaje jeden punkt i kończy turę. Upływ czasu kończy turę bez punktu. Następnie gra kolejna drużyna, a punkty sumują się przez kolejne rundy.

Pokój to osobna sesja przeglądarki `drawit`, niezależna od `showit` i pozostałych gier. Kod pokoju jest identyfikatorem, nie kodem do dołączania z innych urządzeń. Odświeżenie zachowuje stan, wyniki i termin końca tury. Serwer pilnuje czasu i zapobiega powtórnemu naliczeniu punktu.

Rysowanie odbywa się na papierze. Telefon wyświetla hasło osobie rysującej oraz obsługuje czas i wyniki.

143 nowe wielowyrazowe hasła: przysłowia, powiedzenia, tytuły filmów, bajki i książki oraz tytuły piosenek. Początkowa pula nie zawiera haseł z projektów „Pokaż to!” i „Kto kręci?”. Pliki `data/categories/*.json` mają pola `name`, `emoji`, `words`. Jednowyrazowe hasła są pomijane. Talia nie powtarza haseł do wyczerpania puli.

Dźwięk korzysta z Web Audio aktywowanego przyciskiem START lub „Sprawdź dźwięk”. Zostaw stronę na ekranie i ustaw głośność. Po powrocie z uśpienia stan synchronizuje się z serwerem; mobilna przeglądarka może wstrzymać sygnał w tle. Test dźwięku warto wykonać na telefonie przed grą.

`stats.php` udostępnia licznik `gamesPlayed`, zwiększany przy pierwszym START nowej gry. Zachowaj `data/games-played.json` podczas aktualizacji.

Test: przy uruchomionym lokalnym serwerze wykonaj `python3 tests/smoke.py`. Sprawdza osobne pokoje, CSRF, walidację, jedno hasło na turę, punktację, ponowione żądanie, odświeżenie, upływ czasu, zmianę drużyny, reset i licznik gier.
