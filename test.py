from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests, time, inquirer, matplotlib
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import numpy as np

num = 0

def prendi_link_tutte_canzoni(seleziona_artista):
    xpath_lista_canzoni = '/html/body/routable-page/ng-outlet/routable-profile-page/ng-outlet/routed-page/profile-page/div[3]/div[2]/artist-songs-and-albums/div[3]'
    browser = webdriver.Firefox()
    browser.get(f'https://genius.com/artists/{seleziona_artista}')
    tutte_canzoni = browser.find_element_by_xpath(xpath_lista_canzoni)
    tutte_canzoni.click()
    time.sleep(1)
    lista_popup = browser.find_element_by_xpath('/html/body/div[7]')
    time.sleep(1)
    last_height = browser.execute_script('return arguments[0].scrollHeight', lista_popup)
    while True:
        lista_popup.send_keys(Keys.END)
        time.sleep(2)
        #calcola la nuova altezza di scrolling e comparala con l'altezza precedente
        new_height = browser.execute_script('return arguments[0].scrollHeight', lista_popup)
        # se sono uguali significa che sei arrivato in fondo
        if new_height == last_height:
            break
        last_height = new_height

    print('DEBUG: SCROLLING FINITO')

    link_pezzi = []
    lista_xpath = '/html/body/div[7]/div[1]'
    lista = browser.find_element_by_xpath(lista_xpath)
    elems = lista.find_elements_by_xpath("//a[@href]")
    for elem in elems:
        if seleziona_artista.lower() in str(elem.get_attribute('href')).lower():
            link_pezzi.append(elem.get_attribute("href"))

    print('DEBUG: LINK RACCOLTI')
    browser.close()
    browser.quit()
    return link_pezzi


def scarica_tutti_testi(link_pezzi, numero_pezzi):
    testo_completo = ''
    counter = 0
    for link in link_pezzi:
        counter += 1
        print(f'{counter}/{numero_pezzi} pezzi analizzati', end='\r')
        try:
            result = requests.get(link)
            src = result.content
            soup = BeautifulSoup(src, 'lxml')
            testo_completo += soup.find('p').getText()
        except:
            numero_pezzi -= 1 #vuol dire che ne analizzi uno in meno
            print(f'Testo di {link} impossibile da trovare')

    print('DEBUG: RACCOLTA TESTI FINITA')
    return testo_completo


def apri_lista_parolacce():
    with open('assets//Parolacce', 'r') as f:
        lista_parolacce = [line.strip() for line in f]
    return lista_parolacce


def ricerca_ricorrenze_parolacce(testo_completo, lista_parolacce, ricorrenze_parolacce):
    #itero la ricerca di ogni parolaccio nei testi e ne conto le ricorrenze
    for parolaccia in lista_parolacce:
        ricorrenze = testo_completo.lower().count(parolaccia.lower())
        if ricorrenze > 0:
            ricorrenze_parolacce[parolaccia] = ricorrenze

    #itero nel dizionario e rimuovo le parolacce presenti meno di 1 volta
    for key, value in list(ricorrenze_parolacce.items()):
        if value < 1:
            del ricorrenze_parolacce[key]

    print('DEBUG: RICERCA RICORRENZE FINITA')


#plotto le parolacce in un grafico a caso
def plotta(ricorrenze_parolacce, seleziona_artista):
    nomi_parolacce = list(ricorrenze_parolacce.keys())
    frequenza_parolacce = list(ricorrenze_parolacce.values())
    plt.title(f'Frequenza uso parolacce di {seleziona_artista}')
    plt.legend(seleziona_artista)
    bars = plt.bar(range(len(ricorrenze_parolacce)), frequenza_parolacce, align='center')
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x(), yval + .01, yval)

    plt.xticks(range(len(ricorrenze_parolacce)), nomi_parolacce)
    plt.xticks(rotation=45)
    plt.show()


def main():
    #SE USATO DA PYCHARM O UN IDE DE-COMMENTA QUESTO
    # lista_artisti_posibili = ['Fsk-satellite', 'Dark-polo-gang', 'Gallagher', 'Salmo']
    # print(f'Puoi scegliere tra: {lista_artisti_posibili}')
    # while True:
    #     seleziona_artista = input('Inserisci artista da ricercare: ')
    #     if seleziona_artista in lista_artisti_posibili:
    #         break
    #     print(f'URL di {seleziona_artista} non presente')

    #SE USATO DA COMMAND LINE USA QUESTO
    domande = [
        inquirer.List('artista',
                      message="Seleziona artista da ricercare: ",
                      choices=['Fsk-satellite', 'Dark-polo-gang', 'Gallagher', 'Salmo'],
                      carousel=True #ruota arrivato in fondo
                      ),
    ]
    seleziona_artista = inquirer.prompt(domande)
    seleziona_artista = str(seleziona_artista)[13:-2]
    print(f'Artista selezionato: {seleziona_artista}')

    link_pezzi = prendi_link_tutte_canzoni(seleziona_artista)
    numero_pezzi = len(link_pezzi) #Per un loading dinamico

    testo_completo = scarica_tutti_testi(link_pezzi, numero_pezzi)
    lista_parolacce = apri_lista_parolacce()
    # inizializzo un dizionario con tutte le parolacce e la frequenza a 0
    ricorrenze_parolacce = dict.fromkeys(lista_parolacce, 0)

    ricerca_ricorrenze_parolacce(testo_completo, lista_parolacce, ricorrenze_parolacce)
    plotta(ricorrenze_parolacce, seleziona_artista)


if __name__ == "__main__":
    main()





