# -*- coding: utf-8 -*-
import pytest
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time


@allure.feature('Валидация форм')
@pytest.mark.forms
class TestFormValidation:
    
    URL = "https://practice-automation.com/form-fields/"
    
    @allure.title("Т-001: Ввод в поле имени")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_name_field_input(self, driver):
        with allure.step("Открыть страницу формы"):
            driver.get(self.URL)
            time.sleep(2)
        
        with allure.step("Ввести значение в поле Name"):
            name_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "name-input"))
            )
            name_input.clear()
            name_input.send_keys("Daniil Batmanov")
        
        with allure.step("Проверить сохранение значения"):
            assert name_input.get_attribute("value") == "Daniil Batmanov"
        
        allure.attach(driver.get_screenshot_as_png(), name="name_field", 
                     attachment_type=allure.attachment_type.PNG)
    
    @allure.title("Т-002: Ввод email адреса")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_email_field_input(self, driver):
        with allure.step("Открыть страницу формы"):
            driver.get(self.URL)
            time.sleep(2)
        
        with allure.step("Ввести email адрес"):
            email_input = driver.find_element(By.ID, "email")
            email_input.clear()
            email_input.send_keys("bastard@example.com")
        
        with allure.step("Проверить формат email"):
            assert "@" in email_input.get_attribute("value")
            assert "." in email_input.get_attribute("value")
        
        allure.attach(driver.get_screenshot_as_png(), name="email_field",
                     attachment_type=allure.attachment_type.PNG)
    
    @allure.title("Т-003: Проверка невалидного email")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_invalid_email_validation(self, driver):
        with allure.step("Открыть страницу формы"):
            driver.get(self.URL)
            time.sleep(2)
        
        with allure.step("Ввести невалидный email"):
            email_input = driver.find_element(By.ID, "email")
            email_input.clear()
            email_input.send_keys("invalid@")
        
        with allure.step("Попытаться отправить форму"):
            submit_btn = driver.find_element(By.TAG_NAME, "button")
            driver.execute_script("arguments[0].scrollIntoView(true);", submit_btn)
            time.sleep(0.5)
            submit_btn.click()
            time.sleep(1)
        
        allure.attach(driver.get_screenshot_as_png(), name="invalid_email",
                     attachment_type=allure.attachment_type.PNG)
    
    @allure.title("Т-004: Выбор из выпадающего списка")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_dropdown_selection(self, driver):
        with allure.step("Открыть страницу формы"):
            driver.get(self.URL)
            time.sleep(2)
        
        with allure.step("Выбрать опцию из dropdown"):
            dropdown_element = driver.find_element(By.ID, "automation")
            dropdown = Select(dropdown_element)
            options = dropdown.options
            
            if len(options) > 1:
                dropdown.select_by_index(1)
                selected = dropdown.first_selected_option
                assert selected.text != ""
        
        allure.attach(driver.get_screenshot_as_png(), name="dropdown_selected",
                     attachment_type=allure.attachment_type.PNG)
    
    @allure.title("Т-005: Переключение чекбокса")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_checkbox_toggle(self, driver):
        with allure.step("Открыть страницу формы"):
            driver.get(self.URL)
            time.sleep(2)
        
        with allure.step("Переключить чекбокс"):
            checkbox = driver.find_element(By.XPATH, "//input[@type='checkbox']")
            
            if not checkbox.is_selected():
                checkbox.click()
            
            assert checkbox.is_selected() == True
        
        with allure.step("Снять выбор чекбокса"):
            checkbox.click()
            assert checkbox.is_selected() == False
        
        allure.attach(driver.get_screenshot_as_png(), name="checkbox_toggle",
                     attachment_type=allure.attachment_type.PNG)
    
    @allure.title("Т-006: Выбор переключателя (radio button)")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_radio_button_exclusive(self, driver):
        with allure.step("Открыть страницу формы"):
            driver.get(self.URL)
            time.sleep(2)
        
        with allure.step("Найти переключатели"):
            radios = driver.find_elements(By.XPATH, "//input[@type='radio']")
            assert len(radios) >= 2
        
        with allure.step("Выбрать первый переключатель"):
            driver.execute_script("arguments[0].scrollIntoView(true);", radios[0])
            time.sleep(0.5)
            radios[0].click()
            assert radios[0].is_selected()
        
        with allure.step("Выбрать второй переключатель"):
            radios[1].click()
            assert radios[1].is_selected()
            assert not radios[0].is_selected()
        
        allure.attach(driver.get_screenshot_as_png(), name="radio_exclusive",
                     attachment_type=allure.attachment_type.PNG)
    
    @allure.title("Т-007: Ввод многострочного текста")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_textarea_input(self, driver):
        with allure.step("Открыть страницу формы"):
            driver.get(self.URL)
            time.sleep(2)
        
        with allure.step("Ввести многострочный текст"):
            message = driver.find_element(By.ID, "message")
            test_text = "Line 1\nLine 2\nLine 3"
            message.clear()
            message.send_keys(test_text)
        
        with allure.step("Проверить все строки"):
            value = message.get_attribute("value")
            assert "Line 1" in value
            assert "Line 2" in value
            assert "Line 3" in value
        
        allure.attach(driver.get_screenshot_as_png(), name="textarea_input",
                     attachment_type=allure.attachment_type.PNG)
    
    @allure.title("Т-008: Отправка формы")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_form_submission(self, driver):
        with allure.step("Открыть страницу формы"):
            driver.get(self.URL)
            time.sleep(2)
        
        with allure.step("Заполнить все поля"):
            driver.find_element(By.ID, "name-input").send_keys("Daniil Batmanov")
            driver.find_element(By.ID, "email").send_keys("bastard@test.com")
            driver.find_element(By.ID, "message").send_keys("Test message")
        
        with allure.step("Отправить форму"):
            submit_btn = driver.find_element(By.TAG_NAME, "button")
            driver.execute_script("arguments[0].scrollIntoView(true);", submit_btn)
            time.sleep(0.5)
            try:
                submit_btn.click()
            except:
                driver.execute_script("arguments[0].click();", submit_btn)
            time.sleep(2)
        
        allure.attach(driver.get_screenshot_as_png(), name="form_submitted",
                     attachment_type=allure.attachment_type.PNG)
    
    @allure.title("Т-009: Отправка пустой формы")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_empty_form_validation(self, driver):
        with allure.step("Открыть страницу формы"):
            driver.get(self.URL)
            time.sleep(2)
        
        with allure.step("Отправить пустую форму"):
            submit_btn = driver.find_element(By.TAG_NAME, "button")
            driver.execute_script("arguments[0].scrollIntoView(true);", submit_btn)
            time.sleep(0.5)
            submit_btn.click()
            time.sleep(1)
        
        allure.attach(driver.get_screenshot_as_png(), name="empty_validation",
                     attachment_type=allure.attachment_type.PNG)
    
    @allure.title("Т-010: Текст-подсказки в полях")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.regression
    def test_input_placeholders(self, driver):
        with allure.step("Открыть страницу формы"):
            driver.get(self.URL)
            time.sleep(2)
        
        with allure.step("Проверить placeholders"):
            name_input = driver.find_element(By.ID, "name-input")
            email_input = driver.find_element(By.ID, "email")
            
            name_placeholder = name_input.get_attribute("placeholder")
            email_placeholder = email_input.get_attribute("placeholder")
            
            allure.attach(
                f"Name: {name_placeholder}\nEmail: {email_placeholder}",
                name="placeholders",
                attachment_type=allure.attachment_type.TEXT
            )
        
        allure.attach(driver.get_screenshot_as_png(), name="placeholders_view",
                     attachment_type=allure.attachment_type.PNG)
