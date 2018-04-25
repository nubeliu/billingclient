# NubeliU Billing SDK
# @autor: Sergio Colinas
from billingclient.common import utils
from billingclient import exc


def do_metric_definition_list(cc, args):
    data = cc.metrics.mappings.list()
    fields = ['id', 'gnocchi_metric', 'name', 'description', 'show_measures',
              'show_cost', 'function', 'reaggregation']
    fields_labels = ['Id', 'Metric', 'Name', 'Description', 'Show Measures',
                     'Show Cost', 'Function', 'Reaggregation']
    utils.print_list(data, fields, fields_labels, sortby=0)


@utils.arg('--id',
           help='Metric definition Id to get.',
           required=True)
def do_metric_definition_get(cc, args):
    data = cc.metrics.mappings.get(definition_id=args.id)
    data_dict = data.to_dict()
    filters = data_dict["filters"] if data_dict["filters"] else ""
    data_dict["filters"] = "\n"
    for chunk in [filters[i: i + 80] for i in range(0, len(filters), 80)]:
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
def do_metric_definition_create(cc, args):
    out = cc.metrics.mappings.create(
        gnocchi_metric=args.gnocchi_metric, name=args.name,
        description=args.description,
        show_measures=("true" in args.show_measures.lower() or "1" in
                       args.show_measures),
        show_cost="true" in args.show_cost.lower() or "1" in args.show_cost,
        function=args.function, reaggregation=args.reaggregation,
        unit=args.unit)
    data_dict = out.to_dict()
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
def do_metric_definition_update(cc, args={}):
    """Update a metric definition."""
    arg_to_field_mapping = {
        'gnocchi_metric': 'gnocchi_metric',
        'name': 'name',
        'description': 'description',
        'function': 'function',
        'reaggregation': 'reaggregation',
        'show_measures': 'show_measures',
        'show_cost': 'show_cost',
        'unit': 'unit',
    }
    try:
        mapping = cc.metrics.mappings.get(definition_id=args.id)
    except exc.HTTPNotFound:
        raise exc.CommandError('Metric definition not found: %s' %
                               args.counter_name)
    for k, v in vars(args).items():
        if k in arg_to_field_mapping:
            if v is not None:
                if k == "show_measures" or k == "show_cost":
                    setattr(mapping, k, "true" in v.lower() or "1" in v)
                else:
                    setattr(mapping, k, v)
    utils.print_dict(cc.metrics.mappings.update(
        **mapping.dirty_fields).to_dict())


@utils.arg('--gnocchi-metric',
           help='Metric to get info.',
           required=False)
@utils.arg('--refresh',
           help='Force refresh cache.',
           required=False)
def do_metric_available_list(cc, args):
    data = cc.metrics.list_available_metrics(
        gnocchi_metric=args.gnocchi_metric, refresh=args.refresh)
    fields = ['metric', 'gnocchi_unit', 'unit', 'has_cost', 'function',
              'granularities', 'timespans', 'filters']
    fields_labels = ['Metric', 'Gnocchi Unit', 'Unit', 'Has Cost', 'Function',
                     'Granularities', 'Timespans', 'Filters']
    utils.print_list(data["metrics"], fields, fields_labels, formatters={
        "metric": utils.dict_formatter("metric"),
        "gnocchi_unit": utils.dict_formatter("gnocchi_unit"),
        "unit": utils.dict_formatter("unit"),
        "has_cost": utils.dict_formatter("has_cost"),
        "function": utils.dict_formatter("function"),
        "granularities": utils.granularity_formatter("granularities"),
        "timespans": utils.granularity_formatter("timespans"),
        "filters": utils.filters_formatter("filters")}, sortby=None)
