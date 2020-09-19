from selenium import webdriver
from selenium.webdriver.chrome.options import Options as CH_Options
from selenium.webdriver.firefox.options import Options as FF_Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver import ChromeOptions

PHONE_LIST = [
    'iPhone 5', 'iPhone 6', 'iPhone 7', 'iPhone 8', 'iPhone 8 Plus',
    'iPhone X', 'Pixel 2', 'Pixel XL', "Galaxy S5"
]
PAD_LIST = ['iPad', 'iPad Pro']


class ChromeConfig:
    headless = False
    executable_path = "chromedriver"
    chrome_options = None
    options = None
    command_executor = ""


class FirefoxConfig:
    headless = False
    executable_path = "geckodriver"
    command_executor = ""


class IEConfig:
    executable_path = "IEDriverServer.exe"
    command_executor = ""


class EdgeConfig:
    executable_path = "MicrosoftWebDriver.exe"
    command_executor = ""


class OperaConfig:
    executable_path = "operadriver"
    command_executor = ""


class SafariConfig:
    executable_path = "/usr/bin/safaridriver"
    command_executor = ""


class Browser(object):
    """
    Run class initialization method, the default is proper
    to drive the Firefox browser. Of course, you can also
    pass parameter for other browser, Chrome browser for the "Chrome",
    the Internet Explorer browser for "internet explorer" or "ie".
    :param name: Browser name
    :return:
    """

    def __init__(self, name=None, driver_path=None):
        self.name = name
        self.driver_path = driver_path

    @property
    def driver(self):
        if (self.name is None) or (self.name in ["chrome", "google chrome", "gc"]):
            return self.chrome()
        elif self.name in ["firefox", "ff"]:
            return self.firefox()
        elif self.name in ["internet explorer", "ie", "IE"]:
            return self.ie()
        elif self.name == "edge":
            return self.edge()
        elif self.name == "opera":
            return self.opera()
        elif self.name == "safari":
            return self.safari()
        elif self.name == "chrome_headless":
            return self.safari()
        elif self.name in PHONE_LIST:
            return self.phone()
        elif self.name in PAD_LIST:
            return self.pad()
        raise NameError(
            "Not found '{}' browser, See the help doc: https://github.com/SeldomQA/seldom/blob/master/docs/driver.md'.".format(self.name))

    @staticmethod
    def chrome():
        if ChromeConfig.command_executor != "":
            return webdriver.Remote(command_executor=ChromeConfig.command_executor,
                                    desired_capabilities=DesiredCapabilities.CHROME.copy())

        if ChromeConfig.headless is True:
            chrome_options = CH_Options()
            chrome_options.add_argument('--headless')
            driver = webdriver.Chrome(chrome_options=chrome_options, options=ChromeConfig.options,
                                      executable_path=ChromeConfig.executable_path)
        else:
            driver = webdriver.Chrome(options=ChromeConfig.options,
                                      executable_path=ChromeConfig.executable_path)
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
            Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
            })"""
        })
        return driver

    @staticmethod
    def firefox():
        if FirefoxConfig.command_executor != "":
            return webdriver.Remote(command_executor=FirefoxConfig.command_executor,
                                    desired_capabilities=DesiredCapabilities.FIREFOX.copy())
        if FirefoxConfig.headless is True:
            firefox_options = FF_Options()
            firefox_options.headless = True
            return webdriver.Firefox(firefox_options=firefox_options, executable_path=FirefoxConfig.executable_path)
        return webdriver.Firefox(executable_path=FirefoxConfig.executable_path)

    @staticmethod
    def ie():
        if IEConfig.command_executor != "":
            return webdriver.Remote(command_executor=IEConfig.command_executor,
                                    desired_capabilities=DesiredCapabilities.INTERNETEXPLORER.copy())
        return webdriver.Ie(executable_path=IEConfig.executable_path)

    @staticmethod
    def edge():
        if EdgeConfig.command_executor != "":
            return webdriver.Remote(command_executor=EdgeConfig.command_executor,
                                    desired_capabilities=DesiredCapabilities.EDGE.copy())
        return webdriver.Edge(executable_path=EdgeConfig.executable_path)

    @staticmethod
    def opera():
        if OperaConfig.command_executor != "":
            return webdriver.Remote(command_executor=OperaConfig.command_executor,
                                    desired_capabilities=DesiredCapabilities.OPERA.copy())
        return webdriver.Opera(executable_path=OperaConfig.executable_path)

    @staticmethod
    def safari():
        if SafariConfig.command_executor != "":
            return webdriver.Remote(command_executor=SafariConfig.command_executor,
                                    desired_capabilities=DesiredCapabilities.SAFARI.copy())
        return webdriver.Safari(executable_path=OperaConfig.executable_path)

    def phone(self):
        chrome_options = CH_Options()
        chrome_options.add_experimental_option("mobileEmulation", {"deviceName": self.name})
        driver = webdriver.Chrome(chrome_options=chrome_options,
                                  executable_path=ChromeConfig.executable_path,
                                  options=ChromeConfig.options)
        driver.set_window_size(width=480, height=900)
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
                Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
                })"""
        })
        return driver

    def pad(self):
        chrome_options = CH_Options()
        chrome_options.add_experimental_option("mobileEmulation", {"deviceName": self.name})
        driver = webdriver.Chrome(chrome_options=chrome_options,
                                  executable_path=ChromeConfig.executable_path,
                                  options=ChromeConfig.options)
        driver.set_window_size(width=1100, height=900)
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
                Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
                })"""
        })
        return driver


def browser(name=None, driver_path=None, grid_url=None):
    """
    Run class initialization method, the default is proper
    to drive the Firefox browser. Of course, you can also
    pass parameter for other browser, Chrome browser for the "Chrome",
    the Internet Explorer browser for "internet explorer" or "ie".
    :param name: Browser name
    :param driver_path: Browser driver path
    :param grid_url: Either a string representing URL of the remote server or a custom
             remote_connection.RemoteConnection object.
    :return:
    """
    CHROMEDRIVER = "chromedriver"
    FIREFOXDRIVER = "geckodriver"
    IEDRIVER = "IEDriverServer.exe"
    OPERADRIVER = "operadriver"
    EDGEDRIVER = "MicrosoftWebDriver.exe"
    SAFAIRDRIVER = "/usr/bin/safaridriver"

    # Prevention of detection
    option = ChromeOptions()
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    option.add_argument('--ignore-certificate-errors')
    if name is None:
        name = "chrome"

    if name in ["firefox", "ff"]:
        if driver_path is None:
            driver_path = FIREFOXDRIVER
        if grid_url is not None:
            return webdriver.Remote(command_executor=grid_url,
                                    desired_capabilities=DesiredCapabilities.FIREFOX.copy())
        return webdriver.Firefox(executable_path=driver_path)

    elif name in ["chrome", "google chrome", "gc"]:
        if driver_path is None:
            driver_path = CHROMEDRIVER
        if grid_url is not None:
            return webdriver.Remote(command_executor=grid_url,
                                    desired_capabilities=DesiredCapabilities.CHROME.copy())
        driver = webdriver.Chrome(options=option, executable_path=driver_path)
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
            Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
            })"""
        })
        return driver

    elif name in ["internet explorer", "ie", "IE"]:
        if driver_path is None:
            driver_path = IEDRIVER
        return webdriver.Ie(executable_path=driver_path)

    elif name == "opera":
        if driver_path is None:
            driver_path = OPERADRIVER
        return webdriver.Opera(executable_path=driver_path)

    elif name == "chrome_headless":
        if driver_path is None:
            driver_path = CHROMEDRIVER
        chrome_options = CH_Options()
        chrome_options.add_argument('--headless')
        driver = webdriver.Chrome(chrome_options=chrome_options, options=option, executable_path=driver_path)
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
            Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
            })"""
        })
        return driver

    elif name == "firefox_headless":
        firefox_options = FF_Options()
        firefox_options.headless = True
        if driver_path is None:
            driver_path = FIREFOXDRIVER
        return webdriver.Firefox(firefox_options=firefox_options, executable_path=driver_path)

    elif name == 'edge':
        if driver_path is None:
            driver_path = EDGEDRIVER
        return webdriver.Edge(executable_path=driver_path)

    elif name == 'safari':
        if driver_path is None:
            driver_path = SAFAIRDRIVER
        return webdriver.Safari(executable_path=driver_path)

    elif name in PHONE_LIST:
        if driver_path is None:
            driver_path = CHROMEDRIVER
        options = CH_Options()
        options.add_experimental_option("mobileEmulation", {"deviceName": name})
        driver = webdriver.Chrome(chrome_options=options, executable_path=driver_path, options=option)
        driver.set_window_size(width=480, height=900)
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
                    Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                    })"""
        })
        return driver

    elif name in PAD_LIST:
        if driver_path is None:
            driver_path = CHROMEDRIVER
        options = CH_Options()
        options.add_experimental_option("mobileEmulation", {"deviceName": name})
        driver = webdriver.Chrome(chrome_options=options, executable_path=driver_path, options=option)
        driver.set_window_size(width=1100, height=900)
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
                    Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                    })"""
        })
        return driver

    else:
        raise NameError(
            "Not found '{}' browser, See the help doc: https://github.com/SeldomQA/seldom/blob/master/docs/driver.md'.".format(name))
