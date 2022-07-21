import logging
from datetime import date, timedelta

import rich_click as click
from click import Context
from rich.logging import RichHandler
from rich.traceback import install

from todo import __version__
from todo.todo import DATEFORMAT
from todo.todos import Todos

install(show_locals=True)

FORMAT = "%(message)s"
logging.basicConfig(level="INFO", format=FORMAT, datefmt="[%X]", handlers=[RichHandler(rich_tracebacks=True)])

log = logging.getLogger("todo")


@click.option("--debug", is_flag=True, help="Enables debug outputs.")
@click.option("--version", "-V", is_flag=True, help="Print version and exit.")
@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx: Context, version: bool = False, debug: bool = False) -> None:
    if debug:
        log.setLevel(logging.DEBUG)
    if version:
        print(__version__)
        return
    if ctx.invoked_subcommand is None:
        ctx.invoke(show)


@cli.command()
def show() -> None:
    """Shows all current things to do"""
    Todos().render()


def get_due_date(due: int) -> str:
    today = date.today()
    end_date = today + timedelta(due)
    return end_date.strftime(DATEFORMAT)


@cli.command()
@click.argument("content")
@click.argument("due", type=int, default=7)
def add(content: str, due: int) -> None:
    """Adding new things to do"""
    Todos().add(content, get_due_date(due))


@cli.command()
@click.argument("_id", type=int)
def done(_id: int) -> None:
    """Marking things as done"""
    Todos().done(_id)


@cli.command()
def clean() -> None:
    """Removes done tasks"""
    Todos().clean()


@cli.command()
def edit() -> None:
    """Edit an existing todo"""
    pass
