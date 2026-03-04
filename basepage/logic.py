import requests
from bs4 import BeautifulSoup


def znajdz_odmiane(imie):
    # Wynikiem funkcji jest lista z wymienionymi po kolei przypadkami.
    # Przypominam, że dopełniacz (kogo? czego?) jest pod indeksem 1.
    wynik = []
    imie = imie.capitalize()
    webik = requests.get(f"https://odmiana.net/odmiana-przez-przypadki-imienia-{imie}")
    soup = BeautifulSoup(webik.content, 'html.parser')

    soup = soup.find("div", {"class",
                             "odmtab1"})  # tutaj używamy funkcji szukającej z Pięknego Mydła, która wyświetli to, co wpiszę w nawiasie
    soup = soup.find_all("p")
    for opl in soup:
        slowa = opl.get_text()
        if slowa.count(':') == 1:
            lista = slowa.split(':')
            if lista[1].count(' ') == 1:
                wynik.append(lista[1][2:].lower())
            else:
                if lista[1][-1] == '!':
                    wynik.append(lista[1][:-1].lower())
                else:
                    wynik.append(lista[1].lower())
    # dodaj_odmiane( wynik[0], wynik[1], wynik[2], wynik[3], wynik[4], wynik[5], wynik[6])
    return wynik

if __name__ == "__main__":

    print(znajdz_odmiane("piotrek"))