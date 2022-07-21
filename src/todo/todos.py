import json
import logging
from pathlib import Path
from typing import List

from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from todo.todo import Todo

logger = logging.getLogger("todo")


class Todos:
    def __init__(self, database: Path = Path("~/.todos.json")) -> None:
        db_data = []
        self.database = database.expanduser()
        if self.database.exists():
            logger.debug(f"Database exists: {self.database}")
            with open(self.database, "r") as stream:
                db_data = json.load(stream)
        logger.debug(f"Raw Database Data: {db_data}")
        self._todos: List[Todo] = []
        for entry in db_data:
            self._todos.append(Todo(entry["id"], entry["content"], entry["status"], entry["due"]))
        self.sort()
        logger.debug(f"Initialized {len(self._todos)} todos.")

    def render(self) -> None:
        table = Table(box=box.SIMPLE_HEAVY)
        table.add_column("ID", justify="left", style="")
        table.add_column("CONTENT", justify="left", style="")
        table.add_column("DUE", justify="center", style="")
        table.add_column("STATUS", justify="center", style="")

        for entry in self._todos:
            styles: list[str] = ["green"]
            content_style: str = "[b]"
            status: str = ":white_question_mark:"
            if entry.days_remaining < 1:
                styles.append("red")
            elif entry.days_remaining < 3:
                styles.append("dark_orange")
            if entry.status == "done":
                styles.append("default")
                content_style = "[s]"
                status = ":heavy_check_mark:"
                styles = []
            table.add_row(
                f"{entry._id}",
                f"{content_style}{entry.content}",
                f"{entry.days_remaining}d",
                f"{status}",
                style=" ".join(styles),
            )
        panel = Panel(
            table,
            border_style="bright_black",
            title=":alarm_clock:",
            expand=False,
            subtitle=":backhand_index_pointing_up:",
        )

        console = Console()
        console.print(panel)

    def _get_next_id(self) -> int:
        next_id = 1
        while True:
            found = True
            for todo in self._todos:
                if todo._id == next_id:
                    next_id += 1
                    found = False
                    break
            if found:
                return next_id

    def sort(self) -> None:
        self._todos.sort(key=lambda x: x.days_remaining)

    def add(self, content: str, due: str) -> None:
        self._todos.append(Todo(self._get_next_id(), content, "open", due))
        self.save()

    def done(self, _id: int) -> None:
        for todo in self._todos:
            if todo._id == str(_id):
                todo.status = "done"
                logger.info(f"Marked todo item with id {_id} as done.")
                self.save()
                return
        logger.error(f"Item with id {_id} does not exist. Current todos:")
        self.render()

    def save(self) -> None:
        db_data = []
        for todo in self._todos:
            entry: dict[str, str] = {}
            entry["id"] = str(todo._id)
            entry["content"] = todo.content
            entry["status"] = todo.status
            entry["due"] = todo.due
            db_data.append(entry)
        with open(self.database, "w") as stream:
            json.dump(db_data, stream, indent=4)

    def clean(self) -> None:
        open_todos = []
        for todo in self._todos:
            if todo.status == "open":
                open_todos.append(todo)
        logger.info(f"Removed {len(self._todos) - len(open_todos)} done items.")
        self._todos = open_todos
        self.save()
