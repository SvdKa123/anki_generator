import os
import time

from selenium.common.exceptions import (
    ElementNotInteractableException,
    TimeoutException,
)
from selenium.webdriver import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium import webdriver
from anki_manager import AnkiManager
from pyinputplus import inputInt, inputMenu

class AnkiGenerator(AnkiManager):
    def __init__(self):
        super().__init__()
        self.driver = webdriver.Chrome()
        self.actions = ActionChains(self.driver)

    def find_and_click(self, method, path, seconds=60):
        element = WebDriverWait(self.driver, seconds).until(
            EC.element_to_be_clickable((method, path))
        )
        element.click()
        return element

    def wait_for_element(self, method, path, seconds=60):
        element = WebDriverWait(self.driver, seconds).until(
            EC.presence_of_element_located((method, path))
        )
        return element

    def wait_for_elements(self, method, path, seconds=60):
        element = WebDriverWait(self.driver, seconds).until(
            EC.presence_of_all_elements_located((method, path))
        )
        return element

    def moveTo(self, method, path, seconds=60):
        elee = WebDriverWait(self.driver, seconds).until(
            EC.element_to_be_clickable((method, path))  # Hier die Änderung
        )
        self.actions.move_to_element(elee).perform()
        # self.actions.click(elee).perform()
        return elee

    def login(self):
        login_page = self.driver.get("https://app.studysmarter.de/login/email")
        input("Please accept the cookies and press enter to continue")
        email_input = self.find_and_click(By.XPATH, "//input[@type='email']")
        email = self.actions.send_keys(self.email).perform()
        password_input = self.find_and_click(By.XPATH, "//input[@type='password']")
        password = self.actions.send_keys(self.password).perform()
        login_button = self.find_and_click(By.XPATH, "//button[@type='submit']")

    def enter_lection(self):
        x_baddne = self.find_and_click(
            By.XPATH, "//button[@class='ui-icon-button ui-size-sm ui-secondary-button']"
        )
        library_url = self.driver.get("https://app.studysmarter.de/library")
        enter_studyset_card = self.find_and_click(
            By.XPATH, "//*[text()=' Betriebs und Datensysteme ']"
        )
        add_anki = self.find_and_click(
            By.XPATH, "//*[text()=' Materialien hinzufügen ']"
        )
        choose_manual = self.find_and_click(
            By.XPATH, "//*[text()=' Manuell erstellen ']"
        )

    def load_site_correctly(self):
        start_adding = self.driver.get(
            "https://app.studysmarter.de/studyset/19593322/flashcards/create?trackingSource=add_materials_modal"
        )

    def remove_annoyance(self):
        try:
            x_button = self.find_and_click(
                By.XPATH,
                "//button[@class='ui-icon-button ui-size-sm ui-secondary-button']",
                5,
            )
        except Exception as e:
            pass

        try:
            annoying_announce = self.wait_for_element(
                By.XPATH, "//*[text()='Weiter zu Vaia']", 1
            )
            if annoying_announce:
                self.driver.refresh()
        except TimeoutException:
            pass
        library_url = self.driver.get("https://app.studysmarter.de/library")

    def add_anki(self, question: str, answers: list):
        # Hier wird das Einfügen der Frage und Antwort angepasst
        send_question = self.actions.send_keys(question).perform()
        time.sleep(1)
        answer_field = self.find_and_click(
            By.XPATH, "//*[text()=' Antwort hinzufügen ']"
        )
        for answ in answers:
            send_answer = (
                self.actions.send_keys("- ")
                .send_keys(answ)
                .send_keys(Keys.ENTER)
                .perform()
            )
            time.sleep(1)
        time.sleep(2)
        new_anki = self.find_and_click(By.XPATH, "//*[text()=' Neue Karteikarte ']")

    def delete_ankis(self, number: int):
        try:
            for _ in range(number):
                more_options = self.driver.find_elements(
                    By.XPATH, "//button[@data-cy='flashcard-list-item-more-button']"
                )
                more_options[-1].click()
                self.find_and_click(
                    By.XPATH,
                    "//ui-context-menu-item[@data-cy='context-menu-option-delete']",
                )

                choose_manual = self.find_and_click(By.XPATH, "//*[text()=' Löschen ']")
                time.sleep(2)
            return True
        except ElementNotInteractableException:
            print("reload the page")
            return True

    def display_all_topics(self):
        input()
        seven_days_grid = self.driver.find_element(
            By.XPATH,
            "//div[@class='ui-grid-layout content-group-items-wrapper ng-star-inserted']",
        )
        last_seven_days_topics = seven_days_grid.find_elements(
            By.XPATH, "//app-studyset-card[@data-cy='library-studyset-card']"
        )
        return last_seven_days_topics

    def choose_topic(self):
        topics = self.display_all_topics()
        for index, topic in enumerate(topics):
            print(f"Topic {index+1}:")
            print(f"{topic.text.replace('•', '')}\n----")
        topic_number = int(input("Choose the number to click on this topic: "))
        topics[topic_number - 1].click()
        topic_url = self.driver.current_url

    def get_links(self, topic):
        move_mouse_to_topic = self.moveTo(By.XPATH, topic)
        self.actions.key_down(Keys.CONTROL).click().key_up(Keys.CONTROL).perform()
        self.driver.switch_to.window(self.driver.window_handles[1])
        topic_link = self.driver.current_url
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])
        return topic_link

    def start_anki_learning(self):
        click_anki = self.find_and_click(By.XPATH, "pre-wrapper ng-star-inserted")


if __name__ == "__main__":
    print("Starting the instance")
    anki = AnkiGenerator()
    anki.login()
    anki.remove_annoyance()
    anki.choose_topic()

    choice = inputMenu(["Add new anki cards", "Delete Anki Cards"], numbered=True)

    match choice:
        case "Add new anki cards":
            input(
                "To add new Anki Cards, please click on 'Materialien hinzufügen'. After that click on 'Manuell erstellen'. Then the Anki Cards will be displayed. Then click on 'Frage' and just hit enter here in the terminal"
            )

            current_directory = os.getcwd()
            bullet_points_directory = os.path.join(current_directory, "bullet_points")

            files = anki.get_files_in_directory(bullet_points_directory)

            selected_file = anki.choose_file(files)

            file_path = os.path.join(bullet_points_directory, selected_file)

            qanda = anki.load_json(file_path)
            if qanda:
                print("load the file successfully")
                for question, answer in qanda.items():
                    anki.add_anki(question, answer)
                    time.sleep(1)
        case "Delete Anki Cards":
            while True:
                delete_int = inputInt(
                    prompt="Enter the amount of how many anki cards you want to delete. If you finished please press CTRL + C ot quit the Anki Generator"
                )
                anki.delete_ankis(delete_int)
