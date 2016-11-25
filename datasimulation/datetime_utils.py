import scipy.stats as stats
from datetime import timedelta


def time_spread(moment, std, lower_limit=None, upper_limit=None):
    """Add spread to a moment in hours

    Give both the lower_limit and upper_limit or neither. If limits are given, truncated normal distribution is used.

    Args:
        moment: datetime object
        std: Standard deviation in hours
        lower_limit: Lower limit for deviation
        upper_limit: Upper limit for deviation

    Returns:
        Time shifted datetime object
    """
    if lower_limit is not None and upper_limit is not None:
        # Limits given, use truncated normal distribution
        hours = stats.truncnorm(lower_limit/std, upper_limit/std, loc=0, scale=std).rvs(1)[0]
    else:
        # Limits not given, use normal distribution
        hours = stats.norm(loc=0, scale=std).rvs(1)[0]
    td = timedelta(hours=hours)
    return moment + td
