from .by_activity_type import ByActivityType, do_nothing_for_all_activities


def build_do_for_types(actions: dict):
    by_activity_type = ByActivityType({**do_nothing_for_all_activities, **actions})
    return by_activity_type.act
