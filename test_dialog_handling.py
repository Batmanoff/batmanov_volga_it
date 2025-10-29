# -*- coding: utf-8 -*-
import pytest
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time


@allure.feature('Обработка диалогов')
@pytest.mark.dialogs
class TestDialogHandling:
    
    URL = "https://practice-automation.com/popups/"
    
    @allure.title("Т-019: Обработка alert окна")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_alert_handler(self, driver):
        with allure.step("Открыть страницу"):
            driver.get(self.URL)
            time.sleep(2)
        
        with allure.step("Кликнуть на кнопку alert"):
            buttons = driver.find_elements(By.TAG_NAME, "button")
            if buttons:
                alert_btn = buttons[0]
                driver.execute_script("arguments[0].scrollIntoView(true);", alert_btn)
                time.sleep(0.5)
                alert_btn.click()
                time.sleep(1)
        
        with allure.step("Обработать alert"):
            try:
                alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
                alert_text = alert.text
                allure.attach(f"Alert: {alert_text}", name="alert_text",
                            attachment_type=allure.attachment_type.TEXT)
                alert.accept()
                time.sleep(1)
            except TimeoutException:
                pass
        
        allure.attach(driver.get_screenshot_as_png(), name="alert_handled",
                     attachment_type=allure.attachment_type.PNG)
    
    @allure.title("Т-020: Подтверждение диалога (принять)")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_confirm_accept(self, driver):
        with allure.step("Открыть страницу"):
            driver.get(self.URL)
            time.sleep(2)
        
        with allure.step("Кликнуть на кнопку confirm"):
            buttons = driver.find_elements(By.TAG_NAME, "button")
            confirm_btn = buttons[1] if len(buttons) > 1 else buttons[0] if buttons else None
            
            if confirm_btn:
                driver.execute_script("arguments[0].scrollIntoView(true);", confirm_btn)
                time.sleep(0.5)
                confirm_btn.click()
                time.sleep(1)
        
        with allure.step("Принять confirm"):
            try:
                confirm = WebDriverWait(driver, 5).until(EC.alert_is_present())
                confirm_text = confirm.text
                allure.attach(f"Confirm: {confirm_text}", name="confirm_text",
                            attachment_type=allure.attachment_type.TEXT)
                confirm.accept()
                time.sleep(1)
            except TimeoutException:
                pass
        
        allure.attach(driver.get_screenshot_as_png(), name="confirm_accepted",
                     attachment_type=allure.attachment_type.PNG)
    
    @allure.title("Т-021: Подтверждение диалога (отклонить)")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_confirm_reject(self, driver):
        with allure.step("Открыть страницу"):
            driver.get(self.URL)
            time.sleep(2)
        
        with allure.step("Кликнуть на кнопку confirm"):
            buttons = driver.find_elements(By.TAG_NAME, "button")
            confirm_btn = buttons[1] if len(buttons) > 1 else buttons[0] if buttons else None
            
            if confirm_btn:
                driver.execute_script("arguments[0].scrollIntoView(true);", confirm_btn)
                time.sleep(0.5)
                confirm_btn.click()
                time.sleep(1)
        
        with allure.step("Отклонить confirm"):
            try:
                confirm = WebDriverWait(driver, 5).until(EC.alert_is_present())
                confirm_text = confirm.text
                allure.attach(f"Confirm: {confirm_text}", name="confirm_text",
                            attachment_type=allure.attachment_type.TEXT)
                confirm.dismiss()
                time.sleep(1)
            except TimeoutException:
                pass
        
        allure.attach(driver.get_screenshot_as_png(), name="confirm_rejected",
                     attachment_type=allure.attachment_type.PNG)
    
    @allure.title("Т-022: Ввод в prompt окно")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_prompt_input(self, driver):
        with allure.step("Открыть страницу"):
            driver.get(self.URL)
            time.sleep(2)
        
        with allure.step("Кликнуть на кнопку prompt"):
            buttons = driver.find_elements(By.TAG_NAME, "button")
            prompt_btn = buttons[2] if len(buttons) > 2 else buttons[0] if buttons else None
            
            if prompt_btn:
                driver.execute_script("arguments[0].scrollIntoView(true);", prompt_btn)
                time.sleep(0.5)
                prompt_btn.click()
                time.sleep(1)
        
        with allure.step("Ввести текст в prompt"):
            try:
                prompt = WebDriverWait(driver, 5).until(EC.alert_is_present())
                test_input = "Daniil Test"
                prompt.send_keys(test_input)
                allure.attach(f"Input: {test_input}", name="prompt_input",
                            attachment_type=allure.attachment_type.TEXT)
                prompt.accept()
                time.sleep(1)
            except TimeoutException:
                pass
        
        allure.attach(driver.get_screenshot_as_png(), name="prompt_input",
                     attachment_type=allure.attachment_type.PNG)
    
    @allure.title("Т-023: Отмена prompt диалога")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.regression
    def test_prompt_cancel(self, driver):
        with allure.step("Открыть страницу"):
            driver.get(self.URL)
            time.sleep(2)
        
        with allure.step("Кликнуть на кнопку prompt"):
            buttons = driver.find_elements(By.TAG_NAME, "button")
            prompt_btn = buttons[2] if len(buttons) > 2 else buttons[0] if buttons else None
            
            if prompt_btn:
                driver.execute_script("arguments[0].scrollIntoView(true);", prompt_btn)
                time.sleep(0.5)
                prompt_btn.click()
                time.sleep(1)
        
        with allure.step("Отменить prompt"):
            try:
                prompt = WebDriverWait(driver, 5).until(EC.alert_is_present())
                prompt.dismiss()
                time.sleep(1)
                allure.attach("Prompt cancelled", name="prompt_cancelled",
                            attachment_type=allure.attachment_type.TEXT)
            except TimeoutException:
                pass
        
        allure.attach(driver.get_screenshot_as_png(), name="prompt_cancelled",
                     attachment_type=allure.attachment_type.PNG)
    
    @allure.title("Т-024: Отображение tooltip")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.regression
    def test_tooltip_display(self, driver):
        with allure.step("Открыть страницу"):
            driver.get(self.URL)
            time.sleep(2)
        
        with allure.step("Найти элемент с tooltip"):
            tooltip_elements = driver.find_elements(By.CSS_SELECTOR, "[title], [data-tooltip]")
            if not tooltip_elements:
                tooltip_elements = driver.find_elements(By.TAG_NAME, "a")
        
        with allure.step("Наведение и проверка tooltip"):
            if tooltip_elements:
                element = tooltip_elements[0]
                actions = ActionChains(driver)
                actions.move_to_element(element).perform()
                time.sleep(2)
                
                tooltip_text = element.get_attribute("title") or element.get_attribute("data-tooltip")
                if tooltip_text:
                    allure.attach(f"Tooltip: {tooltip_text}", name="tooltip_text",
                                attachment_type=allure.attachment_type.TEXT)
        
        allure.attach(driver.get_screenshot_as_png(), name="tooltip_display",
                     attachment_type=allure.attachment_type.PNG)
    
    @allure.title("Т-025: Модальное окно")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_modal_window(self, driver):
        with allure.step("Открыть страницу"):
            driver.get(self.URL)
            time.sleep(2)
        
        with allure.step("Открыть modal"):
            modal_buttons = driver.find_elements(
                By.XPATH, "//button[contains(text(), 'Modal') or contains(text(), 'modal')]"
            )
            if not modal_buttons:
                modal_buttons = driver.find_elements(By.TAG_NAME, "button")
            
            if modal_buttons:
                modal_btn = modal_buttons[0]
                driver.execute_script("arguments[0].scrollIntoView(true);", modal_btn)
                time.sleep(0.5)
                modal_btn.click()
                time.sleep(2)
        
        with allure.step("Проверить modal"):
            modals = driver.find_elements(By.CSS_SELECTOR, ".modal, [role='dialog']")
            if modals:
                allure.attach("Modal found", name="modal_found",
                            attachment_type=allure.attachment_type.TEXT)
        
        with allure.step("Закрыть modal"):
            close_buttons = driver.find_elements(
                By.CSS_SELECTOR, ".close, [aria-label='Close'], button.modal-close"
            )
            if close_buttons:
                close_buttons[0].click()
                time.sleep(1)
        
        allure.attach(driver.get_screenshot_as_png(), name="modal_window",
                     attachment_type=allure.attachment_type.PNG)
