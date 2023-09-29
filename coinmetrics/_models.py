from typing import Optional, List, Dict
from dataclasses import dataclass, field


@dataclass
class CoinMetricsAPIModel:

    @classmethod
    def get_dataframe_cols(cls) -> List[str]:
        return list(cls.__annotations__.keys())


@dataclass
class AssetChainsData(CoinMetricsAPIModel):
    """
    Class to represent data returned from asset chains data type
    """
    asset: str
    time: str
    chains_count: str
    blocks_count_at_tip: str
    reorg: Optional[str] = field(default="false")
    reorg_depth: str = field(default="0")
    chains: List[List[Dict[str, str]]] = field(default_factory=list)


@dataclass
class TransactionTrackerData(CoinMetricsAPIModel):
    """
    Class to represent data returned from tranasaction-tracker endpoint
    """
    txid: str
    time: str
    first_seen_time: str
    status: str
    status_update_time: str
    status_updates: List[str]
    details: str
    height: str = field(default="0")
    mempool_approx_queue_position: str = field(default="None")
    next_block_approx_settlement_probability_pct: str = field(default="0")
    block_hash: str = field(default="None")
    geo: str = field(default="None")
    replacement_for_txid: str = field(default="None")
    inputs: List[str] = field(default_factory=list)
    outputs: List[str] = field(default_factory=list)
