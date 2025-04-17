from locust import HttpUser, task, between
import random
import uuid

class ManagerAPI(HttpUser):
    wait_time = between(1, 5)  # Время ожидания между запросами (в секундах)

    # Список UUID существующих менеджеров (будет заполняться динамически)
    existing_manager_ids = []

    @task(3)
    def get_all_managers(self):
        """Получение списка всех менеджеров."""
        self.client.get("/")

    @task(2)
    def get_manager(self):
        """Получение данных конкретного менеджера по UUID."""
        if self.existing_manager_ids:
            manager_id = random.choice(self.existing_manager_ids)
            self.client.get(f"/{manager_id}", name="/[manager_id]")
        else:
            print("No managers available to fetch.")

    @task(1)
    def create_manager(self):
        """Создание нового менеджера."""
        new_manager = {
            "name": f"Test Manager {random.randint(1, 1000)}",
            "contracts_count": random.randint(0, 50)
        }
        response = self.client.post("/", json=new_manager)
        if response.status_code == 201:
            manager_id = response.json().get("id")
            if manager_id:
                self.existing_manager_ids.append(manager_id)

    @task(1)
    def update_manager(self):
        """Обновление данных существующего менеджера."""
        if self.existing_manager_ids:
            manager_id = random.choice(self.existing_manager_ids)
            updated_data = {
                "contracts_count": random.randint(0, 50)
            }
            self.client.put(f"/{manager_id}", json=updated_data, name="/[manager_id]")

    @task(1)
    def delete_manager(self):
        """Удаление менеджера."""
        if self.existing_manager_ids:
            manager_id = random.choice(self.existing_manager_ids)
            response = self.client.delete(f"/{manager_id}", name="/[manager_id]")
            if response.status_code == 200:
                self.existing_manager_ids.remove(manager_id)

    @task(2)
    def generate_report(self):
        """Генерация отчета."""
        self.client.get("/reports/report", name="/reports/report")
