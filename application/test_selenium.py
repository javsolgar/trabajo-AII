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


class TestApplication(LiveServerTestCase):
    def setUp(self):
        call_command('loaddata', 'initial_data.json', verbosity=0)
        options = webdriver.FirefoxOptions()
        options.headless = False
        self.driver = webdriver.Firefox(options=options)
        self.base_url = self.live_server_url

    def tearDown(self):
        self.driver.quit()

    def test_admin_inicia_sesion(self):
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

        self.assertEqual("Opciones para admin:", driver.find_element_by_xpath("//li[4]/b").text)
        self.assertEqual("Opciones de administrador", driver.find_element_by_xpath("//li[3]/b").text)
        self.assertEqual(u"Cerrar sesión", driver.find_element_by_link_text(u"Cerrar sesión").text)

        driver.find_element_by_link_text(u"Cerrar sesión").click()
        self.assertEqual("Inicio", driver.find_element_by_xpath("//h1").text)
        self.assertEqual(u"Iniciar sesión", driver.find_element_by_link_text(u"Iniciar sesión").text)

    def test_usuario_ya_registrado(self):
        driver = self.driver

        driver.get(self.base_url)
        self.assertEqual("Inicio", driver.find_element_by_xpath("//h1").text)
        self.assertEqual("Registrarse", driver.find_element_by_link_text("Registrarse").text)

        driver.find_element_by_link_text("Registrarse").click()
        driver.find_element_by_id("id_username").click()
        driver.find_element_by_id("id_username").clear()
        driver.find_element_by_id("id_username").send_keys("prueba")
        driver.find_element_by_id("id_password1").click()
        driver.find_element_by_id("id_password1").clear()
        driver.find_element_by_id("id_password1").send_keys("963852741A")
        driver.find_element_by_id("id_password2").click()
        driver.find_element_by_id("id_password2").clear()
        driver.find_element_by_id("id_password2").send_keys("963852741A")
        driver.find_element_by_xpath("//button[@type='submit']").click()
        self.assertEqual("Registro de usuario", driver.find_element_by_xpath("//h1").text)
        self.assertEqual("A user with that username already exists.", driver.find_element_by_xpath("//p[2]").text)

    def test_registro_usuario(self):
        driver = self.driver
        driver.get(self.base_url)
        self.assertEqual("Inicio", driver.find_element_by_xpath("//h1").text)
        self.assertEqual("Registrarse", driver.find_element_by_link_text("Registrarse").text)

        driver.find_element_by_link_text("Registrarse").click()
        driver.find_element_by_id("id_username").click()
        driver.find_element_by_id("id_username").clear()
        driver.find_element_by_id("id_username").send_keys("test_registro")
        driver.find_element_by_id("id_password1").click()
        driver.find_element_by_id("id_password1").click()
        driver.find_element_by_id("id_password1").clear()
        driver.find_element_by_id("id_password1").send_keys("987456321A")
        driver.find_element_by_id("id_password2").click()
        driver.find_element_by_id("id_password2").clear()
        driver.find_element_by_id("id_password2").send_keys("987456321A")
        driver.find_element_by_xpath("//button[@type='submit']").click()
        self.assertEqual("Inicio", driver.find_element_by_xpath("//h1").text)
        self.assertEqual("Opciones para test_registro:", driver.find_element_by_xpath("//li[3]/b").text)
        self.assertEqual(u"Cerrar sesión", driver.find_element_by_link_text(u"Cerrar sesión").text)

        driver.get(self.base_url+'/registro/')
        self.assertEqual("Inicio", driver.find_element_by_xpath("//h1").text)
        self.assertEqual("Opciones para test_registro:", driver.find_element_by_xpath("//li[3]/b").text)
        self.assertEqual(u"Cerrar sesión", driver.find_element_by_link_text(u"Cerrar sesión").text)

        driver.find_element_by_link_text(u"Cerrar sesión").click()
        self.assertEqual("Registrarse", driver.find_element_by_link_text("Registrarse").text)
