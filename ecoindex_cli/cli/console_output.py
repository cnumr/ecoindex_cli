from rich.console import Console
from rich.table import Table


def display_result_synthesis(total: int, success: int) -> None:
    console = Console()

    table = Table(show_header=True)
    table.add_column("Total analysis")
    table.add_column("Success", header_style="green")
    table.add_column("Failed", header_style="red")
    table.add_row(str(total), str(success), str(total - success))

    console.print(table)
