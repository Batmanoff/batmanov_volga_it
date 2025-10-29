# -*- coding: utf-8 -*-
import pytest
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time


@allure.feature('Взаимодействие пользователя')
@pytest.mark.interactions
class TestUserInteractions:
    
    URL = "https://practice-automation.com/click-events/"
    
    @allure.title("Т-011: Обработка одиночного клика")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_single_click(self, driver):
        with allure.step("Открыть страницу"):
            driver.get(self.URL)
            time.sleep(2)
        
        with allure.step("Найти элемент для клика"):
            buttons = driver.find_elements(By.TAG_NAME, "button")
            assert len(buttons) > 0
        
        with allure.step("Выполнить клик"):
            element = buttons[0]
            driver.execute_script("arguments[0].scrollIntoView(true);", element)
            time.sleep(0.5)
            element.click()
            time.sleep(1)
        
        allure.attach(driver.get_screenshot_as_png(), name="single_click",
                     attachment_type=allure.attachment_type.PNG)
    
    @allure.title("Т-012: Событие двойного клика")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_double_click(self, driver):
        with allure.step("Открыть страницу"):
            driver.get(self.URL)
            time.sleep(2)
        
        with allure.step("Найти элемент"):
            buttons = driver.find_elements(By.TAG_NAME, "button")
            element = buttons[1] if len(buttons) > 1 else buttons[0]
        
        with allure.step("Двойной клик"):
            driver.execute_script("arguments[0].scrollIntoView(true);", element)
            time.sleep(0.5)
            actions = ActionChains(driver)
            actions.double_click(element).perform()
            time.sleep(1)
        
        allure.attach(driver.get_screenshot_as_png(), name="double_click",
                     attachment_type=allure.attachment_type.PNG)
    
    @allure.title("Т-013: Контекстное меню")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_right_click(self, driver):
        with allure.step("Открыть страницу"):
            driver.get(self.URL)
            time.sleep(2)
        
        with allure.step("Правый клик"):
            buttons = driver.find_elements(By.TAG_NAME, "button")
            element = buttons[2] if len(buttons) > 2 else buttons[0]
            
            driver.execute_script("arguments[0].scrollIntoView(true);", element)
            time.sleep(0.5)
            actions = ActionChains(driver)
            actions.context_click(element).perform()
            time.sleep(1)
        
        allure.attach(driver.get_screenshot_as_png(), name="context_menu",
                     attachment_type=allure.attachment_type.PNG)
    
    @allure.title("Т-014: Счетчик кликов")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_click_counter(self, driver):
        with allure.step("Открыть страницу"):
            driver.get(self.URL)
            time.sleep(2)
        
        with allure.step("Кликнуть несколько раз"):
            buttons = driver.find_elements(By.TAG_NAME, "button")
            if buttons:
                element = buttons[0]
                driver.execute_script("arguments[0].scrollIntoView(true);", element)
                time.sleep(0.5)
                
                for i in range(5):
                    element.click()
                    time.sleep(0.3)
        
        allure.attach(driver.get_screenshot_as_png(), name="click_counter",
                     attachment_type=allure.attachment_type.PNG)
    
    @allure.title("Т-015: Удержание клика")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.regression
    def test_click_and_hold(self, driver):
        with allure.step("Открыть страницу"):
            driver.get(self.URL)
            time.sleep(2)
        
        with allure.step("Удержание клика"):
            buttons = driver.find_elements(By.TAG_NAME, "button")
            if buttons:
                element = buttons[0]
                driver.execute_script("arguments[0].scrollIntoView(true);", element)
                time.sleep(0.5)
                
                actions = ActionChains(driver)
                actions.click_and_hold(element).perform()
                time.sleep(2)
                actions.release(element).perform()
                time.sleep(1)
        
        allure.attach(driver.get_screenshot_as_png(), name="click_hold",
                     attachment_type=allure.attachment_type.PNG)
    
    @allure.title("Т-016: Видимость элементов")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_elements_visibility(self, driver):
        with allure.step("Открыть страницу"):
            driver.get(self.URL)
            time.sleep(2)
        
        with allure.step("Проверить видимость"):
            buttons = driver.find_elements(By.TAG_NAME, "button")
            links = driver.find_elements(By.TAG_NAME, "a")
            clickable = buttons + links
            
            visible_count = sum(1 for elem in clickable if elem.is_displayed())
            
            allure.attach(
                f"Всего: {len(clickable)}\nВидимых: {visible_count}",
                name="visibility",
                attachment_type=allure.attachment_type.TEXT
            )
            
            assert visible_count > 0
        
        allure.attach(driver.get_screenshot_as_png(), name="elements_visible",
                     attachment_type=allure.attachment_type.PNG)
    
    @allure.title("Т-017: Отключенный элемент")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_disabled_element(self, driver):
        with allure.step("Открыть страницу"):
            driver.get(self.URL)
            time.sleep(2)
        
        with allure.step("Найти отключенный элемент"):
            disabled = driver.find_elements(By.CSS_SELECTOR, "button[disabled], input[disabled]")
        
        with allure.step("Проверить отключение"):
            if disabled:
                element = disabled[0]
                is_disabled = element.get_attribute("disabled")
                assert is_disabled is not None
                
                allure.attach(
                    f"Найдено отключенных: {len(disabled)}",
                    name="disabled_info",
                    attachment_type=allure.attachment_type.TEXT
                )
        
        allure.attach(driver.get_screenshot_as_png(), name="disabled_element",
                     attachment_type=allure.attachment_type.PNG)
    
    @allure.title("Т-018: Эффекты наведения")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.regression
    def test_hover_effects(self, driver):
        with allure.step("Открыть страницу"):
            driver.get(self.URL)
            time.sleep(2)
        
        with allure.step("Наведение курсора"):
            buttons = driver.find_elements(By.TAG_NAME, "button")
            if buttons:
                element = buttons[0]
                driver.execute_script("arguments[0].scrollIntoView(true);", element)
                time.sleep(0.5)
                
                actions = ActionChains(driver)
                actions.move_to_element(element).perform()
                time.sleep(2)
        
        allure.attach(driver.get_screenshot_as_png(), name="hover_effect",
                     attachment_type=allure.attachment_type.PNG)
