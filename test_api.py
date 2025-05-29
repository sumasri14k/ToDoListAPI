import requests

BASE_URL = "http://localhost:5000/tasks"

def test_api():
    # Test 1: Create a task
    print("Testing POST /tasks...")
    new_task = {"title": "Buy groceries", "description": "Milk, eggs, bread"}
    response = requests.post(BASE_URL, json=new_task)
    print(f"Create Task: {response.status_code} - {response.json()}")

    # Test 2: Get all tasks
    print("\nTesting GET /tasks...")
    response = requests.get(BASE_URL)
    print(f"Get All Tasks: {response.status_code} - {response.json()}")

    # Test 3: Get a specific task
    task_id = 1
    print(f"\nTesting GET /tasks/{task_id}...")
    response = requests.get(f"{BASE_URL}/{task_id}")
    print(f"Get Task {task_id}: {response.status_code} - {response.json()}")

    # Test 4: Update a task
    print(f"\nTesting PUT /tasks/{task_id}...")
    updated_task = {"title": "Buy groceries updated", "completed": True}
    response = requests.put(f"{BASE_URL}/{task_id}", json=updated_task)
    print(f"Update Task {task_id}: {response.status_code} - {response.json()}")

    # Test 5: Delete a task
    print(f"\nTesting DELETE /tasks/{task_id}...")
    response = requests.delete(f"{BASE_URL}/{task_id}")
    print(f"Delete Task {task_id}: {response.status_code} - {response.json()}")

    # Test 6: Try to get deleted task
    print(f"\nTesting GET /tasks/{task_id} (after delete)...")
    response = requests.get(f"{BASE_URL}/{task_id}")
    print(f"Get Deleted Task {task_id}: {response.status_code} - {response.json()}")

if __name__ == "__main__":
    test_api()