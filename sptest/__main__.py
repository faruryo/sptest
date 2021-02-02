import statistics
from typing import List

import pandas as pd
import speedtest
import typer

from sptest import config, repository

app = typer.Typer()


def get_speedtest_servers(servers: List[int]) -> dict:
    limit = None
    if not servers:
        servers = None
    else:
        limit = len(servers)

    sp = speedtest.Speedtest()
    sp.get_servers(servers=servers)
    servers = sp.get_closest_servers(limit=limit)

    return servers


@app.command()
def test(
    conf: str = typer.Argument(..., help="File path of the configuration file"),
    verbose: bool = typer.Option(
        False, "--verbose", "-v", help="Take the operation more talkative"
    )
):

    c = config.load_config(conf)
    speedtest.DEBUG = verbose

    print("Prepare in...")
    servers = get_speedtest_servers(c["speedtest"]["servers"])
    repo = repository.AmbientRepository(c["ambient"]["dataLink"])

    pd.set_option("display.max_columns", 100)
    pd.set_option("display.max_rows", len(servers))
    pd.set_option("display.width", 300)

    print(pd.DataFrame(servers))

    for server in servers:
        try:
            print(f"Testing... {server['host']}", flush=True)
            sp = speedtest.Speedtest()
            sp.get_best_server([server])

            sp.download(threads=c["speedtest"]["threads"])
            print(f"Download :{sp.results.download/1000000.0:0.2f} Mbps", flush=True)
            repo.createDownload(sp.results.dict())

            sp.upload(threads=c["speedtest"]["threads"])
            print(f"Upload   :{sp.results.upload/1000000.0:0.2f} Mbps", flush=True)
            repo.createUpload(sp.results.dict())

        except Exception as e:
            print(e)


@app.command()
def servers(
    conf: str = typer.Option("", help="File path of the configuration file"),
    server_limit: int = typer.Option(5, help="Number of servers to check"),
    ping_num: int = typer.Option(5, help="Number of times to ping test"),
    sort_key: str = typer.Option("latency_median", help="A key to sort the server"),
    verbose: bool = typer.Option(
        False, "--verbose", "-v", help="Take the operation more talkative"
    ),
):

    c = config.load_config(conf)
    speedtest.DEBUG = verbose

    sp = speedtest.Speedtest()
    sp.get_servers(servers=c["speedtest"]["servers"])
    servers = sp.get_closest_servers(limit=server_limit)
    for server in servers:
        print(f"check {server['host']} ", end="", flush=True)
        latencies = []
        for i in range(ping_num):
            sp.get_best_server([server])
            latencies.append(server["latency"])

        server["latency_median"] = float(statistics.median(latencies))
        server["latency_mean"] = float(statistics.mean(latencies))
        print(
            f"median:{server['latency_median']}, mean:{server['latency_mean']}",
            flush=True,
        )

    print()

    pd.set_option("display.max_columns", 100)
    pd.set_option("display.max_rows", server_limit)
    pd.set_option("display.width", 300)

    servers_df = pd.DataFrame(servers)
    sorted_servers_df = servers_df.sort_values(by=sort_key)
    print(f"Server list sorted by {sort_key}")
    print(sorted_servers_df)


if __name__ == "__main__":
    app()
