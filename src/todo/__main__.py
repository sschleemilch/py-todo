import logging
import rich_click as click
from rich.logging import RichHandler
from rich.traceback import install
from datetime import date, timedelta

from todo import __version__
from todo.todos import Todos
from todo.todo import DATEFORMAT

install(show_locals=True)

FORMAT = "%(message)s"
logging.basicConfig(level="INFO", format=FORMAT, datefmt="[%X]", handlers=[RichHandler(rich_tracebacks=True)])

log = logging.getLogger("todo")


@click.option("--debug", is_flag=True, help="Enables debug outputs.")
@click.option("--version", "-V", is_flag=True, help="Print version and exit.")
@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx, version: bool = False, debug: bool = False) -> None:
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


def get_due_date(due: int):
    today = date.today()
    end_date = today + timedelta(due)
    end_date = end_date.strftime(DATEFORMAT)
    return end_date


@cli.command()
@click.argument("content")
@click.argument("due", type=int, default=7)
def add(content, due):
    """Adding new things to do"""
    Todos().add(content, get_due_date(due))


@cli.command()
@click.argument("_id", type=int)
def done(_id: int):
    """Marking things as done"""
    Todos().done(_id)


@cli.command()
def clean():
    """Removes done tasks"""
    Todos().clean()


@cli.command()
def edit():
    """Edit an existing todo"""
    pass
