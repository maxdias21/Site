from pathlib import Path
# Módulos selenium
from selenium.webdriver.chrome.service import Service
from selenium import webdriver

# Ir até a pasta do chromedriver.exe
ROOT_PATH = Path(__file__).parent.parent.parent.parent.resolve()
CHROMEDRIVER_NAME = 'chromedriver/chromedriver.exe'
CHROMEDRIVER_PATH = ROOT_PATH / CHROMEDRIVER_NAME

def make_chrome_browser(*options):
    chrome_options = webdriver.ChromeOptions()

    # Adicionar argumentos para o navegador
    # --headless - faz os testes sem abrir o navegador, ele executa, mas não vê
    if options is not None:
        for option in options:
            chrome_options.add_argument(option)

    chrome_service = Service(executable_path=str(CHROMEDRIVER_PATH))
    browser = webdriver.Chrome(service=chrome_service, options=chrome_options)

    return browser
