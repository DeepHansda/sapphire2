import subprocess
import asyncio
import asyncio
import common.Folder_Paths as Folder_Paths
from common.startup import startUp
import threading
import time
import os


# def startUp_event():
#     result = startUp()
#     # print(result)
main_shared_file_path = os.path.join(Folder_Paths.cwd, "shared_values.json")
main_shared_file_path = os.path.abspath(os.path.expanduser(main_shared_file_path))
print(main_shared_file_path)
# if "\\" in  main_shared_file_path:
#     print(main_shared_file_path)
#     main_shared_file_path = os.path.abspath(os.path.expanduser(main_shared_file_path))
#     print(main_shared_file_path)
    
def startUp_event():
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:  # 'RuntimeError: There is no current event loop...'
        loop = None

    if loop and loop.is_running():
        task = asyncio.create_task(startUp())
        task.add_done_callback(
            lambda t: print(
                f"Task done with result={t.result()}  << return val of main()"
            )
        )

    else:
        print("Starting new event loop")
        result = asyncio.run(startUp())
        print(result)
    print(task.done())


def start_server():
    cmd = [
        "uvicorn",
        "main:app",
        "--reload",
        "--reload-exclude",
        "sapphire2/src/output",
        "--reload-include",
        "sapphire2/src/shared_values.json"
    ]
    cb = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    for line in cb.stdout:
        print(line.strip().decode("utf-8"))

    return_code = cb.wait()
    if return_code != 0:
        print(f"Exiting with return code {return_code}")
        exit(return_code)


if __name__ == "__main__":
    startUp_thread = threading.Thread(target=startUp_event)
    start_server_thread = threading.Thread(target=start_server)

    # Start both threads
    startUp_thread.start()
    start_server_thread.start()

    # Wait for both threads to finish
    startUp_thread.join()
    start_server_thread.join()
