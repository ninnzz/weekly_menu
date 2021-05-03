"""Sample logic code."""
from flask import request
from playhouse.shortcuts import model_to_dict
from app.commons.database import db, Ingredient, RecipeIngredient, Recipe
from app.commons.errors import FailedRequest
from app.commons.utils import validate_input
from app.commons.response import json_response
from app.commons.schema import create_ingredient, update_recipe_ingredient, create_ingredients


# Make sure to add the `res` variable when you use the @json_response decorator
@json_response
def add_ingredient(res):
    """
    Add ingredient.

    :param res:
    :return:
    """
    data = validate_input(request.json, create_ingredient)

    # Maybe no need to add atomic() since its single transaction
    try:
        ingredient = Ingredient.create(
            name=data['name'],
            measure_unit=data['measure_unit']
        )
    except BaseException:
        raise FailedRequest(500, 'Failed to add record to db.')

    return res.send({**{'id': ingredient.id}, **data}, 201)


@json_response
def add_ingredients(res):
    """
    Add ingredients.

    :param res:
    :return:
    """
    data = validate_input(request.json, create_ingredients)

    with db.atomic() as transaction:
        try:
            for to_insert in data['ingredients']:
                ingredient = Ingredient.create(**to_insert)
                to_insert['id'] = ingredient.id
        except BaseException:
            transaction.rollback()
            raise FailedRequest(500, 'Failed to add record to db.')

    return res.send({**{'id': ingredient.id}, **data}, 201)


@json_response
def get_ingredient(res, ingredient_id: int):
    """
    Get ingredient.

    :param ingredient_id:
    :param res:
    :return:
    """
    ingredient = Ingredient.select().where(Ingredient.id == ingredient_id)
    if len(ingredient) == 0:
        raise FailedRequest(404, 'Cannot find ingredient.')
    ig = ingredient.dicts()[0]

    return res.send(ig)


@json_response
def update_recipe_ingredients(res, recipe_id: int):
    """
    Update recipe ingredients.

    Accepts a new set of recipe for the weekly menu.

    :param recipe_id:
    :param res:
    :return:
    """
    try:
        recipe = Recipe.select().where(Recipe.id == recipe_id).get()
        return_data = model_to_dict(recipe)
    except Recipe.DoesNotExist:
        raise FailedRequest(404, 'Cannot find recipe.')

    data = validate_input(request.json, update_recipe_ingredient)

    to_delete = []
    with db.atomic() as transaction:
        try:
            # TODO
            # Refactor
            query = (RecipeIngredient
                     .select(RecipeIngredient, Ingredient)
                     .join(Ingredient, on=(RecipeIngredient.ingredient == Ingredient.id))
                     .where(RecipeIngredient.recipe == recipe.id))

            # Just delete all and overwrite for now
            # not sure about Peewee transaction for delete
            for old_ingredient in query:
                to_delete.append(old_ingredient.id)

            # TODO
            # We can refactor this in a separate function
            # Not sure if peewee object can be passed by reference
            # so we are sure its same object in function though :(
            for ingredient in data['ingredients']:
                # NOTE!!!
                # Maybe add some checking of all ingredient ids?
                # Its not advisable to check every ingredient ids using query
                # But it might be okay since you will not call add recipe every time (assumption)
                # IMPORTANT, if assumption fails, then need to think about checking efficiently.
                try:
                    ingredient_check = Ingredient.select()\
                        .where(Ingredient.id == ingredient['ingredient_id']).get()
                except Recipe.DoesNotExist:
                    raise ValueError('Cannot find some recipe in the list')

                recipe_ingredient = RecipeIngredient.create(
                    recipe=recipe.id,
                    ingredient=ingredient['ingredient_id'],
                    amount_for_two=ingredient['amount_for_two'],
                    amount_for_four=ingredient['amount_for_four'],
                    included_in_delivery=ingredient['included_in_delivery']
                )
                ingredient['id'] = recipe_ingredient.id
                ingredient['name'] = ingredient_check.name
                ingredient['measure_unit'] = ingredient_check.measure_unit

            # Perorm actual delete
            del_query = RecipeIngredient.delete()\
                .where(RecipeIngredient.id << to_delete)    # weird operator -_-
            del_query.execute()

        except ValueError as err:
            transaction.rollback()
            raise FailedRequest(401, str(err))
        except BaseException as err:
            transaction.rollback()
            raise FailedRequest(500, 'Failed to add record to db.')

    return_data['ingredients'] = data['ingredients']
    return res.send(return_data)
