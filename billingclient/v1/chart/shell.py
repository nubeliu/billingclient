# NubeliU Billing SDK
# @autor: Sergio Colinas
import textwrap

from billingclient.common import utils
from billingclient import exc


def do_chart_definition_list(cc, args):
    data = cc.charts.mappings.list()
    fields = ['id', 'gnocchi_metric', 'name', 'description', 'granularities',
              'time_range_start', 'time_range_end', 'group_by',
              'show_measures', 'show_cost', 'billing_user', 'function',
              'reaggregation', 'chart_type', 'chart_width', 'chart_height',
              'chart_x', 'chart_y', 'is_in_use', 'hidden']
    fields_labels = ['Id', 'Metric', 'Name', 'Description', 'Granularities',
                     'Time Range Start', 'Time Range End', 'Group By',
                     'Show Measures', 'Show Cost', 'Billing User', 'Function',
                     'Reaggregation', 'Chart Type', 'Chart Width',
                     'Chart Heigth', 'Chart posX', 'Chart posY', 'Is in Use',
                     'Hidden']
    utils.print_list(data, fields, fields_labels, sortby=0)


def do_dashboard_definition_list(cc, args):
    data = cc.charts.dashboards.list()
    fields = ['id', 'name', 'description', 'charts', 'charts_width',
              'charts_height', 'charts_x', 'charts_y', 'status',
              'billing_user', 'is_default', 'updated_at', 'hidden']
    fields_labels = ['Id', 'Name', 'Description', 'Charts', 'Charts Widths',
                     'Charts Heights', 'Charts X', 'Charts Y', 'Status',
                     'Billing User', 'Is Default', 'Updated at',
                     'Hidden']
    utils.print_list(data, fields, fields_labels, sortby=0)


@utils.arg('--id',
           help='Chart definition Id to get.',
           required=True)
def do_chart_definition_get(cc, args):
    data = cc.charts.mappings.get(definition_id=args.id)
    data_dict = data.to_dict()
    filters = data_dict["filters"] if data_dict["filters"] else ""
    data_dict["filters"] = "\n"
    for chunk in [filters[i: i + 80] for i in range(0, len(filters), 80)]:
        data_dict["filters"] += chunk + "\n"
    utils.print_dict(data_dict)


@utils.arg('--id',
           help='Dashboard definition Id to get.',
           required=True)
def do_dashboard_definition_get(cc, args):
    data = cc.charts.dashboards.get(definition_id=args.id)
    data_dict = data.to_dict()
    utils.print_dict(data_dict)


def do_dashboard_definition_get_default(cc, args):
    data = cc.charts.dashboards.get_default()
    print(data)


@utils.arg('--gnocchi-metric',
           help='Name of the gnocchi source metric.',
           required=True)
@utils.arg('--name',
           help='Name of the chart definition.',
           required=True)
@utils.arg('--description',
           help='Chart definition description.',
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
           required=True)
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
@utils.arg('--chart-type',
           help='Chart type.',
           required=True)
@utils.arg('--billing-user',
           help='Indicates that the chart will be available for billing_user.',
           required=False)
def do_chart_definition_create(cc, args):
    out = cc.charts.mappings.create(
        gnocchi_metric=args.gnocchi_metric, name=args.name,
        description=args.description, granularities=args.granularities,
        time_range_start=args.time_range_start,
        time_range_end=args.time_range_end,
        group_by=args.group_by, function=args.function,
        reaggregation=args.reaggregation,
        show_measures=("true" in args.show_measures.lower() or "1" in
                       args.show_measures),
        show_cost="true" in args.show_cost.lower() or "1" in args.show_cost,
        unit=args.unit, filters=args.filters, chart_type=args.chart_type,
        billing_user=(True if args.billing_user and (
            args.billing_user.lower() == 'true' or args.billing_user.lower()
            == '1') else False))
    data_dict = out.to_dict()
    filters = data_dict["filters"] if data_dict["filters"] else ''
    for chunk in [filters[i: i + 80] for i in range(0, len(filters), 80)]:
        data_dict["filters"] += chunk + "\n"
    if data_dict["filters"]:
        data_dict["filters"] = data_dict["filters"][:-1]
    utils.print_dict(data_dict)


@utils.arg('--name',
           help='Name of the chart definition.',
           required=True)
@utils.arg('--description',
           help='Chart definition description.',
           required=False)
@utils.arg('--charts',
           help='List of charts to include in the dashboard.',
           required=True)
@utils.arg('--charts-width',
           help='List of charts widths to include in the dashboard.',
           required=False)
@utils.arg('--charts-height',
           help='List of charts heights to include in the dashboard.',
           required=False)
@utils.arg('--charts-x',
           help='List of charts pos_x to include in the dashboard.',
           required=False)
@utils.arg('--charts-y',
           help='List of charts pos_y to include in the dashboard.',
           required=False)
@utils.arg('--billing-user',
           help='Indicates that the dashboard will be available for '
                'billing_user.',
           required=False)
@utils.arg('--is-default',
           help='Indicates that the dashboard will be the default dashboard.',
           required=False)
def do_dashboard_definition_create(cc, args):
    out = cc.charts.dashboards.create(
        name=args.name, description=args.description, charts=args.charts,
        charts_width=args.charts_width, charts_height=args.charts_height,
        charts_x=args.charts_x, charts_y=args.charts_y,
        billing_user=(True if args.billing_user and (
            args.billing_user.lower() == 'true' or args.billing_user.lower()
            == '1') else False),
        is_default=(True if args.is_default and
                    (args.is_default.lower() == 'true' or
                     args.is_default.lower() == '1') else False))
    data_dict = out.to_dict()
    utils.print_dict(data_dict)


@utils.arg('--id',
           help='Chart definition Id to delete.',
           required=True)
def do_chart_definition_delete(cc, args):
    cc.charts.mappings.delete(definition_id=args.id)


@utils.arg('--id',
           help='Dashboard definition Id to delete.',
           required=True)
def do_dashboard_definition_delete(cc, args):
    cc.charts.dashboards.delete(definition_id=args.id)


@utils.arg('--id',
           help='Chart definition Id to update.',
           required=True)
@utils.arg('--gnocchi-metric',
           help='Name of the gnocchi source metric.',
           required=False)
@utils.arg('--name',
           help='Name of the chart definition.',
           required=False)
@utils.arg('--description',
           help='Chart definition description.',
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
           required=False)
@utils.arg('--show-cost',
           help='Show associated cost.',
           required=False)
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
@utils.arg('--chart-type',
           help='Chart type.',
           required=False)
@utils.arg('--billing-user',
           help='Indicates that the chart will be available for billing_user.',
           required=False)
def do_chart_definition_update(cc, args={}):
    """Update a chart definition."""
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
        'billing_user': 'billing_user',
    }
    try:
        mapping = cc.charts.mappings.get(definition_id=args.id)
    except exc.HTTPNotFound:
        raise exc.CommandError('Chart definition not found: %s' %
                               args.counter_name)
    for k, v in vars(args).items():
        if k in arg_to_field_mapping:
            if v is not None:
                if k == "billing_user":
                    setattr(mapping, k, "true" in v.lower() or "1" in v)
                elif k == "show_measures" or k == "show_cost":
                    setattr(mapping, k, "true" in v.lower() or "1" in v)
                else:
                    setattr(mapping, k, v)
    utils.print_dict(cc.charts.mappings.update(
        id=mapping.dirty_fields["id"],
        gnocchi_metric=mapping.dirty_fields["gnocchi_metric"],
        name=mapping.dirty_fields["name"],
        granularities=mapping.dirty_fields["granularities"],
        show_measures=mapping.dirty_fields["show_measures"],
        show_cost=mapping.dirty_fields["show_cost"],
        function=mapping.dirty_fields["function"],
        reaggregation=mapping.dirty_fields["reaggregation"],
        description=mapping.dirty_fields["description"],
        time_range_start=mapping.dirty_fields["time_range_start"],
        time_range_end=mapping.dirty_fields["time_range_end"],
        group_by=mapping.dirty_fields["group_by"],
        unit=mapping.dirty_fields["unit"],
        filters=mapping.dirty_fields["filters"],
        chart_type=mapping.dirty_fields["chart_type"],
        billing_user=mapping.dirty_fields["billing_user"]).to_dict())


@utils.arg('--id',
           help='Dashboard definition Id to update.',
           required=True)
@utils.arg('--name',
           help='Name of the dashboard definition.',
           required=False)
@utils.arg('--description',
           help='Dashboard definition description.',
           required=False)
@utils.arg('--charts',
           help='List of charts to include in the dashboard.',
           required=False)
@utils.arg('--charts-width',
           help='List of charts widths to include in the dashboard.',
           required=False)
@utils.arg('--charts-heights',
           help='List of charts heights to include in the dashboard.',
           required=False)
@utils.arg('--charts-x',
           help='List of charts pos_x to include in the dashboard.',
           required=False)
@utils.arg('--charts-y',
           help='List of charts pos_y to include in the dashboard.',
           required=False)
@utils.arg('--billing-user',
           help='Indicates that the dashboard will be available for '
                'billing_user.',
           required=False)
@utils.arg('--is-default',
           help='Indicates that the dashboard will be the default dashboard.',
           required=False)
def do_dashboard_definition_update(cc, args={}):
    """Update a dashboard definition."""
    arg_to_field_mapping = {
        'id': 'id',
        'name': 'name',
        'charts': 'charts',
        'charts_width': 'charts_width',
        'charts_height': 'charts_height',
        'charts_x': 'charts_x',
        'charts_y': 'charts_y',
        'description': 'description',
        'billing_user': 'billing_user',
        'is_default': 'is_default'
    }
    try:
        mapping = cc.charts.dashboards.get(definition_id=args.id)
    except exc.HTTPNotFound:
        raise exc.CommandError('Dashboard definition not found: %s' %
                               args.counter_name)
    for k, v in vars(args).items():
        if k in arg_to_field_mapping:
            if v is not None:
                if k == "billing_user":
                    setattr(mapping, k, "true" in v.lower() or "1" in v)
                elif k == "is_default":
                    setattr(mapping, k, "true" in v.lower() or "1" in v)
                else:
                    setattr(mapping, k, v)
    data_dict = cc.charts.dashboards.update(
        id=mapping.dirty_fields["id"], name=mapping.dirty_fields["name"],
        charts=mapping.dirty_fields["charts"],
        charts_width=mapping.dirty_fields["charts_width"],
        charts_height=mapping.dirty_fields["charts_height"],
        charts_x=mapping.dirty_fields["charts_x"],
        charts_y=mapping.dirty_fields["charts_y"],
        description=mapping.dirty_fields["description"],
        billing_user=mapping.dirty_fields["billing_user"],
        is_default=mapping.dirty_fields["is_default"]).to_dict()
    utils.print_dict(data_dict)


def _granularity_formatter(list):
    return lambda o: '\n'.join([str(item) for item in o[list]])


def _filters_formatter(dict):
    return lambda o: '\n'.join(['\n'.join(textwrap.wrap(
        str(item["filter"]).replace('_id', '') + ": " + ', '.join(
            dict["display_name"] for dict in item["values"]), 80))
        for item in o[dict]])


def _dict_formatter(field):
    return lambda o: o[field]


def _print_chart_definition_measures(data):
    if isinstance(data, dict):
        data_dict = data
    else:
        data_dict = data.to_dict()
    print("Chart name: " + unicode(data_dict["name"]))
    print("Chart description: " + unicode(data_dict["description"]))
    print("Chart unit: " + unicode(data_dict["unit"]))
    print("Chart has measures: " + unicode(data_dict["has_measures"]))
    print("Chart has cost: " + unicode(data_dict["has_cost"]))
    for group in data_dict["definition_measures"]:
        for key, val in group.iteritems():
            if key != 'measures':
                print(key + ": " + unicode(val["display_name"]))
        if (len(group["measures"]) > 0 and "value" in group["measures"][0]
                and "cost" in group["measures"][0]):
            fields = ['timestamp', 'value', 'cost', 'granularity']
            fields_labels = ['Timestamp', 'Value', 'Cost', 'Granularity']
            utils.print_list(
                group["measures"], fields, fields_labels,
                formatters={
                    "timestamp": _dict_formatter("timestamp"),
                    "value": _dict_formatter("value"),
                    "cost": _dict_formatter("cost"),
                    "granularity": _dict_formatter("granularity")},
                sortby=0)
        elif len(group["measures"]) > 0 and "value" in group["measures"][0]:
            fields = ['timestamp', 'value', 'granularity']
            fields_labels = ['Timestamp', 'Value', 'Granularity']
            utils.print_list(
                group["measures"], fields, fields_labels,
                formatters={
                    "timestamp": _dict_formatter("timestamp"),
                    "value": _dict_formatter("value"),
                    "granularity": _dict_formatter("granularity")},
                sortby=0)
        else:
            fields = ['timestamp', 'cost', 'granularity']
            fields_labels = ['Timestamp', 'Cost', 'Granularity']
            utils.print_list(
                group["measures"], fields, fields_labels,
                formatters={
                    "timestamp": _dict_formatter("timestamp"),
                    "cost": _dict_formatter("cost"),
                    "granularity": _dict_formatter("granularity")},
                sortby=0)


def _print_dashboard_definition_measures(data):
    print("Dashboard name: " + unicode(data.name))
    print("Dashboard description: " + unicode(data.description))
    for group in data.to_dict()["dashboard_charts"]:
        _print_chart_definition_measures(group)


@utils.arg('--id',
           help='Id of the chart to get measures.',
           required=True)
@utils.arg('--granularity',
           help='Granularity to get (returns the finer by default).',
           required=False)
@utils.arg('--groupby',
           help='Grouping option to get (returns the first by default).',
           required=False)
@utils.arg('--page-number',
           help='Number of the page to get (default 1).',
           required=False)
@utils.arg('--items-per-page',
           help='Items per page (default 1000).',
           required=False)
@utils.arg('--filter-domain-id',
           help='Domain id to filter.',
           required=False)
@utils.arg('--filter-project-id',
           help='Project id to filter.',
           required=False)
def do_chart_definition_measures_get(cc, args):
    data = cc.charts.measures.get(definition_id=args.id,
                                  granularity=args.granularity,
                                  groupby=args.groupby,
                                  page_number=args.page_number,
                                  items_per_page=args.items_per_page,
                                  domain_id=args.filter_domain_id,
                                  project_id=args.filter_project_id)
    _print_chart_definition_measures(data)


@utils.arg('--id',
           help='Dashboard definition Id to get measures.',
           required=True)
def do_dashboard_definition_measures_get(cc, args):
    data = cc.charts.dashboard_measures.get(definition_id=args.id)
    _print_dashboard_definition_measures(data)


@utils.arg('--gnocchi-metric',
           help='Name of the gnocchi source metric.',
           required=True)
@utils.arg('--name',
           help='Name of the chart definition.',
           required=True)
@utils.arg('--description',
           help='Chart definition description.',
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
@utils.arg('--granularity',
           help='Granularity to get measures.',
           required=True)
def do_chart_definition_measures_preview(cc, args):
    data = cc.charts.measures.preview(
        gnocchi_metric=args.gnocchi_metric, name=args.name,
        description=args.description, granularities=args.granularities,
        time_range_start=args.time_range_start,
        time_range_end=args.time_range_end, group_by=args.group_by,
        show_measures=("true" in args.show_measures.lower() or "1" in
                       args.show_measures),
        show_cost="true" in args.show_cost.lower() or "1" in args.show_cost,
        function=args.function, reaggregation=args.reaggregation,
        unit=args.unit, filters=args.filters, granularity=args.granularity)
    _print_chart_definition_measures(data)


@utils.arg('--name',
           help='Name of the dashboard definition.',
           required=True)
@utils.arg('--description',
           help='Dashboard definition description.',
           required=False)
@utils.arg('--charts',
           help='List of charts to include in the dashboard.',
           required=True)
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
@utils.arg('--filters',
           help='Selected filter options.',
           required=False)
@utils.arg('--granularity',
           help='Granularity to get measures.',
           required=True)
@utils.arg('--page-number',
           help='Page number to get measures.',
           required=True)
def do_dashboard_definition_measures_preview(cc, args):
    data = cc.charts.dashboard_measures.preview(
        name=args.name, charts=args.charts, description=args.description,
        granularities=args.granularities,
        time_range_start=args.time_range_start,
        time_range_end=args.time_range_end, group_by=args.group_by,
        filters=args.filters, granularity=args.granularity,
        page_number=args.page_number)
    _print_dashboard_definition_measures(data)
