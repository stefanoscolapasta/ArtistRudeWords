from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests, time, inquirer, matplotlib
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt


def prendi_link_tutte_canzoni(seleziona_artista):
    xpath_lista_canzoni = '/html/body/routable-page/ng-outlet/routable-profile-page/ng-outlet/routed-page/profile-page/div[3]/div[2]/artist-songs-and-albums/div[3]'
    browser = webdriver.Firefox()
    browser.set_window_position(x=960, y=0)
    browser.set_window_size(960, 1080)
    browser.get(f'https://genius.com/artists/{seleziona_artista}')
    tutte_canzoni = browser.find_element_by_xpath(xpath_lista_canzoni)
    tutte_canzoni.click()
    time.sleep(1)
    lista_popup = browser.find_element_by_xpath('/html/body/div[7]')
    time.sleep(2)
    last_height = browser.execute_script('return arguments[0].scrollHeight', lista_popup)
    time.sleep(1)
    while True:
        lista_popup.send_keys(Keys.END)
        time.sleep(2)
        #calcola la nuova altezza di scrolling e comparala con l'altezza precedente
        new_height = browser.execute_script('return arguments[0].scrollHeight', lista_popup)
        # se sono uguali significa che sei arrivato in fondo
        if new_height == last_height:
            break
        last_height = new_height

    print('DEBUG: SCROLLING FINISHED')

    link_pezzi = []
    lista_xpath = '/html/body/div[7]/div[1]'
    lista = browser.find_element_by_xpath(lista_xpath)
    elems = lista.find_elements_by_css_selector("div.profile_list_item a") #entro nel div con class name = profilo_list_item nell'elemento a
    for elem in elems:
        link_pezzi.append(elem.get_attribute("href"))

    print('DEBUG: LINKS COLLECTED')
    browser.close()
    browser.quit()
    return link_pezzi


def scarica_tutti_testi(link_pezzi, numero_pezzi):
    testo_completo = ''
    counter = 0
    print('  ')
    for link in link_pezzi:

        print(f'  {counter}/{numero_pezzi} songs analyzed', end='\r')
        try:
            counter += 1
            result = requests.get(link)
            src = result.content
            soup = BeautifulSoup(src, 'lxml')
            testo_completo += soup.find('p').getText()
        except:
            counter -= 1
            numero_pezzi -= 1 #vuol dire che ne analizzi uno in meno
            print(f'LYRICS OF {link} IMPOSSIBLE TO FIND')

    print('DEBUG: LYRYCS RETRIEVAL FINISHED')
    return testo_completo


def apri_lista_parolacce(seleziona_lingua):
    if seleziona_lingua == 'Italian':
        with open('assets//Parolacce', 'r') as f:
            lista_parolacce = [line.strip() for line in f]
        return lista_parolacce
    if seleziona_lingua == 'English':
        with open('assets//swear-words', 'r') as f:
            rude_words_list = [line.strip() for line in f]
        return rude_words_list


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

    print('DEBUG: SWEAR-WORD FREQUENCY SEARCH FINISHED')


#plotto le parolacce in un grafico a caso
def plotta(ricorrenze_parolacce, seleziona_artista):
    nomi_parolacce = list(ricorrenze_parolacce.keys())
    frequenza_parolacce = list(ricorrenze_parolacce.values())
    plt.title(f'Swear-word use frequency of {seleziona_artista}')
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
                      message="Select artist to search: ",
                      choices=['6ix9ine','Eminem','Ski-and-wok','Fabrizio-de-andre','Anna', 'Yung-lean','Fsk-satellite', 'Dark-polo-gang', 'Gallagher', 'Salmo'],
                      carousel=True #ruota arrivato in fondo
                      ),
    ]
    seleziona_artista = inquirer.prompt(domande)
    seleziona_artista = str(seleziona_artista)[13:-2] #I strip extra data
    print(f'Selected artist: {seleziona_artista}', end='\n\n')

    domande = [
        inquirer.List('language',
                      message="Select artist's main language: ",
                      choices=['Italian', 'English'],
                      carousel=True  # ruota arrivato in fondo
                      ),
    ]
    seleziona_lingua = inquirer.prompt(domande)
    seleziona_lingua = str(seleziona_lingua)[14:-2]
    print(f'Selected language: {seleziona_lingua}', end='\n\n')

    link_pezzi = prendi_link_tutte_canzoni(seleziona_artista)
    link_pezzi = list(set(link_pezzi)) #rimuovo i doppioni
    numero_pezzi = len(link_pezzi) #Per un loading dinamico

    testo_completo = scarica_tutti_testi(link_pezzi, numero_pezzi)
    lista_parolacce = apri_lista_parolacce(seleziona_lingua)
    # inizializzo un dizionario con tutte le parolacce e la frequenza a 0
    ricorrenze_parolacce = dict.fromkeys(lista_parolacce, 0)

    ricerca_ricorrenze_parolacce(testo_completo, lista_parolacce, ricorrenze_parolacce)
    plotta(ricorrenze_parolacce, seleziona_artista)


if __name__ == "__main__":
    main()





