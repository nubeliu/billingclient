# NubeliU Billing SDK
# @autor: Sergio Colinas
import functools

from oslo_utils import strutils

from billingclient.common import utils
from billingclient import exc

_bool_strict = functools.partial(strutils.bool_from_string, strict=True)


@utils.arg('-m', '--gnocchi-metric',
           help='Associated gnocchi metric',
           required=True)
@utils.arg('-f', '--aggregation-function',
           help='Aggregation function to use for calculations',
           required=True)
@utils.arg('-gu', '--gnocchi-unit',
           help='Gnocchi Unit',
           required=True)
@utils.arg('-bu', '--billing-unit',
           help='Billing Unit',
           required=False)
def do_rating_metric_rule_set_create(cc, args={}):
    """Create a metric rule set."""
    arg_to_field_mapping = {
        'gnocchi_metric': 'gnocchi_metric',
        'aggregation_function': 'aggregation_function',
        'gnocchi_unit': 'gnocchi_unit',
        'billing_unit': 'billing_unit'
    }
    fields = {}
    for k, v in vars(args).items():
        if k in arg_to_field_mapping:
            if v is not None:
                fields[arg_to_field_mapping.get(k, k)] = v
    out = cc.gnocchi.metric_rule_sets.create(**fields)
    utils.print_dict(out.to_dict())


def do_rating_metric_rule_set_list(cc, args={}):
    """List metric rule sets."""
    try:
        metric_rule_sets = cc.gnocchi.metric_rule_sets.list()
    except exc.HTTPNotFound:
        raise exc.CommandError('Metric rule sets not found: %s' % args.counter_name)
    else:
        field_labels = ['Gnocchi Metric', 'Aggregation Function', 'Gnocchi Unit', 'Billing Unit', 'Id']
        fields = ['gnocchi_metric', 'aggregation_function', 'gnocchi_unit', 'billing_unit', 'id']
        utils.print_list(metric_rule_sets, fields, field_labels,
                         sortby=0)


@utils.arg('-s', '--id',
           help='Metric rule set uuid',
           required=True)
def do_rating_metric_rule_set_get(cc, args={}):
    """Get a metric rule set."""
    try:
        metric_rule_set = cc.gnocchi.metric_rule_sets.get(metric_rule_set_id=args.id)
        utils.print_dict(metric_rule_set.to_dict())
    except exc.HTTPNotFound:
        raise exc.CommandError('Metric rule set not found: %s' % args.counter_name)


@utils.arg('-s', '--id',
           help='Metric rule set uuid',
           required=True)
def do_rating_metric_rule_set_delete(cc, args={}):
    """Delete a metric rule set."""
    try:
        cc.gnocchi.metric_rule_sets.delete(metric_rule_set_id=args.id)
    except exc.HTTPNotFound:
        raise exc.CommandError('Metric rule set not found: %s' % args.counter_name)


@utils.arg('-n', '--name',
           help='Metadata rule set name',
           required=True)
@utils.arg('-s', '--metric-rule-set-id',
           help='Metric rule set id',
           required=True)
def do_rating_metadata_rule_set_create(cc, args={}):
    """Create a metadata rule set."""
    arg_to_field_mapping = {
        'name': 'name',
        'metric_rule_set_id': 'metric_rule_set_id'
    }
    fields = {}
    for k, v in vars(args).items():
        if k in arg_to_field_mapping:
            if v is not None:
                fields[arg_to_field_mapping.get(k, k)] = v
    out = cc.gnocchi.metadata_rule_sets.create(**fields)
    utils.print_dict(out.to_dict())


@utils.arg('-t', '--id',
           help='Metadata rule set uuid',
           required=True)
def do_rating_metadata_rule_set_get(cc, args={}):
    """Get a metadata rule set."""
    try:
        metadata_rule_set = cc.gnocchi.metadata_rule_sets.get(metadata_rule_set_id=args.id)
    except exc.HTTPNotFound:
        raise exc.CommandError('Metadata rule set not found: %s' % args.id)
    utils.print_dict(metadata_rule_set.to_dict())


@utils.arg('-rs', '--metric-rule-set-id',
           help='Metric rule set id',
           required=True)
def do_rating_metadata_rule_set_list(cc, args={}):
    """List metadata rule sets."""
    try:
        created_metadata_rule_set = cc.gnocchi.metadata_rule_sets.list(metric_rule_set_id=args.metric_rule_set_id)
    except exc.HTTPNotFound:
        raise exc.CommandError('Metadata rule sets not found: %s' % args.counter_name)
    else:
        field_labels = ['Id', 'Name', 'Metadata rule set id']
        fields = ['id', 'name', 'metric_rule_set_id']
        utils.print_list(created_metadata_rule_set, fields, field_labels,
                         sortby=0)


@utils.arg('-m', '--id',
           help='Metadata rule set uuid',
           required=True)
def do_rating_metadata_rule_set_delete(cc, args={}):
    """Delete a metadata rule set."""
    try:
        cc.gnocchi.metadata_rule_sets.delete(id=args.id)
    except exc.HTTPNotFound:
        raise exc.CommandError('Metadata rule set not found: %s' % args.counter_name)


@utils.arg('-c', '--cost',
           help='Metric rule cost',
           required=True)
@utils.arg('-t', '--type',
           help='Metric rule type (flat, rate)',
           required=False)
@utils.arg('-s', '--metric-rule-set-id',
           help='Metric rule set id',
           required=False)
@utils.arg('-vs', '--valid-since',
           help='Metric rule valid since',
           required=False)
@utils.arg('-vu', '--valid-until',
           help='Metric rule valid until',
           required=False)
@utils.arg('-p', '--providers',
           help='Metric rule providers (openstack or vmware)',
           required=False)
def do_rating_metric_rule_create(cc, args={}):
    """Create a metric rule."""
    arg_to_field_mapping = {
        'cost': 'cost',
        'type': 'type',
        'metric_rule_set_id': 'metric_rule_set_id',
        'valid_since': 'valid_since',
        'valid_until': 'valid_until',
        'providers': 'providers',
    }
    fields = {}
    for k, v in vars(args).items():
        if k in arg_to_field_mapping:
            if v is not None:
                fields[arg_to_field_mapping.get(k, k)] = v
    out = cc.gnocchi.metric_rules.create(**fields)
    utils.print_dict(out.to_dict())


@utils.arg('-c', '--cost',
           help='Metadata rule cost',
           required=True)
@utils.arg('-v', '--value',
           help='Metadata rule value',
           required=False)
@utils.arg('-d', '--display-value',
           help='Metadata rule display name',
           required=False)
@utils.arg('-t', '--type',
           help='Metadata rule type (flat, rate)',
           required=False)
@utils.arg('-s', '--metadata-rule-set-id',
           help='Metadata rule set id',
           required=False)
@utils.arg('-vs', '--valid-since',
           help='Metadata rule valid since',
           required=False)
@utils.arg('-vu', '--valid-until',
           help='Metadata rule valid until',
           required=False)
@utils.arg('-p', '--providers',
           help='Metadata rule providers (openstack or vmware)',
           required=False)
def do_rating_metadata_rule_create(cc, args={}):
    """Create a metadata rule."""
    arg_to_field_mapping = {
        'cost': 'cost',
        'value': 'value',
        'display_value': 'display_value',
        'type': 'type',
        'metadata_rule_id': 'metadata_rule_id',
        'valid_since': 'valid_since',
        'valid_until': 'valid_until',
        'providers': 'providers',
    }
    fields = {}
    for k, v in vars(args).items():
        if k in arg_to_field_mapping:
            if v is not None:
                fields[arg_to_field_mapping.get(k, k)] = v
    out = cc.gnocchi.metadata_rules.create(**fields)
    utils.print_dict(out.to_dict())


@utils.arg('-m', '--id',
           help='Metric rule id',
           required=True)
@utils.arg('-c', '--cost',
           help='Metric rule cost',
           required=False)
@utils.arg('-t', '--type',
           help='Metric rule type (flat, rate)',
           required=False)
@utils.arg('-s', '--valid-since',
           help='Metric rule valid since',
           required=False)
@utils.arg('-u', '--valid-until',
           help='Metric rule valid until',
           required=False)
@utils.arg('-p', '--providers',
           help='Metric rule providers (openstack or vmware)',
           required=False)
def do_rating_metric_rule_update(cc, args={}):
    """Update a metric rule."""
    arg_to_field_mapping = {
        'id': 'id',
        'cost': 'cost',
        'type': 'type',
        'valid_since': 'valid_since',
        'valid_until': 'valid_until',
        'providers': 'providers',
    }
    try:
        metric_rule = cc.gnocchi.metric_rules.get(id=args.id)
    except exc.HTTPNotFound:
        raise exc.CommandError('Metric rule not found: %s' % args.counter_name)
    for k, v in vars(args).items():
        if k in arg_to_field_mapping:
            if v is not None:
                if k == 'valid_since':
                    setattr(metric_rule, k, None)
                else:
                    setattr(metric_rule, k, v)
    cc.gnocchi.metric_rules.update(**metric_rule.dirty_fields)


@utils.arg('-m', '--id',
           help='Metadata rule id',
           required=True)
@utils.arg('-c', '--cost',
           help='Metadata rule cost',
           required=False)
@utils.arg('-v', '--value',
           help='Metadata rule value',
           required=False)
@utils.arg('-d', '--display-value',
           help='Metadata rule display value',
           required=False)
@utils.arg('-t', '--type',
           help='Metadata rule type (flat, rate)',
           required=False)
@utils.arg('-s', '--valid-since',
           help='Metadata rule valid since',
           required=False)
@utils.arg('-u', '--valid-until',
           help='Metadata rule valid until',
           required=False)
@utils.arg('-p', '--providers',
           help='Metadata rule providers',
           required=False)
def do_rating_mapping_update(cc, args={}):
    """Update a metadata rule."""
    arg_to_field_mapping = {
        'id': 'id',
        'cost': 'cost',
        'value': 'value',
        'display_value': 'display_value',
        'type': 'type',
        'valid_since': 'valid_since',
        'valid_until': 'valid_until',
        'providers': 'providers',
    }
    try:
        metadata_rule = cc.gnocchi.metadata_rules.get(id=args.id)
    except exc.HTTPNotFound:
        raise exc.CommandError('Metadata rule not found: %s' % args.counter_name)
    for k, v in vars(args).items():
        if k in arg_to_field_mapping:
            if v is not None:
                if k == 'valid_since':
                    setattr(metadata_rule, k, None)
                else:
                    setattr(metadata_rule, k, v)
    cc.gnocchi.metadata_rules.update(**metadata_rule.dirty_fields)


@utils.arg('-s', '--metric-rule-set-id',
           help='Metric rule set id',
           required=False)
def do_rating_metric_rule_list(cc, args={}):
    """List metric rules."""
    if args.metric_rule_set_id is None:
        raise exc.CommandError("Provide metric-rule-set-id")
    try:
        metric_rules = cc.gnocchi.metric_rules.list(metric_rule_set_id=args.metric_rule_set_id)
    except exc.HTTPNotFound:
        raise exc.CommandError('Metric rule not found: %s' % args.counter_name)
    else:
        field_labels = ['Id', 'Cost', 'Type', 'Metric rule set id',
                        'Valid Since', 'Valid Until', 'Providers']
        fields = ['id', 'cost', 'type', 'metric_rule_set_id',
                  'valid_since', 'valid_until', 'providers']
        utils.print_list(metric_rules, fields, field_labels,
                         sortby=0)


@utils.arg('-f', '--metadata-rule-set-id',
           help='Metadata rule set id',
           required=False)
def do_rating_metadata_rule_list(cc, args={}):
    """List metadata rules."""
    if args.metadata_rule_set_id is None:
        raise exc.CommandError("Provide metadata-rule-set-id")
    try:
        metadata_rules = cc.gnocchi.metadata_rules.list(metadata_rule_set_id=args.metadata_rule_set_id)
    except exc.HTTPNotFound:
        raise exc.CommandError('Metadata rule not found: %s' % args.counter_name)
    else:
        field_labels = ['Id', 'Value', 'Display name',
                        'Cost', 'Type', 'Metadata rule set id',
                        'Valid Since', 'Valid Until', 'Providers']
        fields = ['id', 'value', 'display_value',
                  'cost', 'type', 'metadata_rule_set_id',
                  'valid_since', 'valid_until', 'providers']
        utils.print_list(metadata_rules, fields, field_labels,
                         sortby=0)


@utils.arg('-m', '--id',
           help='Metric rule uuid',
           required=True)
def do_rating_metric_rule_get(cc, args={}):
    """Get a metric rule."""
    try:
        cc.gnocchi.metric_rules.get(metric_rule_id=args.id)
    except exc.HTTPNotFound:
        raise exc.CommandError('Metric rule not found: %s' % args.id)


@utils.arg('-m', '--id',
           help='Metadata rule uuid',
           required=True)
def do_rating_metadata_rule_get(cc, args={}):
    """Get a metadata rule."""
    try:
        cc.gnocchi.metadata_rules.get(metadata_rule_id=args.id)
    except exc.HTTPNotFound:
        raise exc.CommandError('Metadata rule not found: %s' % args.id)


@utils.arg('-m', '--id',
           help='Metric rule uuid',
           required=True)
def do_rating_metric_rule_delete(cc, args={}):
    """Delete a metric rule."""
    try:
        cc.gnocchi.metric_rules.delete(id=args.id)
    except exc.HTTPNotFound:
        raise exc.CommandError('Metric rule not found: %s' % args.id)


@utils.arg('-m', '--id',
           help='Metadata rule uuid',
           required=True)
def do_rating_metadata_rule_delete(cc, args={}):
    """Delete a metadata rule."""
    try:
        cc.gnocchi.metadata_rules.delete(id=args.id)
    except exc.HTTPNotFound:
        raise exc.CommandError('Metadata rule not found: %s' % args.id)


@utils.arg('-l', '--level',
           help='Threshold level',
           required=True)
@utils.arg('-c', '--cost',
           help='Threshold cost',
           required=True)
@utils.arg('-m', '--map-type',
           help='Threshold type (flat, rate)',
           required=False)
@utils.arg('-s', '--metric-rule-set-id',
           help='Metric rule set id',
           required=False)
@utils.arg('-vs', '--valid-since',
           help='Valid Since',
           required=False)
@utils.arg('-vu', '--valid-until',
           help='Valid Until',
           required=False)
@utils.arg('-p', '--providers',
           help='Providers',
           required=False)
def do_rating_threshold_rule_create(cc, args={}):
    """Create a threshold rule."""
    arg_to_field_mapping = {
        'level': 'level',
        'cost': 'cost',
        'type': 'type',
        'metric_rule_set_id': 'metric_rule_set_id',
        'valid_since': 'valid_since',
        'valid_until': 'valid_until',
        'providers': 'providers',
    }
    fields = {}
    for k, v in vars(args).items():
        if k in arg_to_field_mapping:
            if v is not None:
                fields[arg_to_field_mapping.get(k, k)] = v
    out = cc.gnocchi.threshold_rules.create(**fields)
    utils.print_dict(out.to_dict())


@utils.arg('-t', '--id',
           help='Threshold id',
           required=True)
@utils.arg('-l', '--level',
           help='Threshold level',
           required=False)
@utils.arg('-c', '--cost',
           help='Threshold cost',
           required=False)
@utils.arg('-m', '--type',
           help='Threshold type (flat or rate)',
           required=False)
@utils.arg('-vs', '--valid-since',
           help='Valid Since',
           required=False)
@utils.arg('-vu', '--valid-until',
           help='Valid Until',
           required=False)
@utils.arg('-p', '--providers',
           help='Providers',
           required=False)
def do_rating_threshold_rule_update(cc, args={}):
    """Update a threshold rule."""
    arg_to_field_mapping = {
        'id': 'id',
        'cost': 'cost',
        'level': 'level',
        'type': 'type',
        'valid_since': 'valid_since',
        'valid_until': 'valid_until',
        'providers': 'providers',
    }
    try:
        threshold_rule = cc.gnocchi.threshold_rules.get(id=args.id)
    except exc.HTTPNotFound:
        raise exc.CommandError('Modules not found: %s' % args.counter_name)
    for k, v in vars(args).items():
        if k in arg_to_field_mapping:
            if v is not None:
                setattr(threshold_rule, k, v)
    cc.gnocchi.threshold_rules.update(**threshold_rule.dirty_fields)


@utils.arg('-rs', '--metric-rule-set-id',
           help='Metric rule set id',
           required=False)
def do_rating_threshold_rule_list(cc, args={}):
    """List threshold rules."""
    if args.metric_rule_set_id is None:
        raise exc.CommandError("Provide metric-rule-set-id")
    try:
        threshold_rules = cc.gnocchi.threshold_rules.list(metric_rule_set_id=args.metric_rule_set_id)
    except exc.HTTPNotFound:
        raise exc.CommandError('Threshold rule not found: %s' % args.counter_name)
    else:
        field_labels = ['Id', 'Level', 'Cost', 'Type',
                        'Metric rule set id', 'Valid Since',
                        'Valid Until', 'Providers']
        fields = ['id', 'level', 'cost', 'type', 'metric_rule_set_id',
                  'valid_since', 'valid_until', 'providers']
        utils.print_list(threshold_rules, fields, field_labels, sortby=0)


@utils.arg('-t', '--id',
           help='Threshold rule uuid',
           required=True)
def do_rating_threshold_rule_delete(cc, args={}):
    """Delete a threshold rule."""
    try:
        cc.gnocchi.threshold_rules.delete(id=args.id)
    except exc.HTTPNotFound:
        raise exc.CommandError('Threshold rule not found: %s' % args.id)


@utils.arg('-t', '--id',
           help='Threshold rule uuid',
           required=True)
def do_rating_threshold_rule_get(cc, args={}):
    """Get a threshold rule."""
    try:
        threshold_rule = cc.gnocchi.threshold_rules.get(threshold_rule_id=args.id)
    except exc.HTTPNotFound:
        raise exc.CommandError('Threshold rule not found: %s' % args.id)
    utils.print_dict(threshold_rule.to_dict())
