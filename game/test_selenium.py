# -*- coding: utf-8 -*-
from selenium import webdriver
from django.test import LiveServerTestCase
from django.core.management import call_command


class TestApplication(LiveServerTestCase):
    def setUp(self):
        options = webdriver.FirefoxOptions()
        options.headless = True
        self.driver = webdriver.Firefox(options=options)
        self.base_url = self.live_server_url

    def tearDown(self):
        self.driver.quit()

    def test_enlace_juego_pelicula(self):
        driver = self.driver
        driver.get(self.base_url)

        driver.find_element_by_link_text("Lista de juegos").click()
        juego = driver.find_element_by_xpath("//td[3]/a").text
        driver.find_element_by_link_text(juego).click()
        self.assertEqual(juego, driver.find_element_by_xpath("//td[3]/table/tbody/tr/td").text)
        driver.find_element_by_link_text("Ver noticias de este juego").click()
        driver.find_element_by_link_text(juego).click()
        self.assertEqual(juego, driver.find_element_by_xpath("//td[3]/table/tbody/tr/td").text)
