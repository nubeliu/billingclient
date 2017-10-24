# NubeliU Billing SDK
# @autor: Sergio Colinas

from billingclient.common import base


class MetricRuleSet(base.Resource):
    key = 'metric_rule_set'

    def __repr__(self):
        return "<gnocchi.MetricRuleSet %s>" % self._info

    @property
    def metadata_rule_sets(self):
        return MetadataRuleSetManager(client=self.manager.client).findall(
            metric_rule_set_id=self.metric_rule_set_id
        )

    @property
    def metric_rules(self):
        return MetricRuleManager(client=self.manager.client).findall(
            metric_rule_set_id=self.metric_rule_set_id
        )


class MetricRuleSetManager(base.CrudManager):
    resource_class = MetricRuleSet
    base_url = '/v1/rating/gnocchi'
    key = 'metric_rule_set'
    collection_key = 'metric_rule_sets'


class MetadataRuleSet(base.Resource):
    key = 'metadata_rule_set'

    def __repr__(self):
        return "<gnocchi.MetadataRuleSet %s>" % self._info

    @property
    def metric_rule_set(self):
        return MetricRuleSetManager(client=self.manager.client).get(
            metric_rule_set_id=self.metric_rule_set_id
        )


class MetadataRuleSetManager(base.CrudManager):
    resource_class = MetadataRuleSet
    base_url = '/v1/rating/gnocchi'
    key = 'metadata_rule_set'
    collection_key = 'metadata_rule_sets'


class MetricRule(base.Resource):
    key = 'metric_rule'

    def __repr__(self):
        return "<gnocchi.MetricRule %s>" % self._info

    @property
    def metric_rule_set(self):
        return MetricRuleSetManager(client=self.manager.client).get(
            metric_rule_set_id=self.metric_rule_set_id
        )


class MetadataRule(base.Resource):
    key = 'metadata_rule'

    def __repr__(self):
        return "<gnocchi.MetadataRule %s>" % self._info

    @property
    def metadata_rule_set(self):
        if self.metadata_rule_set_id is None:
            return None
        return MetadataRuleSetManager(client=self.manager.client).get(
            metric_rule_set_id=self.metric_rule_set_id
        )


class MetricRuleManager(base.CrudManager):
    resource_class = MetricRule
    base_url = '/v1/rating/gnocchi'
    key = 'metric_rule'
    collection_key = 'metric_rules'


class MetadataRuleManager(base.CrudManager):
    resource_class = MetadataRule
    base_url = '/v1/rating/gnocchi'
    key = 'metadata_rule'
    collection_key = 'metadata_rules'


class ThresholdRule(base.Resource):
    key = 'threshold_rule'

    def __repr__(self):
        return "<gnocchi.ThresholdRule %s>" % self._info


class ThresholdRuleManager(base.CrudManager):
    resource_class = ThresholdRule
    base_url = '/v1/rating/gnocchi'
    key = 'threshold_rule'
    collection_key = 'threshold_rules'
