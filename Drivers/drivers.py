from selenium import webdriver

class Chrome(webdriver.Chrome):
    def __init__(
        self,
        headless = False,
        detach = True,
        teardown = False,
        options = webdriver.ChromeOptions()
    ) -> None:
        self.teardown = teardown
        if(headless):
            options.add_argument('--headless')
        if(detach):
            options.add_experimental_option('detach' , True)
        super().__init__(options= options)
        self.implicitly_wait(10)
        self.maximize_window()
    
    def __exit__(self, exc_type, exc, traceback):
        if(self.teardown):
            return super().__exit__(exc_type, exc, traceback)
        

class Firefox(webdriver.Firefox):
    def __init__(
        self,
        headless = False,
        teardown = False,
        options = webdriver.FirefoxOptions()
    ) -> None:
        self.teardown = teardown
        if(headless):
            options.add_argument('--headless')
        super().__init__(options= options)
        self.implicitly_wait(10)
        self.maximize_window()

    def __exit__(self, exc_type, exc, traceback):
        if(self.teardown):
            return super().__exit__(exc_type, exc, traceback)