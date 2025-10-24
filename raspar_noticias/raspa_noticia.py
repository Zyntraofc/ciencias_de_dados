# %%
# Bibliotecas
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import json
import time

# %%
# Configurações
chrome_options = Options()

# Desativar pop-ups e notificações
prefs = {
    "profile.default_content_setting_values.notifications": 2,
    "profile.default_content_setting_values.popups": 0,
    "profile.default_content_setting_values.geolocation": 2,
    "profile.default_content_setting_values.automatic_downloads": 1,
    "profile.default_content_setting_values.cookies": 2,
}
chrome_options.add_experimental_option("prefs", prefs)

chrome_options.add_argument("--disable-popup-blocking")
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--start-maximized")

# Criação do driver
service = Service(r".\chromedriver.exe")
chrome = webdriver.Chrome(service=service, options=chrome_options)


# %%
# Função
def pegar_texto_elemento(driver, by, locator, timeout=10):
    try:
        elemento = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, locator))
        )
        return elemento.text
    except Exception as e:
        print(f"Erro ao pegar elemento: {e}")
        return None


# %%
links_lista = [
    "https://bluestudio.estadao.com.br/agencia-de-comunicacao/releases/releases-geral/taxa-de-absenteismo-alta-traz-prejuizos-em-empresas/?utm_source=chatgpt.com",
    "https://www.oalfenense.com.br/noticia/28089/saude-mental-e-a-maior-causa-de-absenteismo-nas-empresas?",
    "https://oglobo.globo.com/economia/negocios/noticia/2025/04/08/empregados-faltam-mais-ao-trabalho-e-afetam-resultado-financeiro-das-empresas.ghtml?utm_source=chatgpt.com",
    "https://www.band.com.br/noticias/jornal-da-band/ultimas/enxaqueca-e-a-principal-causa-da-falta-de-trabalho-no-brasil-202409282002",
    "https://radios.ebc.com.br/tarde-nacional-rio-de-janeiro/2024/09/afastamento-por-depressao-e-ansiedade-no-trabalho-aumentam-50-por-cento-no-brasil"
]

manchetes = []

for link in links_lista:
    chrome.get(link)
    time.sleep(2)  # espera leve para carregamento de página
    manchete = pegar_texto_elemento(chrome, By.TAG_NAME, "h1")
    manchetes.append({"link": link, "manchete": manchete})

chrome.quit()

# %%
# Salvar em JSON
with open("manchetes.json", "w", encoding="utf-8") as f:
    json.dump(manchetes, f, ensure_ascii=False, indent=4)

print("Arquivo 'manchetes.json' criado com sucesso!")

