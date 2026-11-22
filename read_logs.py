with open("django.log", "r", encoding="utf-8") as file:
    logs = file.read()

print(logs)