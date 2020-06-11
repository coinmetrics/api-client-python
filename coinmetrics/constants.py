from enum import Enum


class ApiBranch(Enum):
    PRODUCTION = 1
    STAGING = 2


class PagingFrom(Enum):
    START = 'start'
    END = 'end'


API_BASE = {
    ApiBranch.PRODUCTION: 'https://api.coinmetrics.io',
    ApiBranch.STAGING: 'https://staging-api.coinmetrics.io'
}
