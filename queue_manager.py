import queue
import threading
import time

task_queue = queue.Queue(maxsize=100)

active_tasks = {}

task_lock = threading.Lock()


def add_task(
    user_id,
    task_type,
    data=None
):
    if task_queue.full():
        raise Exception(
            "Queue is full"
        )

    task = {
        "user_id": user_id,
        "task_type": task_type,
        "data": data,
        "created": time.time()
    }

    task_queue.put(task)

    return task_queue.qsize()


def get_queue_size():
    return task_queue.qsize()


def is_processing(user_id):

    with task_lock:
        return user_id in active_tasks


def worker():

    while True:

        task = task_queue.get()

        try:

            user_id = task["user_id"]

            with task_lock:

                active_tasks[user_id] = task

            process_task(task)

        except Exception as e:

            print(
                f"[QUEUE ERROR] {e}"
            )

        finally:

            with task_lock:

                active_tasks.pop(
                    task["user_id"],
                    None
                )

            task_queue.task_done()


def process_task(task):

    task_type = task["task_type"]

    if task_type == "REMOVE_BG":
        time.sleep(2)

    elif task_type == "PDF_TO_IMAGE":
        time.sleep(2)

    elif task_type == "IMAGE_TO_PDF":
        time.sleep(2)

    else:
        time.sleep(1)


def start_workers(
    count=3
):
    for _ in range(count):

        thread = threading.Thread(
            target=worker,
            daemon=True
        )

        thread.start()


def get_status(user_id):

    with task_lock:

        if user_id in active_tasks:

            return {
                "status": "processing",
                "task":
                    active_tasks[user_id][
                        "task_type"
                    ]
            }

    return {
        "status": "waiting"
    }


def queue_info():

    with task_lock:

        return {
            "waiting":
                task_queue.qsize(),

            "active":
                len(active_tasks)
        }


start_workers(3)