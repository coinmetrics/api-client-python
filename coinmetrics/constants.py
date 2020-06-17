from enum import Enum


class ApiBranch(Enum):
    PRODUCTION = 1
    STAGING = 2
    COMMUNITY = 3
    STAGING_COMMUNITY = 4


class PagingFrom(Enum):
    START = 'start'
    END = 'end'


API_BASE = {
    ApiBranch.PRODUCTION: 'https://api.coinmetrics.io',
    ApiBranch.STAGING: 'https://staging-api.coinmetrics.io',
    ApiBranch.COMMUNITY: 'https://community-api.coinmetrics.io',
    ApiBranch.STAGING_COMMUNITY: 'https://staging-community-api.coinmetrics.io',
}
COMMUNITY_API_BRANCHES = {ApiBranch.STAGING, ApiBranch.STAGING_COMMUNITY}
