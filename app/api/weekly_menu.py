"""Sample logic code."""
from flask import request
from collections import defaultdict
from playhouse.shortcuts import model_to_dict
from app.commons.database import db, WeeklyMenu, WeeklyMenuRecipe, Recipe
from app.commons.errors import FailedRequest
from app.commons.utils import validate_input
from app.commons.response import json_response
from app.commons.schema import create_weekly_menu, update_weekly_menu


def return_zero():
    """Defaultdict util."""
    return 0


# Make sure to add the `res` variable when you use the @json_response decorator
@json_response
def add_weekly_menu(res):
    """
    Add weekly_menu.

    :param res:
    :return:
    """
    data = validate_input(request.json, create_weekly_menu)

    category_mapping = defaultdict(return_zero)
    with db.atomic() as transaction:
        try:
            weekly_menu = WeeklyMenu.create(
                for_week=data['for_week']
            )

            # Add recipe ingredient
            for recipe in data['recipes']:

                # NOTE!!!
                # Maybe add some checking of all recipe ids?
                # Its not advisable to check every recipe ids using query
                # But it might be okay since you will not call add menu every time (assumption)
                # IMPORTANT, if assumption fails, then need to think about checking efficiently.
                try:
                    recipe_check = Recipe.select().where(Recipe.id == recipe['recipe_id']).get()
                except Recipe.DoesNotExist:
                    raise ValueError('Cannot find some recipe in the list')

                menu_recipe = WeeklyMenuRecipe.create(
                    weekly_menu=weekly_menu.id,
                    recipe=recipe_check
                )
                recipe['id'] = menu_recipe.id
                recipe['recipe_id'] = recipe_check.id
                recipe['name'] = recipe_check.name
                recipe['category'] = recipe_check.category
                category_mapping[recipe_check.category] += 1

        except ValueError as err:
            transaction.rollback()
            raise FailedRequest(401, str(err))
        except BaseException as err:
            transaction.rollback()
            raise FailedRequest(500, 'Failed to add record to db.')
    data['frequency'] = category_mapping
    return res.send({**{'id': weekly_menu.id}, **data}, 201)


@json_response
def get_weekly_menu(res, weekly_menu_id: int):
    """
    Get weekly_menu.

    :param weekly_menu_id:
    :param res:
    :return:
    """
    # Maybe add key to recipe.name for search??
    try:
        weekly_menu = WeeklyMenu.select() \
            .where(WeeklyMenu.id == weekly_menu_id).get()
        return_data = model_to_dict(weekly_menu)
    except WeeklyMenu.DoesNotExist:
        raise FailedRequest(404, 'Cannot find weekly menu.')

    # using a backref is just a query, but it wont include the other relation
    # in the ingredients table
    # just query with a join
    query = (WeeklyMenuRecipe
             .select(WeeklyMenuRecipe, Recipe)
             .join(Recipe, on=(WeeklyMenuRecipe.recipe == Recipe.id))
             .where(WeeklyMenuRecipe.weekly_menu == weekly_menu.id))

    category_mapping = defaultdict(return_zero)
    return_data['recipes'] = []
    for recipe in query:
        category_mapping[recipe.recipe.category] += 1
        return_data['recipes'].append({
            'id': recipe.id,
            'recipe_id': recipe.recipe.id,
            'name': recipe.recipe.name,
            'category': recipe.recipe.category,
            'tags': recipe.recipe.tags.split(','),
            'allergens': recipe.recipe.allergens.split(','),
            'difficulty': recipe.recipe.difficulty,
            'prep_time': recipe.recipe.prep_time,
            'prep_time_unit': recipe.recipe.prep_time_unit
        })
    return_data['frequency'] = category_mapping
    return res.send(return_data)


@json_response
def update_weekly_menu_recipe(res, weekly_menu_id: int):
    """
    Update weekly_menu.

    Accepts a new set of recipe for the weekly menu.

    :param weekly_menu_id:
    :param res:
    :return:
    """
    try:
        weekly_menu = WeeklyMenu.select().where(WeeklyMenu.id == weekly_menu_id).get()
    except WeeklyMenu.DoesNotExist:
        raise FailedRequest(404, 'Cannot find weekly menu.')

    data = validate_input(request.json, update_weekly_menu)

    recipe_ids = [x['recipe_id'] for x in data['recipes']]
    dont_delete = []
    to_delete = []
    with db.atomic() as transaction:
        try:
            query = (WeeklyMenuRecipe
                     .select()
                     .where(WeeklyMenuRecipe.weekly_menu == weekly_menu.id))

            # Forgot to add, but maybe its easier to catch error
            # if I make recipe_id and weekly_menu_id as primary key lol
            for old_recipe in query:
                if old_recipe.recipe.id not in recipe_ids:
                    # NOTE!!!
                    # I am not familiar with how Peewee handles deletes in transaction
                    # Normally, I will just delete this then revert back if something
                    # happens. But I am still learning the nature of "delete" in Peewee
                    to_delete.append(old_recipe.id)
                else:
                    dont_delete.append(old_recipe.recipe.id)

            to_insert = list(set(recipe_ids) - set(dont_delete))

            recipe_return = []
            category_mapping = defaultdict(return_zero)
            for recipe_id in to_insert:
                try:
                    recipe_check = Recipe.select().where(Recipe.id == recipe_id).get()
                except Recipe.DoesNotExist:
                    raise ValueError('Cannot find some recipe in the list')

                menu_recipe = WeeklyMenuRecipe.create(
                    weekly_menu=weekly_menu.id,
                    recipe=recipe_check
                )
                recipe_return.append({
                    'id': menu_recipe.id,
                    'recipe_id': recipe_id,
                    'name': recipe_check.name,
                    'category': recipe_check.category,
                })
                category_mapping[recipe_check.category] += 1

            # Perorm actual delete
            del_query = WeeklyMenuRecipe.delete().where(WeeklyMenuRecipe.id << to_delete)
            del_query.execute()

        except ValueError as err:
            transaction.rollback()
            raise FailedRequest(401, str(err))
        except BaseException as err:
            transaction.rollback()
            raise FailedRequest(500, 'Failed to add record to db.')

    return res.send({})


@json_response
def delete_weekly_menu(res, weekly_menu_id: int):
    """
    Delete recipe.

    :param weekly_menu_id:
    :param res:
    :return:
    """
    try:
        weekly_menu = WeeklyMenu.select().where(WeeklyMenu.id == weekly_menu_id).get()
    except WeeklyMenu.DoesNotExist:
        raise FailedRequest(404, 'Cannot find weekly menu.')

    try:
        weekly_menu.delete_instance()
    except BaseException:
        raise FailedRequest(500, 'Failed to delete record in db.')

    return res.send({
        'id': weekly_menu_id,
        'deleted': True
    })
