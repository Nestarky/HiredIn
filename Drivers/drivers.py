from selenium import webdriver


from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

class Chrome(webdriver.Chrome):
    def __init__(
        self,
        headless = True,
        detach = True,
        teardown = False,
        options = webdriver.ChromeOptions()
    ) -> None:
        self.teardown = teardown
        if(headless):
            options.add_argument('--headless')
        if(detach):
            options.add_experimental_option('detach' , True)
        super().__init__(
            service= Service(ChromeDriverManager().install()),
            options= options
        )
        self.implicitly_wait(10)
        self.maximize_window()
    
    def __exit__(self, exc_type, exc, traceback):
        if(self.teardown):
            return super().__exit__(exc_type, exc, traceback)



from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service

class Firefox(webdriver.Firefox):
    def __init__(
        self,
        headless = True,
        teardown = True,
        options = webdriver.FirefoxOptions()
    ) -> None:
        self.teardown = teardown
        if(headless):
            options.add_argument('--headless')
        super().__init__(
            service= Service(GeckoDriverManager().install()),
            options= options
        )
        self.implicitly_wait(10)
        self.maximize_window()

    def __exit__(self, exc_type, exc, traceback):
        if(self.teardown):
            return super().__exit__(exc_type, exc, traceback)