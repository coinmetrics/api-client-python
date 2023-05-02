import datetime
import itertools
import os
from coinmetrics.api_client import CoinMetricsClient
from requests.exceptions import HTTPError
from typing import Union, List, Any, Iterator, Optional

client = CoinMetricsClient(os.environ.get("CM_API_KEY"))


def chunk(it: Any, size: int) -> Iterator:
    """
    Simple utility function to split an iterable into smaller chunks
    """

    it = iter(it)
    return iter(lambda: tuple(itertools.islice(it, size)), ())


def get_atlas_balance_updates(asset: str,
                              start_time: Optional[Union[datetime.datetime, str]] = None,
                              end_time: Optional[Union[datetime.datetime, str]] = None,
                              list_of_accounts: List[str] = [],
                              balance_updates_file_name: str = "balance_updates.csv",
                              ) -> None:
    """
    Get atlas balance updates from a list of accounts and save the results in a file.

    :param asset: The asset for which balance updates are to be fetched.
    :type asset: str
    :param start_time: The start time for the balance updates.
    :type start_time: Union[datetime.datetime, str]
    :param end_time: The end time for the balance updates.
    :type end_time: Union[datetime.datetime, str]
    :param csv_account_column: The column in the CSV file that contains the account information. Defaults to "assets".
    :type csv_account_column: str, optional
    :param balance_updates_file_name: The name of the file where the balance updates will be saved. Defaults to "balance_updates.csv".
    :type balance_updates_file_name: str, optional
    :return: str name of the file created
    """
    balance_updates_file_extension = balance_updates_file_name.split('.')[-1]
    balance_updates_file_base = balance_updates_file_name[:-(len(balance_updates_file_extension) + 1)]
    print(f"Asset: {asset}")
    accounts_all = list_of_accounts
    print(f"Found {len(accounts_all)} accounts...")

    # can edit the account chunks to be larger, max is about 300
    chunk_size = 100
    account_chunks = chunk([a for a in accounts_all], chunk_size)

    for i, accounts in enumerate(account_chunks):
        print(f"Processing chunk {i}; {i*chunk_size}/{len(accounts_all)} accounts...")

        try:
            balance_updates_chunk_file_name = f"{balance_updates_file_base}_{i}.{balance_updates_file_extension}"

            if balance_updates_file_extension == 'csv':
                balance_file = client.get_list_of_balance_updates_v2(
                    asset=asset, accounts=accounts, start_time=start_time, end_time=end_time, page_size=1000
                ).export_to_csv(balance_updates_chunk_file_name)
            elif balance_updates_file_extension == 'json':
                balance_file = client.get_list_of_balance_updates_v2(
                    asset=asset, accounts=accounts, page_size=1000
                ).export_to_json(balance_updates_chunk_file_name)

            print(f"File saved in {balance_updates_chunk_file_name}")

        except (ValueError, HTTPError):
            print("Chunking failed. Trying smaller chunk size.")
            subchunk_size = 10

            account_subchunks = chunk([a for a in account_chunks], subchunk_size)
            for j, accounts in account_subchunks:
                print(f"Processing chunk {i}-{j}; {i * chunk_size + j}/{len(accounts_all)} accounts...")
                balance_updates_chunk_file_name = f"{balance_updates_file_base}_{i}_{j}.{balance_updates_file_extension}"
                if balance_updates_file_extension == 'csv':
                    balance_file = client.get_list_of_balance_updates_v2(
                        asset=asset, accounts=accounts, start_time=start_time, end_time=end_time, page_size=1000
                    ).export_to_csv(balance_updates_chunk_file_name)
                elif balance_updates_file_extension == 'json':
                    balance_file = client.get_list_of_balance_updates_v2(
                        asset=asset, accounts=accounts, page_size=1000
                    ).export_to_json(balance_updates_chunk_file_name)

                print(f"File saved in {balance_updates_chunk_file_name}")

    print("Done.")
    return balance_updates_chunk_file_name


if __name__ == "__main__":
    """
    This script shows how to export balance updates using ATLAS v2 given a list of accounts. 
    By defualt it will just read a few accounts from the `accounts.txt` file but there is a commented out example showing 
    how to get balance updates from the .list_of_accounts_v2() method as well. By defualt these values will be appended
    to a file called `balance_updates_0.csv`
    """

    # list_accounts = [account_data['account'] for account_data in client.get_list_of_accounts_v2(asset="btc", paging_from="start", page_size=100).first_page()][50:]
    list_accounts = open("accounts.txt").read().split(",")
    asset = "btc"
    get_atlas_balance_updates(asset=asset, list_of_accounts=list_accounts)
