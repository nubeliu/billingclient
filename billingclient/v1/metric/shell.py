# NubeliU Billing SDK
# @autor: Sergio Colinas
import textwrap
from billingclient import exc
from billingclient.common import utils


def do_metric_definition_list(cc, args):
    data = cc.metrics.mappings.list()
    fields = ['id', 'gnocchi_metric', 'name', 'description', 'granularities',
              'time_range_start', 'time_range_end', 'group_by',
              'show_measures', 'show_cost', 'function', 'reaggregation']
    fields_labels = ['Id', 'Metric', 'Name', 'Description', 'Granularities',
                     'Time Range Start', 'Time Range End', 'Group By',
                     'Show Measures', 'Show Cost', 'Function', 'Reaggregation']
    utils.print_list(data, fields, fields_labels, sortby=0)


@utils.arg('--id',
           help='Metric definition Id to get.',
           required=True)
def do_metric_definition_get(cc, args):
    data = cc.metrics.mappings.get(definition_id=args.id)
    data_dict = data.to_dict()
    filters = data_dict["filters"] if data_dict["filters"] else ""
    data_dict["filters"] = "\n"
    for chunk in [filters[i:i+80] for i in range(0, len(filters), 80)]:
        data_dict["filters"] += chunk + "\n"
    utils.print_dict(data_dict)


@utils.arg('--gnocchi-metric',
           help='Name of the gnocchi source metric.',
           required=True)
@utils.arg('--name',
           help='Name of the metric definition.',
           required=True)
@utils.arg('--description',
           help='Metric definition description.',
           required=False)
@utils.arg('--granularities',
           help='Selected granularities.',
           required=True)
@utils.arg('--time-range-start',
           help='Time range start.',
           required=True)
@utils.arg('--time-range-end',
           help='Time range end.',
           required=True)
@utils.arg('--group-by',
           help='Selected grouping options.',
           required=False)
@utils.arg('--show-measures',
           help='Show metric measures.',
           required=True)
@utils.arg('--show-cost',
           help='Show associated cost.',
           required=True)
@utils.arg('--function',
           help='Aggregation function (Raw data granularities aggregation).',
           required=False)
@utils.arg('--reaggregation',
           help='Reaggregation function (Query aggregation).',
           required=False)
@utils.arg('--unit',
           help='Convertion unit.',
           required=False)
@utils.arg('--filters',
           help='Selected filter options.',
           required=False)
def do_metric_definition_create(cc, args):
    out = cc.metrics.mappings.create(
        gnocchi_metric=args.gnocchi_metric, name=args.name,
        description=args.description, granularities=args.granularities,
        time_range_start=args.time_range_start,
        time_range_end=args.time_range_end,
        group_by=args.group_by,
        show_measures="true" in args.show_measures.lower() or "1" in args.show_measures,
        show_cost="true" in args.show_cost.lower() or "1" in args.show_cost,
        function=args.function, reaggregation=args.reaggregation,
        unit=args.unit, filters=args.filters)
    data_dict = out.to_dict()
    filters = data_dict["filters"] if data_dict["filters"] else ''
    for chunk in [filters[i:i+80] for i in range(0, len(filters), 80)]:
        data_dict["filters"] += chunk + "\n"
    if data_dict["filters"]:
        data_dict["filters"] = data_dict["filters"][:-1]
    utils.print_dict(data_dict)


@utils.arg('--id',
           help='Metric definition Id to delete.',
           required=True)
def do_metric_definition_delete(cc, args):
    cc.metrics.mappings.delete(definition_id=args.id)


@utils.arg('--id',
           help='Metric definition Id to update.',
           required=True)
@utils.arg('--gnocchi-metric',
           help='Name of the gnocchi source metric.',
           required=False)
@utils.arg('--name',
           help='Name of the metric definition.',
           required=False)
@utils.arg('--description',
           help='Metric definition description.',
           required=False)
@utils.arg('--granularities',
           help='Selected granularities.',
           required=False)
@utils.arg('--time-range-start',
           help='Time range start in seconds.',
           required=False)
@utils.arg('--time-range-end',
           help='Time range end in seconds.',
           required=False)
@utils.arg('--group-by',
           help='Selected grouping options.',
           required=False)
@utils.arg('--show-measures',
           help='Show metric measures.',
           required=True)
@utils.arg('--show-cost',
           help='Show associated cost.',
           required=True)
@utils.arg('--function',
           help='Aggregation function (Raw data granularities aggregation).',
           required=False)
@utils.arg('--reaggregation',
           help='Reaggregation function (Query aggregation).',
           required=False)
@utils.arg('--unit',
           help='Convertion unit.',
           required=False)
@utils.arg('--filters',
           help='Selected filter options.',
           required=False)
def do_metric_definition_update(cc, args={}):
    """Update a metric definition."""
    arg_to_field_mapping = {
        'gnocchi_metric': 'gnocchi_metric',
        'name': 'name',
        'description': 'description',
        'granularities': 'granularities',
        'time_range_start': 'time_range_start',
        'time_range_end': 'time_range_end',
        'group_by': 'group_by',
        'function': 'function',
        'reaggregation': 'reaggregation',
        'show_measures': 'show_measures',
        'show_cost': 'show_cost',
        'unit': 'unit',
        'filters': 'filters',
    }
    try:
        mapping = cc.metrics.mappings.get(definition_id=args.id)
    except exc.HTTPNotFound:
        raise exc.CommandError('Metric definition not found: %s' % args.counter_name)
    for k, v in vars(args).items():
        if k in arg_to_field_mapping:
            if v is not None:
                if k == "show_measures" or k == "show_cost":
                    setattr(mapping, k, "true" in v.lower() or "1" in v)
                else:
                    setattr(mapping, k, v)
    utils.print_dict(cc.metrics.mappings.update(**mapping.dirty_fields).to_dict())


@utils.arg('--gnocchi-metric',
           help='Metric to get info.',
           required=False)
def do_metric_available_list(cc, args):
    data = cc.metrics.list_available_metrics(gnocchi_metric=args.gnocchi_metric)
    fields = ['metric', 'unit', 'has_cost', 'function', 'granularities', 'timespans', 'filters']
    fields_labels = ['Metric', 'Unit', 'Has Cost', 'Function', 'Granularities', 'Timespans', 'Filters']
    utils.print_list(data["metrics"], fields, fields_labels, formatters={
        "metric": utils.dict_formatter("metric"),
        "unit": utils.dict_formatter("unit"),
        "has_cost": utils.dict_formatter("has_cost"),
        "function": utils.dict_formatter("function"),
        "granularities": utils.granularity_formatter("granularities"),
        "timespans": utils.granularity_formatter("timespans"),
        "filters": utils.filters_formatter("filters")}, sortby=None)


@utils.arg('--id',
           help='Metric definition Id to get measures.',
           required=True)
@utils.arg('--granularity',
           help='Granularity to get measures.',
           required=False)
@utils.arg('--page-number',
           help='Page number to get measures.',
           required=False)
def do_metric_definition_measures_get(cc, args):
    data = cc.metrics.measures.get(definition_id=args.id,
                                   granularity=args.granularity,
                                   page_number=args.page_number)
    utils.print_metric_definition_measures(data)
