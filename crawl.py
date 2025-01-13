import typer
from typing import Optional
from _crawling_functions import new_crawlers, _checker_funcs


app = typer.Typer()

def validate_url(url: str) -> str:
    """Validate and clean the URL."""
    if url.endswith('/'):
        return url[:-1]
    return url

@app.command()
def crawl(
    url: str = typer.Argument(..., help="Site directory to crawl"),
    checker_function: Optional[str] = typer.Option(
        None,
        "--checker", "-c",
        help="Name of the checker function from _checker_funcs to use"
    ),
    dynamic_content: Optional[bool] = typer.Option(
        False,
        "--dynamic", "-d",
        help="Enable dynamic content crawling"
    )
):
    """
    Crawl a website with optional content checking functionality.

    If a checker function is provided, it will use the CheckerCrawler,
    otherwise it will use the ClassicCrawler.
    """
    site_url = validate_url(url)

    if checker_function:
        try:
            check_func = getattr(_checker_funcs, checker_function)
            crawler = new_crawlers.CheckerCrawler(site_url, check_func)
        except AttributeError:
            available_funcs = [f for f in dir(_checker_funcs)
                             if not f.startswith('_')]
            typer.echo(f"Error: Invalid checker function. Available functions: {available_funcs}")
            raise typer.Exit(1)
    else:
        crawler = new_crawlers.ClassicCrawler(site_url)

    try:
        crawler.start_crawling(dynamic_pages=dynamic_content)
    except Exception as e:
        typer.echo(f"Error during crawling: {str(e)}")
        raise typer.Exit(1)


def main():
    app()


if __name__ == "__main__":
    main()
