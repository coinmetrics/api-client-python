import logging
import sys
from datetime import datetime
from multiprocessing import Pool
from os import environ, makedirs
from os.path import abspath, join

import requests

logger = logging.getLogger()
stream_handler = logging.StreamHandler()
level = logging.INFO
stream_handler.level = level
formatter = logging.Formatter(
    datefmt="[%Y-%m-%d %H:%M:%S]", fmt="%(asctime)-15s %(levelname)s %(message)s"
)
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)
logger.level = level


api_key = (
    environ.get("CM_API_KEY") or sys.argv[1]
)  # sys.argv[1] is executed only if CM_API_KEY is not found

DST_ROOT = "./data"

asset = "btc"


def export_data():
    logger.info("retrieving metric names")
    response = requests.get(
        "https://api.coinmetrics.io/v4/catalog/assets?assets=btc&api_key={}".format(
            api_key
        )
    )
    if response.status_code != 200:
        response.raise_for_status()
    catalog_response = response.json()["data"]
    metric_names = [
        metric_info["metric"]
        for metric_info in catalog_response[0]["metrics"]
        if any(
            frequency_info["frequency"] == "1b"
            for frequency_info in metric_info["frequencies"]
        )
    ]
    max_block = max(
        [
            max(
                int(frequency_info.get("max_height", 0))
                for frequency_info in metric_info["frequencies"]
            )
            for metric_info in catalog_response[0]["metrics"]
        ]
    )

    dst_file = join(DST_ROOT, "{}_bbb_metrics.csv".format(asset))
    makedirs(DST_ROOT, exist_ok=True)
    logger.info(
        "exporting metrics into a csv file (this might take awhile): %s",
        abspath(dst_file),
    )
    with open(dst_file, "w") as dst_file_buffer:
        with Pool(4) as pool:
            tasks = []
            page_size = 10000

            for start_height in range(0, max_block + 1, page_size):
                tasks.append(
                    pool.apply_async(
                        requests.get,
                        ("https://api.coinmetrics.io/v4/timeseries/asset-metrics",),
                        {
                            "params": {
                                "assets": asset,
                                "metrics": ",".join(metric_names),
                                "frequency": "1b",
                                "page_size": page_size,
                                "start_height": start_height,
                                "end_height": (start_height + page_size - 1),
                                "paging_from": "start",
                                "format": "csv",
                                "api_key": api_key,
                            }
                        },
                    )
                )

            for i, task in enumerate(tasks):
                res = task.get()
                if res.status_code != 200:
                    res.raise_for_status()
                else:
                    content = task.get().content.decode()
                    logger.info(
                        "saving_blocks: %s - %s",
                        i * page_size,
                        min(((i + 1) * page_size - 1), max_block),
                    )

                    dst_file_buffer.write(
                        content if i == 0 else content[content.find("\n") + 1 :]
                    )


if __name__ == "__main__":
    export_start_time = datetime.now()
    try:
        export_data()
    finally:
        logger.info("export took: %s", datetime.now() - export_start_time)
