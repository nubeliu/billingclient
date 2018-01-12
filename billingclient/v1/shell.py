# NubeliU Billing SDK
# @autor: Sergio Colinas

from billingclient.common import utils
from billingclient import exc


def do_rating_is_enabled(cc, args):
    """Return True if rating is enabled."""
    is_enabled = cc.modules.is_enabled()
    print is_enabled


@utils.arg('-e', '--enabled',
           help='Rating set status enabled (true/false)',
           required=True)
def do_rating_set_status(cc, args):
    """Set rating status enabled (true/false)."""
    cc.modules.set_status(enabled=args.enabled)


def do_rating_get_last_processed_timestamp(cc, args):
    """Return the last processed timestamp."""
    last_processed_timestamp = cc.modules.get_last_processed_timestamp()
    print last_processed_timestamp


@utils.arg('-t', '--timestamp',
           help='Recalculate costs from timestamp',
           required=True)
def do_rating_recalculate_since(cc, args):
    """Recalculates costs from timestamp."""
    timestamp = cc.modules.recalculate_since(
        args.timestamp)
    print "Recalculating costs since: " + timestamp
