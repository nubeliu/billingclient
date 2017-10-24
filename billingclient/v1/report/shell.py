# NubeliU Billing SDK
# @autor: Sergio Colinas
from billingclient.common import utils


def do_report_definition_list(cc, args):
    data = cc.metrics.reports.list()
    fields = ['id', 'name', 'description', 'metrics', 'granularities', 'time_range_start', 'time_range_end', 'group_by', 'status', 'billing_user', 'updated_at', 'hidden', 'items_per_page']
    fields_labels = ['Id', 'Name', 'Description', 'Metrics', 'Granularities', 'Time Range Start', 'Time Range End', 'Group By', 'Status', 'Billing User', 'Updated at', 'Hidden', 'Items per Page']
    utils.print_list(data, fields, fields_labels, sortby=0)


@utils.arg('--id',
           help='Report definition Id to get.',
           required=True)
def do_report_definition_get(cc, args):
    data = cc.metrics.reports.get(definition_id=args.id)
    data_dict = data.to_dict()
    filters = data_dict["filters"] if data_dict["filters"] else ''
    for chunk in [filters[i:i+80] for i in range(0, len(filters), 80)]:
        data_dict["filters"] += chunk + "\n"
    if data_dict["filters"]:
        data_dict["filters"] = data_dict["filters"][:-1]
    utils.print_dict(data_dict)


@utils.arg('--name',
           help='Name of the metric definition.',
           required=True)
@utils.arg('--description',
           help='Metric definition description.',
           required=False)
@utils.arg('--metrics',
           help='List of metrics to include in the report.',
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
@utils.arg('--billing-user',
           help='Indicates that the report will be available for billing_user.',
           required=False)
@utils.arg('--items-per-page',
           help='Number of items per page.',
           required=False)
def do_report_definition_create(cc, args):
    out = cc.metrics.reports.create(name=args.name,
        description=args.description, metrics=args.metrics, granularities=args.granularities,
        time_range_start=args.time_range_start, time_range_end=args.time_range_end,
        group_by=args.group_by, filters=args.filters, items_per_page=args.items_per_page,
        billing_user=True if args.billing_user and (args.billing_user.lower() == 'true' or args.billing_user.lower() == '1') else False)
    data_dict = out.to_dict()
    filters = data_dict["filters"] if data_dict["filters"] else ''
    for chunk in [filters[i:i+80] for i in range(0, len(filters), 80)]:
        data_dict["filters"] += chunk + "\n"
    if data_dict["filters"]:
        data_dict["filters"] = data_dict["filters"][:-1]
    utils.print_dict(data_dict)


@utils.arg('--id',
           help='Report definition Id to delete.',
           required=True)
def do_report_definition_delete(cc, args):
    cc.metrics.reports.delete(definition_id=args.id)


@utils.arg('--id',
           help='Report definition Id to update.',
           required=True)
@utils.arg('--name',
           help='Name of the metric definition.',
           required=False)
@utils.arg('--description',
           help='Metric definition description.',
           required=False)
@utils.arg('--metrics',
           help='List of metrics to include in the report.',
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
@utils.arg('--filters',
           help='Selected filter options.',
           required=False)
@utils.arg('--billing-user',
           help='Indicates that the report will be available for billing_user.',
           required=False)
@utils.arg('--items-per-page',
           help='Number of items per page.',
           required=False)
def do_report_definition_update(cc, args={}):
    """Update a metric definition."""
    arg_to_field_mapping = {
        'name': 'name',
        'description': 'description',
        'metrics': 'metrics',
        'granularities': 'granularities',
        'time_range_start': 'time_range_start',
        'time_range_end': 'time_range_end',
        'group_by': 'group_by',
        'filters': 'filters',
        'billing_user': 'billing_user',
        'items_per_page': 'items_per_page'
    }
    try:
        mapping = cc.metrics.reports.get(definition_id=args.id)
    except exc.HTTPNotFound:
        raise exc.CommandError('Metric definition not found: %s' % args.counter_name)
    for k, v in vars(args).items():
        if k in arg_to_field_mapping:
            if v is not None:
                if k == "billing_user":
                    setattr(mapping, k, "true" in v.lower() or "1" in v)
                else:
                    setattr(mapping, k, v)
    cc.metrics.reports.update(id=mapping.dirty_fields["id"], name=mapping.dirty_fields["name"],
        metrics=mapping.dirty_fields["metrics"], granularities=mapping.dirty_fields["granularities"],
        description=mapping.dirty_fields["description"], time_range_start=mapping.dirty_fields["time_range_start"],
        time_range_end=mapping.dirty_fields["time_range_end"], group_by=mapping.dirty_fields["group_by"],
        filters=mapping.dirty_fields["filters"], billing_user=mapping.dirty_fields["billing_user"],
        items_per_page=mapping.dirty_fields["items_per_page"])


@utils.arg('--id',
           help='Report definition Id to get measures.',
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
def do_report_definition_measures_get(cc, args):
    data = cc.metrics.report_measures.get(definition_id=args.id,
                                          granularity=args.granularity,
                                          page_number=args.page_number,
                                          items_per_page=args.items_per_page)
    utils.print_report_definition_measures(data)


@utils.arg('-a', '--account-id',
           help='AWS access key id',
           required=True, dest='account_id')
@utils.arg('-s', '--secret-access-key',
           help='AWS secret access key',
           required=True, dest='secret_access_key')
@utils.arg('-u', '--u-domain-id',
           help='User domain ID',
           required=True, dest='u_domain_id')
@utils.arg('-t', '--term-duration',
           help='Not required. You can choose AWS term duration. This will affect the number of potential savings.'
                ' Default: 1_year. Available options: 1_year | 3_years_standard | 3_years_convertible ',
           required=False, dest='term_duration')
@utils.arg('-o', '--offering-type',
           help='Not required. Choose AWS OfferingType. This will affect the number of potential savings.'
                ' Default: no_upfront. Available options: no_upfront | partial_upfront | all_upfront ',
           required=False, dest='offering_type')
def do_aws_ri_coverage_get(cc, args):
    aws_ri_coverage = cc.reports.get_aws_ri_coverage(account_id=args.account_id,
                                                     secret_access_key=args.secret_access_key,
                                                     u_domain_id=args.u_domain_id)
    valid_terms = ['1_year', '3_years_standard', '3_years_convertible']
    valid_offering_types = ['no_upfront', 'partial_upfront', 'all_upfront']
    choosed_term = args.term_duration if args.term_duration is not None and args.term_duration in valid_terms else "1_year"
    choosed_offering_type = args.offering_type if args.offering_type is not None and args.offering_type in valid_offering_types else "no_upfront"
    for element in aws_ri_coverage:
        element['potential_savings_pm'] = element['potential_savings_pm'][choosed_term][choosed_offering_type]
        utils.print_dict(element)
    return aws_ri_coverage
