"""
Validation schema.

Declare any kind of validation schema here.
"""
from datetime import datetime


def convert_date(s):
    """Convert date."""
    return datetime.strptime(s, '%Y-%m-%d')


create_ingredient = {
    'name': {'type': 'string', 'required': True, 'empty': False},
    'measure_unit': {'type': 'string', 'required': True, 'empty': False}
}

create_ingredients = {
    'ingredients': {
        'required': True,
        'type': 'list',
        'schema': {
            'type': 'dict',
            'schema': create_ingredient
        }
    }
}

create_recipe_ingredient = {
    'type': 'dict',
    'schema': {
        'ingredient_id': {'type': 'integer', 'required': True, 'empty': False},
        'amount_for_two': {'type': 'float', 'required': True, 'empty': False},
        'amount_for_four': {'type': 'float', 'required': True, 'empty': False},
        'included_in_delivery': {'type': 'boolean', 'required': True, 'default': True}
    }
}

create_recipe = {
    'name': {'type': 'string', 'required': True, 'empty': False},
    'sub_header': {'type': 'string', 'required': True, 'empty': False},
    'description': {'type': 'string', 'required': True, 'empty': False},
    'tags': {'type': 'string', 'required': True, 'empty': False},
    'category': {'type': 'string', 'required': True, 'empty': False},
    'allergens': {'type': 'string', 'required': True, 'empty': False},
    'prep_time': {'type': 'float', 'required': True, 'empty': False},
    'prep_time_unit': {'type': 'string', 'required': True, 'empty': False},
    'difficulty': {'type': 'string', 'required': True, 'empty': False},
    'ingredients': {
        'required': True,
        'type': 'list',
        'schema': create_recipe_ingredient
    }
}


update_recipe = {
    'name': {'type': 'string', 'required': False, 'empty': False},
    'sub_header': {'type': 'string', 'required': False, 'empty': False},
    'description': {'type': 'string', 'required': False, 'empty': False},
    'tags': {'type': 'string', 'required': False, 'empty': False},
    'allergens': {'type': 'string', 'required': False, 'empty': False},
    'prep_time': {'type': 'float', 'required': False, 'empty': False},
    'prep_time_unit': {'type': 'string', 'required': False, 'empty': False},
    'difficulty': {'type': 'string', 'required': False, 'empty': False}
}


create_weekly_menu = {
    'for_week': {'type': 'datetime', 'required': True, 'coerce': convert_date},
    'recipes': {
        'required': True,
        'type': 'list',
        'schema': {
            'type': 'dict',
            'schema': {
                'recipe_id': {'type': 'integer', 'required': True, 'empty': False},
            }
        }
    }
}


update_weekly_menu = {
    'recipes': {
        'required': True,
        'type': 'list',
        'schema': {
            'type': 'dict',
            'schema': {
                'recipe_id': {'type': 'integer', 'required': True, 'empty': False},
            }
        }
    }
}

update_recipe_ingredient = {
    'ingredients': {
        'required': True,
        'type': 'list',
        'schema': create_recipe_ingredient
    }
}
