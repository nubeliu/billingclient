# NubeliU Billing SDK
# @autor: Sergio Colinas
from billingclient.common import utils
from billingclient import exc


def do_widget_definition_list(cc, args):
    data = cc.metrics.widgets.list()
    fields = ['id', 'name', 'description', 'metrics', 'granularities',
              'time_range_start', 'time_range_end', 'group_by', 'status',
              'billing_user', 'updated_at', 'hidden', 'items_per_page',
              'top_n', 'reverse_top']
    fields_labels = ['Id', 'Name', 'Description', 'Metrics', 'Granularities',
                     'Time Range Start', 'Time Range End', 'Group By',
                     'Status', 'Billing User', 'Updated at', 'Hidden',
                     'Items per Page', 'Top N', 'Reverse Top']
    utils.print_list(data, fields, fields_labels, sortby=0)


@utils.arg('--id',
           help='Widget definition Id to get.',
           required=True)
def do_widget_definition_get(cc, args):
    data = cc.metrics.widgets.get(definition_id=args.id)
    data_dict = data.to_dict()
    filters = data_dict["filters"] if data_dict["filters"] else ''
    for chunk in [filters[i: i + 80] for i in range(0, len(filters), 80)]:
        data_dict["filters"] += chunk + "\n"
    if data_dict["filters"]:
        data_dict["filters"] = data_dict["filters"][:-1]
    utils.print_dict(data_dict)


@utils.arg('--widget-type',
           help='Types (0: Pie;  1: Donut; 2: Bar; 3: Column; 4: '
                'Line; 5: Line & Column; 6: Tile; 7: Stacked Bar; '
                '8: Stacked Column; 9: Scalar; 10: Table)',
           required=True)
@utils.arg('--name',
           help='Name of the metric definition.',
           required=True)
@utils.arg('--description',
           help='Metric definition description.',
           required=False)
@utils.arg('--metrics',
           help='List of metrics to include in the widget.',
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
@utils.arg('--top-n',
           help='Get top N categories and group less significative ones.',
           required=False)
@utils.arg('--reverse-top',
           help='Indicates if it has to show top N (True) or bottom',
           required=False)
@utils.arg('--items-per-page',
           help='Number of items per page.',
           required=False)
@utils.arg('--filters',
           help='Selected filter options.',
           required=False)
@utils.arg('--billing-user',
           help='Indicates that the widget will be available for '
                'billing_user.',
           required=False)
@utils.arg('--hidden',
           help='Use to hide system reserved widgets.',
           required=False)
def do_widget_definition_create(cc, args):
    out = cc.metrics.widgets.create(
        widget_type=args.widget_type, name=args.name,
        description=args.description, metrics=args.metrics,
        granularities=args.granularities,
        time_range_start=args.time_range_start,
        time_range_end=args.time_range_end, group_by=args.group_by,
        filters=args.filters, items_per_page=args.items_per_page,
        billing_user=True
        if args.billing_user and (args.billing_user.lower() == 'true' or
                                  args.billing_user.lower() == '1') else False,
        top_n=args.top_n,
        reverse_top=True
        if args.billing_user and (args.reverse_top.lower() == 'true' or
                                  args.reverse_top.lower() == '1') else False,
        hidden=True if args.hidden and (args.hidden.lower() == 'true' or
                                        args.hidden.lower() == '1') else False)
    data_dict = out.to_dict()
    filters = data_dict["filters"] if data_dict["filters"] else ''
    for chunk in [filters[i: i + 80] for i in range(0, len(filters), 80)]:
        data_dict["filters"] += chunk + "\n"
    if data_dict["filters"]:
        data_dict["filters"] = data_dict["filters"][:-1]
    utils.print_dict(data_dict)


@utils.arg('--id',
           help='Widget definition Id to delete.',
           required=True)
def do_widget_definition_delete(cc, args):
    cc.metrics.widgets.delete(definition_id=args.id)


@utils.arg('--id',
           help='Widget definition Id to update.',
           required=True)
@utils.arg('--widget-type',
           help='Types (0: Pie;  1: Donut; 2: Bar; 3: Column; 4: '
                'Line; 5: Line & Column; 6: Tile; 7: Stacked Bar; '
                '8: Stacked Column; 9: Scalar; 10: Table)',
           required=True)
@utils.arg('--name',
           help='Name of the metric definition.',
           required=False)
@utils.arg('--description',
           help='Metric definition description.',
           required=False)
@utils.arg('--metrics',
           help='List of metrics to include in the widget.',
           required=True)
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
@utils.arg('--top-n',
           help='Get top N categories and group less significative ones.',
           required=False)
@utils.arg('--reverse-top',
           help='Indicates if it has to show top N (True) or bottom',
           required=False)
@utils.arg('--filters',
           help='Selected filter options.',
           required=False)
@utils.arg('--billing-user',
           help='Indicates that the widget will be available for '
                'billing_user.',
           required=False)
@utils.arg('--items-per-page',
           help='Number of items per page.',
           required=False)
@utils.arg('--hidden',
           help='Use to hide system reserved widgets.',
           required=False)
def do_widget_definition_update(cc, args={}):
    """Update a metric definition."""
    arg_to_field_mapping = {
        'widget_type': 'widget_type',
        'name': 'name',
        'description': 'description',
        'metrics': 'metrics',
        'granularities': 'granularities',
        'time_range_start': 'time_range_start',
        'time_range_end': 'time_range_end',
        'group_by': 'group_by',
        'top_n': 'top_n',
        'reverse_top': 'reverse_top',
        'filters': 'filters',
        'billing_user': 'billing_user',
        'items_per_page': 'items_per_page',
        'hidden': 'hidden'
    }
    try:
        mapping = cc.metrics.widgets.get(definition_id=args.id)
    except exc.HTTPNotFound:
        raise exc.CommandError('Metric definition not found: %s' %
                               args.counter_name)
    for k, v in vars(args).items():
        if k in arg_to_field_mapping:
            if v is not None:
                if k == "billing_user" or k == "hidden":
                    setattr(mapping, k, "true" in v.lower() or "1" in v)
                else:
                    setattr(mapping, k, v)
    cc.metrics.widgets.update(
        id=mapping.dirty_fields["id"],
        widget_type=mapping.dirty_fields["widget_type"],
        name=mapping.dirty_fields["name"],
        metrics=mapping.dirty_fields["metrics"],
        granularities=mapping.dirty_fields["granularities"],
        description=mapping.dirty_fields["description"],
        time_range_start=mapping.dirty_fields["time_range_start"],
        time_range_end=mapping.dirty_fields["time_range_end"],
        group_by=mapping.dirty_fields["group_by"],
        top_n=mapping.dirty_fields["top_n"],
        reverse_top=mapping.dirty_fields["reverse_top"],
        filters=mapping.dirty_fields["filters"],
        billing_user=mapping.dirty_fields["billing_user"],
        items_per_page=mapping.dirty_fields["items_per_page"],
        hidden=mapping.dirty_fields["hidden"])


@utils.arg('--id',
           help='Widget definition Id to get measures.',
           required=True)
@utils.arg('--granularity',
           help='Granularity to get measures.',
           required=False)
@utils.arg('--page-number',
           help='Page number to get measures.',
           required=False)
@utils.arg('--items-per-page',
           help='Items per page.',
           required=False)
def do_widget_definition_measures_get(cc, args):
    data = cc.metrics.widget_measures.get(definition_id=args.id,
                                          granularity=args.granularity,
                                          page_number=args.page_number,
                                          items_per_page=args.items_per_page)
    utils.print_widget_definition_measures(data)
