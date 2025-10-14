from locust import HttpUser, TaskSet, task, between
from core.environment.host import get_host_for_locust_testing


class NotepadBehavior(TaskSet):
    def on_start(self):
        self.index()

    @task
    def index(self):
        response = self.client.get("/notepad")

        if response.status_code != 200:
            print(f"Notepad index failed: {response.status_code}")


class NotepadUser(HttpUser):
    tasks = [NotepadBehavior]
    min_wait = 5000
    max_wait = 9000
    host = get_host_for_locust_testing()


class WebsiteTestUser(HttpUser):
    wait_time = between(1, 5)

    @task(2)
    def load_tasks(self):
        print("Cargando la lista de tareas...")
        response = self.client.get("/notepad")
        if response.status_code == 200:
            print("Lista de tareas cargada correctamente.")
        else:
            print(f"Error al cargar la lista de tareas: {response.status_code}")

    @task(1)
    def create_task(self):
        print("Creando una nueva tarea...")
        response = self.client.post("/notepad/create", data={"title": "Tarea generada por Locust", "body": "Texto generado por Locust"})
        if response.status_code == 201:
            print("Tarea creada correctamente.")
        else:
            print(f"Error al crear la tarea: {response.status_code}")