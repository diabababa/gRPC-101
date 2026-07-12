import os
import shutil

order = (
    "01_protocol_buffers",
    "02_service_stub",
    "03_unary_service",
    "04_unary_client",
    "05_streaming",
    "06_deadlines_cancellation_errors",
    "07_final_chat_client"
)

solutions_order = (
    "chat.proto",
    "server.py",
    "server.py",
    "client.py",
    "streaming.py",
    "deadlines_demo.py",
    "client.py"
)

workshop_directory = "/".join(os.getcwd().split("/")[:-1])+"/workshop"
exercises_directory = os.path.join(workshop_directory, "exercises")
solutions_directory = os.path.join(workshop_directory, "solutions")
new_line = "\n"
if os.path.exists(f"{exercises_directory}/README.md"):
    os.remove(f"{exercises_directory}/README.md")
for index, exercise_chapter in enumerate(order):
    temp_text = ""
    with open(
        os.path.join(f"{exercises_directory}/{exercise_chapter}", "README.md")
    ) as f:
        temp_text = f.read()
    with open(f"{exercises_directory}/README.md", "a") as f:
        f.write(f"{new_line * 2 if index > 0 else ''}{temp_text}")
    solution_path = os.path.join(f"{exercises_directory}", solutions_order[index]) if index == 6 else os.path.join(f"{solutions_directory}/{exercise_chapter}", solutions_order[index])
    with open(solution_path) as f:
        temp_text = f.read()
    with open(f"{exercises_directory}/README.md", "a") as f:
        f.write(f"{new_line * 2}<details>{new_line * 2}<summary>Click to view Solution {index + 1}</summary>{new_line * 2}{temp_text}{new_line * 2}</details>")