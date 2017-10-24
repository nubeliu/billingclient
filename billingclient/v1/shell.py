# NubeliU Billing SDK
# @autor: Sergio Colinas

from billingclient.common import utils
from billingclient import exc


def do_module_list(cc, args):
    '''List the samples for this meters.'''
    try:
        modules = cc.modules.list()
    except exc.HTTPNotFound:
        raise exc.CommandError('Modules not found: %s' % args.counter_name)
    else:
        field_labels = ['Module', 'Enabled']
        fields = ['module_id', 'enabled']
        utils.print_list(modules, fields, field_labels,
                         sortby=0)


@utils.arg('-n', '--name',
           help='Module name',
           required=True)
def do_module_enable(cc, args):
    '''Enable a module.'''
    try:
        module = cc.modules.get(module_id=args.name)
        module.enable()
    except exc.HTTPNotFound:
        raise exc.CommandError('Modules not found: %s' % args.counter_name)
    else:
        field_labels = ['Module', 'Enabled']
        fields = ['module_id', 'enabled']
        modules = [cc.modules.get(module_id=args.name)]
        utils.print_list(modules, fields, field_labels,
                         sortby=0)


@utils.arg('-n', '--name',
           help='Module name',
           required=True)
def do_module_disable(cc, args):
    '''Disable a module.'''
    try:
        module = cc.modules.get(module_id=args.name)
        module.disable()
    except exc.HTTPNotFound:
        raise exc.CommandError('Modules not found: %s' % args.counter_name)
    else:
        field_labels = ['Module', 'Enabled']
        fields = ['module_id', 'enabled']
        modules = [cc.modules.get(module_id=args.name)]
        utils.print_list(modules, fields, field_labels,
                         sortby=0)
