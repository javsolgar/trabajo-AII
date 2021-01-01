# -*- coding: utf-8 -*-
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType
import unittest, time, re
from django.test import LiveServerTestCase
from django.core.management import call_command


class UntitledTestCase(LiveServerTestCase):
    def setUp(self):
        call_command('loaddata', 'initial_data.json', verbosity=0)
        options = webdriver.ChromeOptions()
        options.headless = True
        self.driver = webdriver.Chrome(options=options)
        self.base_url = self.live_server_url
        self.accept_next_alert = True

    def tearDown(self):
        self.driver.quit()

    def test_untitled_test_case(self):
        driver = self.driver
        driver.get(self.base_url)

        self.assertEqual(u"Iniciar sesión", driver.find_element_by_link_text(u"Iniciar sesión").text)

        driver.find_element_by_link_text(u"Iniciar sesión").click()
        driver.find_element_by_id("id_username").click()
        driver.find_element_by_id("id_username").clear()
        driver.find_element_by_id("id_username").send_keys("admin")
        driver.find_element_by_id("id_password").click()
        driver.find_element_by_id("id_password").clear()
        driver.find_element_by_id("id_password").send_keys("admin")
        driver.find_element_by_xpath("//button[@type='submit']").click()

        self.assertEqual("Opciones para admin:", driver.find_element_by_xpath("//b").text)
        self.assertEqual("Opciones de administrador", driver.find_element_by_xpath("//li[4]/b").text)
        self.assertEqual(u"Cerrar sesión", driver.find_element_by_link_text(u"Cerrar sesión").text)

        driver.find_element_by_link_text(u"Cerrar sesión").click()
        self.assertEqual("Inicio", driver.find_element_by_xpath("//h1").text)
        self.assertEqual(u"Iniciar sesión", driver.find_element_by_link_text(u"Iniciar sesión").text)


