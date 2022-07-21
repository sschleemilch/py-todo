from datetime import date, datetime

DATEFORMAT = "%d.%m.%Y"


class Todo:
    def __init__(self, _id: int, content: str, status: str, due: str) -> None:
        self._id = _id
        self.content = content
        self.status = status
        self.due = due
        self.days_remaining = (
            datetime.strptime(due, DATEFORMAT).date() - date.today()
        ).days
