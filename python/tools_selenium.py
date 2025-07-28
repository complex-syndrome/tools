import time
from selenium import webdriver

def get_driver(headless=False):
    """_summary_
    Get a simple chrome webdriver.
    
    Args:
        headless (bool, optional): _description_. Defaults to False.

    Returns:
        _type_: _description_
    """
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument('--log-level=3')
    options.set_capability("browserVersion", "117")  # Devtools will appear if not < 118
    options.add_argument("--disable-blink-features=AutomationControlled")
    
    # May affect stability of drivers
    if headless:
        options.add_argument('--headless=new')
        options.add_argument('--disable-gpu')
    return webdriver.Chrome(options)


def scroll_to_bottom(driver, scroll_wait_time=5) -> None:
    """_summary_
    Scrolls to bottom of the webpage and waits to load, can lower scroll_wait_time if your internet is fast 

    Args:
        driver: The webdriver 
        scroll_wait_time (int, optional): Time to wait before scrolling down again. Defaults to [5] seconds.
    """
    
    if scroll_wait_time == 0: return
    
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_wait_time)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
        
        
def is_scrollable(driver, elem) -> bool:
    """_summary_
    Checks if element is scrollable
    
    Args:
        driver: The webdriver
        elem: The element to try scrolling

    Returns:
        bool: Element is scrollable (T/F)
    """
    return driver.execute_script("return arguments[0].scrollHeight > arguments[0].clientHeight;", elem)
