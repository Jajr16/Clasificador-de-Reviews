from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
import time
from csv import writer

############## CONSTRUCCIÓN DE CVS Y WEB SCRAPING #########################
def build_csv(opiniones, stars):
    """
        Construcción de csv (Dataset a utilizar)
    """

    with open('E:\Escritorio\Semestres ESCOM\Semestre 5 - ESCOM\Lenguaje Natural\TLN\TLN\static\csv\\reviews.csv', "a", newline="", encoding="utf-8") as feelings:
        for _, (opinion, star) in enumerate(zip(opiniones, stars)):
                        
            opinion_text = opinion.strip()
            star_text = star.text.strip().split()[0]
            print(star_text)
            print(opinion_text)
            new_data = writer(feelings)
            new_data.writerow([star_text, opinion_text])

def scroll(driver):
    """
        Función para hacer scroll en la página.

        Sirve para cargar una página dinámica completamente.
    """
    SCROLL_PAUSE_TIME = 5

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

# def clasificate(opinions, stars):
#     for _ in range(len(opinions)):
#         Proyecto.Clasificar(opinions)

def scrap(soup, driver):
    """
        Obtención de datos de la página dada.
    """

    opiniones = []
    
    stars = soup.find_all('span', {'class': 'a-icon-alt'})
    stars.pop(0)

    print('\n' + '-'*10 + ' Empezando búsqueda de campos traducidos y no traducidos ' + '-'*10)
    contenedores = driver.find_elements(By.CSS_SELECTOR, '[class="a-section celwidget"]')

    for contenedor in contenedores:
        try:#review-text-sub-contents
            if(contenedor.find_element(By.CSS_SELECTOR, '.a-size-base.reviewText.review-text-content')):
                campo_traducido = contenedor.find_element(By.CSS_SELECTOR, '.a-size-base.reviewText.review-text-content')
                opiniones.append(campo_traducido.text.replace("\n", " ").strip())          

        except Exception as e:
            print(f'Pues no estuvo ese botón {e}')
            print('-'*10 + 'Iniciando segundo intento ' + '-'*10)
            campo_normal_cont = contenedor.find_elements(By.CSS_SELECTOR, '.review-text-sub-contents')
            for opinion in campo_normal_cont:

                opinion = opinion.text.replace("\n", " ").strip()
                opiniones.append(opinion)

            

    print('\n' + '-'*10 + ' Búsqueda y extracción finalizadas ' + '-'*10)
    build_csv(opiniones, stars)

def Recorrer(driver):
    """
        Función para mostrar tantos comentarios como deje la página (Click a ver más).
    """
    scroll(driver)
    print('-'*10 + ' Desplegando más opiniones ' + '-'*10)
    while True:
        try:
            mostrar_mas = driver.find_element(By.CSS_SELECTOR, '.a-button.a-button-base.cm-cr-show-more')
            mostrar_mas.click()
            
            scroll(driver)
            
        except NoSuchElementException:
            print('El botón ya no está, adiós')
            break

    print('\n' + '-'*10 + ' Comenzando traducciones ' + '-'*10)
    try:     
        traductores = driver.find_elements(By.CSS_SELECTOR, '[class="a-size-small a-link-normal"]')
        
        for elemento in traductores:
            elemento.click()

    except Exception as e:
        print(f'El campo de las traducciones no existe {e}')

    html = driver.page_source
    # Parsear el contenido HTML de la página
    soup = BeautifulSoup(html, 'html.parser')
    scrap(soup, driver)


def scroll_stars(driver):
    """
        Función para ir a cada una de las opiniones por medio de filtros
    """
    # print('pausa')
    # for i in range(5, 0, -1):
    #for i in range(2, 1, -1):
    try:
        class_name = f'{2}star'
        product_score = driver.find_element(By.CSS_SELECTOR, f'[class*="a-link-normal"][class*="{class_name}"]') # Se pone de esta forma ya que se busca solamente el puro valor, no una clase como tal (es decir el texto en específico)
        product_score.click()

        Recorrer(driver)
    except NoSuchElementException as Ne:
        print(f'Hubo un error: {Ne}')
    
def scrap_start(urls, driver):
    urls = ['https://www.amazon.com.mx/AFA-Escritorio-Prado-Office-Blanco/dp/B094TTRZ7P/ref=lp_9757362011_1_11?pf_rd_p=a8422b71-27d5-4a7d-8254-0c9e97c83f02&pf_rd_r=K3VKHMHJQTA8K744ZNH4&sbo=RZvfv%2F%2FHxDF%2BO5021pAnSA%3D%3D&ufe=app_do%3Aamzn1.fos.4e545b5e-1d45-498b-8193-a253464ffa47&th=1','https://www.amazon.com.mx/FBXGT-Escritorio-Minimalista-Computadora-Industrial/dp/B0CJC3PW5P/ref=sr_1_2_sspa?dib=eyJ2IjoiMSJ9.vU8R8iRWRh-PlDaX8RE5kjkJ-I5wDO5-WVYRDRG2JlP4FzijOy7Nr4BD1Y-6fDiDc_atZOOUSWlhnPLHN_5iOQ.sfhchn2BjDJub4gd3VySd5L39Iu9sPotoE_CjjwlXD8&dib_tag=se&qid=1704985492&s=kitchen&sr=1-2-spons&ufe=app_do%3Aamzn1.fos.4e545b5e-1d45-498b-8193-a253464ffa47&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGZfYnJvd3Nl&th=1','https://www.amazon.com.mx/ANTUVI-Escritorio-Portátil-Ajustable-Dormitorio/dp/B0C1BCS73K/ref=sr_1_6?dib=eyJ2IjoiMSJ9.vU8R8iRWRh-PlDaX8RE5kjkJ-I5wDO5-WVYRDRG2JlP4FzijOy7Nr4BD1Y-6fDiDc_atZOOUSWlhnPLHN_5iOQ.sfhchn2BjDJub4gd3VySd5L39Iu9sPotoE_CjjwlXD8&dib_tag=se&qid=1704985492&s=kitchen&sr=1-6&ufe=app_do%3Aamzn1.fos.4e545b5e-1d45-498b-8193-a253464ffa47','https://www.amazon.com.mx/AFA-Escritorio-Prado-Office-Blanco/dp/B094TTRZ7P/ref=sr_1_15?dib=eyJ2IjoiMSJ9.vU8R8iRWRh-PlDaX8RE5kjkJ-I5wDO5-WVYRDRG2JlP4FzijOy7Nr4BD1Y-6fDiDc_atZOOUSWlhnPLHN_5iOQ.sfhchn2BjDJub4gd3VySd5L39Iu9sPotoE_CjjwlXD8&dib_tag=se&qid=1704985492&s=kitchen&sr=1-15&ufe=app_do%3Aamzn1.fos.4e545b5e-1d45-498b-8193-a253464ffa47&th=1','https://www.amazon.com.mx/ECHIGOYA-Escritorio-Ajustable-Desayuno-Cepillado/dp/B0BV1HTJ4W/ref=sr_1_18?dib=eyJ2IjoiMSJ9.vU8R8iRWRh-PlDaX8RE5kjkJ-I5wDO5-WVYRDRG2JlP4FzijOy7Nr4BD1Y-6fDiDc_atZOOUSWlhnPLHN_5iOQ.sfhchn2BjDJub4gd3VySd5L39Iu9sPotoE_CjjwlXD8&dib_tag=se&qid=1704985492&s=kitchen&sr=1-18&ufe=app_do%3Aamzn1.fos.4e545b5e-1d45-498b-8193-a253464ffa47&th=1','https://www.amazon.com.mx/DOBEVI-Escritorio-para-Dormitorio-Estructura/dp/B0C77WQMHW/ref=sr_1_21_sspa?dib=eyJ2IjoiMSJ9.vU8R8iRWRh-PlDaX8RE5kjkJ-I5wDO5-WVYRDRG2JlP4FzijOy7Nr4BD1Y-6fDiDc_atZOOUSWlhnPLHN_5iOQ.sfhchn2BjDJub4gd3VySd5L39Iu9sPotoE_CjjwlXD8&dib_tag=se&qid=1704985492&s=kitchen&sr=1-21-spons&ufe=app_do%3Aamzn1.fos.4e545b5e-1d45-498b-8193-a253464ffa47&sp_csd=d2lkZ2V0TmFtZT1zcF9idGZfYnJvd3Nl&psc=1','https://www.amazon.com.mx/TOPLIVING-Escritorio-Minimalista-Escuadra-Repisas/dp/B07RBXQPMP/ref=sr_1_25?dib=eyJ2IjoiMSJ9.3ptWPSByYcIiszlsnXzx5t8SkCex7ypnzNaWuIAQ7-x_plxoYWfZTaeYOF9nFFVbJn_0ruYxD_57zYerJ9hk4w.ZQHABiDxVcfTFkiWanntu6NfkvTBIbj-D74U3VkPO_8&dib_tag=se&qid=1704985586&s=kitchen&sr=1-25&ufe=app_do%3Aamzn1.fos.4e545b5e-1d45-498b-8193-a253464ffa47']
    
    try:
        
        for _, url in enumerate(urls):
            # Navega a la página principal
            driver.get(url)

            # Esperar a la carga de la página
            driver.implicitly_wait(10)
            # Clase del primer botón (Botón para acceder a reseñas)
            boton_css_selector = '.a-touch-link.a-box.a-touch-link-noborder.seeMostRecentReviews.a-text-bold'

        try:
            scroll(driver)
            wait = WebDriverWait(driver, 10)

            # Buscar botón
            boton = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, boton_css_selector)))
            if boton:
                # Haz clic en el botón
                boton.click()
                
                scroll_stars(driver)
                
        except Exception as e:
            print(f'No: {e}')
    finally:
        # Cierra el navegador después de procesar todas las URLs
        driver.quit()

def get_urls(driver):
    urls = []
    try:
        item_container = driver.find_elements(By.CSS_SELECTOR, '[class="a-section a-spacing-small a-spacing-top-small puis-padding-right-small"]')

        for item in item_container:
            get_url = item.find_element(By.CSS_SELECTOR, '[class="a-link-normal s-faceout-link a-text-normal"]')
            url = get_url.getAttribute("href")
            print(f'La URL es: https://www.amazon.com.mx/{url}')


    except Exception as e:
        print(f'Falló en obtención de urls {e}')

def main():
    
    busqueda = input('¿Qué deseas buscar?')
    
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')  # Evita la detección de Selenium
    chrome_options.add_argument('--ignore-ssl-errors=yes')
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Microsoft; Lumia 640 XL LTE) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.160 Mobile Safari/537.36 Edge/12.10166")

    # Habilita la aceptación automática de cookies
    chrome_options.add_argument('--enable-automation')
    chrome_options.add_argument('--disable-popup-blocking')

    # Inicia el navegador con las opciones configuradas
    driver = webdriver.Chrome(options=chrome_options)
    
    driver.get('https://www.amazon.com.mx/')

    # Esperar a la carga de la página
    driver.implicitly_wait(10)
    
    try:
        search = driver.find_element(By.CSS_SELECTOR, '.nav-input.nav-progressive-attribute')
        
        search.send_keys(busqueda)
        search.send_keys(Keys.ENTER)

        get_urls(driver)

    except Exception as e:
        print(f'Fallo en obtención de búsqueda de objeto: {e}')

if __name__ == "__main__":
    main()
    #print(detect_language("The Lucidsound LS35X headset works very well with the XBOX. Connection is simple and quick. The large volume dial on the left ear is easy to adjust without having to feel around for a dial/button. The Headset can also be muted just by tapping the left ear once  which is very convenient. The headset is very comfortable to wear for long sessions. I also like the fact that the chat mic does not need to be attached for solo players and they provide a blanking plug that covers the mic input hole. Overall these are impressive headsets, the bass sounds nice and deep and they represent the audio as it should be not at all tinny like the Stealth 600's. If you are looking for a decent pair of cans that work very well with COD these should be on your list. Unfortunately they lasted a year before the headset swivel cracked so not recommended now."))


    #a-section a-spacing-small a-spacing-top-small puis-padding-right-small
    #a-link-normal s-faceout-link a-text-normal
    #a-last