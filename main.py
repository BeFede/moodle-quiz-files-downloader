import os
import requests
from bs4 import BeautifulSoup

class MoodleManager:
    def __init__(self, moodle_url, session):
        self.moodle_url = moodle_url
        self.session = session

    def get_attempt_urls(self, quiz_id):
        quiz_report_url = f"{self.moodle_url}/mod/quiz/report.php?id={quiz_id}&mode=overview"
        response = self.session.get(quiz_report_url)

        if response.status_code != 200:
            print(f"Failed to retrieve the quiz report. Status code: {response.status_code}")
            return []

        soup = BeautifulSoup(response.text, "html.parser")
        attempt_elements = soup.find_all('a', attrs={'title': 'Revisar respuesta'})
        attempt_href_list = [element.get('href') for element in attempt_elements]
        return attempt_href_list

    def download_files_from_attempt(self, attempt_url, directory_path):
        response = self.session.get(attempt_url)

        if response.status_code != 200:
            print(f"Failed to retrieve attempt {attempt_url}. Status code: {response.status_code}")
            return

        soup = BeautifulSoup(response.text, "html.parser")
        attachments = soup.select("div.attachments a")

        for link in attachments:
            file_url = link["href"]
            file_name = link.get_text(strip=True)
            local_file_path = os.path.join(directory_path, file_name)
            
            with open(local_file_path, "wb") as file:
                file.write(self.session.get(file_url).content)

class SessionManager:
    def get_session(self, username, password):
        session = requests.session()
        login_url = "https://uv.frc.utn.edu.ar/login/index.php"
        login_data = {
            "username": username,
            "password": password,
        }
        session.post(login_url, data=login_data)
        return session

def main():
    print("¡Atención! antes de ejecutar el script ingrese al listado de evaluaciones desde la página de Moodle y configure el tamaño de página en 100")
    username = input("Ingrese su usuario de Moodle: ")
    password = input("Ingrese su contraseña de Moodle: ")
    print("Para obtener el id de la evaluacion debe ingresar al examen y en la url estará el id. Prr ejemplo https://uv.frc.utn.edu.ar/mod/quiz/view.php?id=123, el id es 123")
    quiz_id = input("Ingrese el ID de la evaluación: ")
    moodle_url = "https://uv.frc.utn.edu.ar"

    session_manager = SessionManager()
    session = session_manager.get_session(username, password)

    moodle = MoodleManager(moodle_url, session)
    attempt_urls = moodle.get_attempt_urls(quiz_id)

    directory_path = "./parciales"

    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        print(f"Directory '{directory_path}' created.")

    for attempt_url in attempt_urls:
        moodle.download_files_from_attempt(attempt_url, directory_path)

    print("Downloaded files for all attempts.")

if __name__ == "__main__":
    main()
