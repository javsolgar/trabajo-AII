# -*- coding: utf-8 -*-
from selenium import webdriver
from django.test import LiveServerTestCase
from django.core.management import call_command


class TestApplication(LiveServerTestCase):
    def setUp(self):
        call_command('loaddata', 'initial_data.json', verbosity=0)
        options = webdriver.FirefoxOptions()
        options.headless = True
        self.driver = webdriver.Firefox(options=options)
        self.base_url = self.live_server_url

    def tearDown(self):
        self.driver.quit()

    def test_admin_inicia_sesion(self):
        driver = self.driver
        driver.get(self.base_url)

        self.assertEqual("Acceder", driver.find_element_by_link_text("Acceder").text)

        driver.find_element_by_link_text("Acceder").click()
        self.assertEqual(u"Inicio de sesión", driver.find_element_by_link_text(u"Inicio de sesión").text)

        driver.find_element_by_link_text(u"Inicio de sesión").click()
        self.assertEqual(u"Inicio de sesión", driver.find_element_by_xpath("//div[@id='cover-caption']/div/div/div/form/div/h2").text)

        driver.find_element_by_id("id_username").clear()
        driver.find_element_by_id("id_username").send_keys("admin")
        driver.find_element_by_id("id_password").click()
        driver.find_element_by_id("id_password").clear()
        driver.find_element_by_id("id_password").send_keys("admin")
        driver.find_element_by_xpath("//button[@type='btn btn-primary']").click()
        self.assertEqual("admin", driver.find_element_by_link_text("admin").text)

        driver.find_element_by_link_text("admin").click()
        self.assertEqual(u"Cerrar sesión", driver.find_element_by_link_text(u"Cerrar sesión").text)

        driver.find_element_by_link_text(u"Cerrar sesión").click()
        self.assertEqual("Acceder", driver.find_element_by_link_text("Acceder").text)

        driver.find_element_by_link_text("Acceder").click()
        self.assertEqual(u"Inicio de sesión", driver.find_element_by_link_text(u"Inicio de sesión").text)

    def test_usuario_ya_registrado(self):
        driver = self.driver
        driver.get(self.base_url)

        self.assertEqual("Acceder", driver.find_element_by_link_text("Acceder").text)

        driver.find_element_by_link_text("Acceder").click()
        self.assertEqual("Registrarse", driver.find_element_by_link_text("Registrarse").text)

        driver.find_element_by_link_text("Registrarse").click()
        self.assertEqual("Registro de usuario",
                         driver.find_element_by_xpath("//div[@id='cover-caption']/div/div/div/form/h4").text)

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
        self.assertEqual("A user with that username already exists.",
                         driver.find_element_by_xpath("//div[@id='cover-caption']/div/div/div/form/div/p[2]").text)

    def test_registro_inicio_sesion_nuevo_usuario(self):
        driver = self.driver
        driver.get(self.base_url)

        # Registro del nuevo usuario
        self.assertEqual("Acceder", driver.find_element_by_link_text("Acceder").text)

        driver.find_element_by_link_text("Acceder").click()
        self.assertEqual("Registrarse", driver.find_element_by_link_text("Registrarse").text)

        driver.find_element_by_link_text("Registrarse").click()
        self.assertEqual("Registro de usuario",
                         driver.find_element_by_xpath("//div[@id='cover-caption']/div/div/div/form/h4").text)
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

        self.assertEqual("test_registro", driver.find_element_by_link_text("test_registro").text)

        driver.find_element_by_link_text("test_registro").click()
        self.assertEqual(u"Cerrar sesión", driver.find_element_by_link_text(u"Cerrar sesión").text)

        # Inicio sesión nuevo usuario
        driver.find_element_by_link_text(u"Cerrar sesión").click()
        self.assertEqual("Acceder", driver.find_element_by_link_text("Acceder").text)

        driver.find_element_by_link_text("Acceder").click()
        self.assertEqual(u"Inicio de sesión", driver.find_element_by_link_text(u"Inicio de sesión").text)

        driver.find_element_by_link_text(u"Inicio de sesión").click()
        self.assertEqual(u"Inicio de sesión",
                         driver.find_element_by_xpath("//div[@id='cover-caption']/div/div/div/form/div/h2").text)

        driver.find_element_by_id("id_username").clear()
        driver.find_element_by_id("id_username").send_keys("test_registro")
        driver.find_element_by_id("id_password").click()
        driver.find_element_by_id("id_password").clear()
        driver.find_element_by_id("id_password").send_keys("987456321A")
        driver.find_element_by_xpath("//button[@type='btn btn-primary']").click()
        self.assertEqual("test_registro", driver.find_element_by_link_text("test_registro").text)

        driver.find_element_by_link_text("test_registro").click()
        self.assertEqual(u"Cerrar sesión", driver.find_element_by_link_text(u"Cerrar sesión").text)

        driver.find_element_by_link_text(u"Cerrar sesión").click()
        self.assertEqual("Acceder", driver.find_element_by_link_text("Acceder").text)

        driver.find_element_by_link_text("Acceder").click()
        self.assertEqual(u"Inicio de sesión", driver.find_element_by_link_text(u"Inicio de sesión").text)
