import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

from page.MainPage import Main


@pytest.fixture()
def browser():
    driver = webdriver.Chrome()
    driver.implicitly_wait(5)
    driver.maximize_window()
    yield browser
    driver.quit()


@allure.id('Kinopoisk_01')
@allure.feature('Поиск фильма. Без авторизации.')
@allure.title('Поиск фильма/сериала по валидному названию.'
              'Позитивная проверка.')
@allure.description('Проверить, что название введенного фильма соостветствует '
                    'отображенному названию в верхней плашке'
                    '"поиск: Девчата • результаты: 30"')
@allure.severity("Blocker")
# @pytest.mark.positive_test
def test_search_movie__main_page():
    browser = webdriver.Chrome(service=ChromeService
                               (ChromeDriverManager().install()))
    main_page = Main(browser)
    main_page.captcha()
    main_page.open_advanced_filter()
    title_serch = main_page.serch("Девчата")
    title_total = main_page.title()
    with allure.step('Проверка, что название введенного фильма'
                     'соостветствует отображенному названию'
                     'в верхней плашке).'):
        assert title_serch == title_total


@allure.id('Kinopoisk_02')
@allure.feature('Поиск фильма. Без авторизации.')
@allure.title('Поиск фильма/сериала в названии содержатся символы.'
              'Негативная проверка.')
@allure.description('Ввести невалидное название фильма (символы),'
                    'убедиться, что получаем сообщение:'
                    '"К сожалению, по вашему запросу ничего не найдено..."')
@allure.severity("Minor")
# @pytest.mark.negative_test
def test_negative_1_serch():
    browser = webdriver.Chrome(service=ChromeService
                               (ChromeDriverManager().install()))
    main_page = Main(browser)
    main_page.captcha()
    main_page.open_advanced_filter()
    main_page.serch("#")
    with allure.step('Проверка, что при невалидных данных'
                     '(введении символов в поле поиска) видим сообщение:'
                     '"К сожалению, по вашему запросу ничего не найдено...".'):
        massege = main_page.driver.find_element(By.XPATH,
                                                '//*[@id="block_left_pad"]'
                                                '/div/table/tbody/tr[1]/td/h2'
                                                ).text
        assert massege == "К сожалению, по вашему запросу ничего не найдено..."


@allure.id('Kinopoisk_03')
@allure.feature('Поиск фильма. Без авторизации.')
@allure.title('Поиск фильма/сериала с несуществующим названием. '
              'Негативная проверка.')
@allure.description('Ввести несуществующее название фильма'
                    '(бессмысленный набор букв латиница/кириллица),'
                    'убедится, что получаем сообщение: '
                    '"К сожалению,по вашему запросу ничего не найдено..."')
@allure.severity("Minor")
# @pytest.mark.negative_test
def test_negative_2_serch():
    browser = webdriver.Chrome(service=ChromeService
                               (ChromeDriverManager().install()))
    main_page = Main(browser)
    main_page.captcha()
    main_page.open_advanced_filter()
    main_page.serch("dkjbuufkflf")
    with allure.step('Проверка, что при невалидных данных'
                     '(введении символов в поле поиска) видим сообщение:'
                     '"К сожалению, по вашему запросу ничего не найдено...".'):
        massege = main_page.driver.find_element(By.XPATH,
                                                '//*[@id="block_left_pad"]'
                                                '/div/table/tbody/tr[1]/td/h2'
                                                ).text
        assert massege == "К сожалению, по вашему запросу ничего не найдено..."


@allure.id('KinopoisK_04')
@allure.feature('Поиск фильма. Без авторизации.')
@allure.title('Поиск фильма/сериала c по нескольким параметрам.'
              'Позитивная проверка.')
@allure.description('Ввести в поиск название фильма и год,'
                    'убедиться, что результат поиска соответствует ожиданиям')
@allure.severity("Critical")
# @pytest.mark.positive_test
def test_positive_2_serch():
    browser = webdriver.Chrome(service=ChromeService
                               (ChromeDriverManager().install()))
    main_page = Main(browser)
    main_page.captcha()
    main_page.open_advanced_filter()
    with allure.step('Ввод в соответствующие поля'
                     'названия фильма (title) и год (year).'):
        title = "Девчата"
        year = "1961"
    main_page.serch_title_year(title, year)
    with allure.step('Проверка, что что результат поиска'
                     'соответствует ожиданиям.'):
        result = main_page.driver.find_element(By.CSS_SELECTOR,
                                               '[itemprop="name"]').text
        # By.XPATH,'//*[@id="__next"]/div[1]/div[2]/
        # main/div[1]/div[2]/div/div[3]/div/div/div[1]/div[1]/div/div[1]/h1/span'
        assert result == f'{title} ({year})'


@allure.id('KinopoisK_05')
@allure.feature('Поиск фильма. Без авторизации.')
@allure.title('Проверка активности кнопки "Смотреть фильм".')
@allure.description('')
@allure.severity("Blocker")
# @pytest.mark.positive_test
def test_positive_button():
    browser = webdriver.Chrome(service=ChromeService
                               (ChromeDriverManager().install()))
    main_page = Main(browser)
    main_page.captcha()
    main_page.open_advanced_filter()
    main_page.serch_title_year("Девчата", "1961")
    with allure.step('Нажать на кнопку "Смотреть фильм",'
                     'убедиться, что осуществлен переход'
                     ' на страницу авторизации'):
        main_page.driver.find_element(By.CSS_SELECTOR,
                                      'button[data-test-id="Offer"]').click()


@allure.id('KinopoisK_06')
@allure.feature('Авторизация.')
@allure.title('Проверка валидности телефонного номера при входе в ЛК.'
              'Номер не зарегистрирован.')
@allure.description('В случае если номер не зарегистрирован,'
                    'то получаем сообщение:'
                    '"Можно зарегистрировать новый аккаунт".')
@allure.severity("Blocker")
# @pytest.mark.positive_test
def test_pozitive_phone_not_registered():
    browser = webdriver.Chrome(service=ChromeService
                               (ChromeDriverManager().install()))
    main_page = Main(browser)
    main_page.captcha()
    main_page.entrance_personal_account()
    with allure.step('Ввод валидного телефонного номера,'
                     'но не зарегистрированного.'):
        main_page.number_phone(9992222224)
    with allure.step('Нажать кнопку "Войти" для  перехода'
                     'на страницу ввода СМС.'):
        # нажимаем кнопку "Войти" для  перехода  на страницу ввода СМС.
        main_page.driver.find_element(By.CSS_SELECTOR,
                                      '[id="passp:sign-in"]').click()
    with allure.step('Проверка, что в случае если номер не зарегистрирован,'
                     'то получаем сообщение:'
                     '"Можно зарегистрировать новый аккаунт".'):
        massege = main_page.driver.find_element(By.XPATH, '//*[@id="root"]/'
                                                'div/div[2]/div[2]/'
                                                'div/div/div[2]/div[3]/'
                                                'div/form/div/div[2]/div'
                                                ).text
        assert massege == "Можно зарегистрировать новый аккаунт"


@allure.id('KinopoisK_07')
@allure.feature('Авторизация.')
@allure.title('Проверка валидности телефонного номера при входе в ЛК.'
              'Номер зарегистрирован.')
@allure.description('в случае если номер  зарегистрирован,'
                    'то получаем сообщение:'
                    '"Проверьте пуш-уведомления".')
@allure.severity("Blocker")
# @pytest.mark.positive_test
def test_pozitive_phone_registered():
    browser = webdriver.Chrome(service=ChromeService
                               (ChromeDriverManager().install()))
    main_page = Main(browser)
    main_page.captcha()
    main_page.entrance_personal_account()
    with allure.step('Ввод валидного телефонного номера,'
                     'зарегистрированного на Кинопоиске.'):
        main_page.number_phone(9051905932)
    with allure.step('Нажать кнопку "Войти" для  перехода'
                     'на страницу ввода СМС.'):
        main_page.driver.find_element(By.CSS_SELECTOR,
                                      '[id="passp:sign-in"]').click()
    with allure.step('Провека, что в случае если номер не зарегистрирован,'
                     'то получаем сообщение:'
                     '"Проверьте пуш-уведомления".'):
        massege = main_page.driver.find_element(By.XPATH,
                                                '//*[@id="UserEntryFlow"]/'
                                                'form/div/div[2]/div/h4'
                                                ).text
        assert massege == "Проверьте пуш-уведомления"


@allure.id('KinopoisK_08')
@allure.feature('Авторизация.')
@allure.title('Проверка телефонного номера при входе в ЛК.'
              'Номер невалидный.')
@allure.description('В случае если номер не зарегистрирован,'
                    'то получаем сообщение:'
                    '"Недопустимый формат номера".')
@allure.severity("Minor")
# @pytest.mark.negative_test
def test_negative_phone():
    browser = webdriver.Chrome(service=ChromeService
                               (ChromeDriverManager().install()))
    main_page = Main(browser)
    main_page.captcha()
    main_page.entrance_personal_account()
    with allure.step('Ввод невалидного телефонного номера'
                     '(боллее 10 символов).'):
        main_page.number_phone(905190593211)
    with allure.step('Нажать кнопку "Войти" для  перехода'
                     'на страницу ввода СМС.'):
        main_page.driver.find_element(By.CSS_SELECTOR,
                                      '[id="passp:sign-in"]').click()
    with allure.step('Проверка, что в случае если номер не валидный,'
                     'то получаем сообщение:'
                     '"Недопустимый формат номера".'):
        massege = main_page.driver.find_element(By.CSS_SELECTOR,
                                                '[id="field:input-phone:hint"]'
                                                ).text
        assert massege == "Недопустимый формат номера"
