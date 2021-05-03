"""Sample logic code."""
from flask import request
from playhouse.shortcuts import model_to_dict
from app.commons.database import db, Recipe, RecipeIngredient, Ingredient
from app.commons.errors import FailedRequest
from app.commons.utils import validate_input
from app.commons.response import json_response
from app.commons.schema import create_recipe, update_recipe


# Make sure to add the `res` variable when you use the @json_response decorator
@json_response
def add_recipe(res):
    """
    Add ingredient.

    :param res:
    :return:
    """
    data = validate_input(request.json, create_recipe)

    with db.atomic() as transaction:
        try:
            recipe = Recipe.create(
                name=data['name'],
                sub_header=data['sub_header'],
                description=data['description'],
                tags=data['tags'],
                category=data['category'],
                allergens=data['allergens'],
                prep_time=data['prep_time'],
                prep_time_unit=data['prep_time_unit'],
                difficulty=data['difficulty']
            )

            # Add recipe ingredient
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
        except ValueError as err:
            transaction.rollback()
            raise FailedRequest(401, str(err))
        except BaseException as err:
            print(err)
            transaction.rollback()
            raise FailedRequest(500, 'Failed to add record to db.')

    data['tags'] = data['tags'].split(',')
    return res.send({**{'id': recipe.id}, **data}, 201)


@json_response
def get_recipe(res, recipe_id: int):
    """
    Get ingredient.

    :param recipe_id:
    :param res:
    :return:
    """
    # Maybe add key to recipe.name for search??
    try:
        recipe = Recipe.select().where(Recipe.id == recipe_id).get()
        return_data = model_to_dict(recipe)
    except Recipe.DoesNotExist:
        raise FailedRequest(404, 'Cannot find recipe.')

    # using a backref is just a query, but it wont include the other relation
    # in the ingredients table
    # just query with a join
    query = (RecipeIngredient
             .select(RecipeIngredient, Ingredient)
             .join(Ingredient, on=(RecipeIngredient.ingredient == Ingredient.id))
             .where(RecipeIngredient.recipe == recipe.id))

    return_data['ingredients'] = []
    return_data['tags'] = return_data['tags'].split(',')
    for ingredient in query:
        return_data['ingredients'].append({
            'id': ingredient.id,
            'ingredient_id': ingredient.ingredient.id,
            'name': ingredient.ingredient.name,
            'measure_unit': ingredient.ingredient.measure_unit,
            'amount_for_two': ingredient.amount_for_two,
            'amount_for_four': ingredient.amount_for_four,
            'included_in_delivery': ingredient.included_in_delivery
        })

    return res.send(return_data)


@json_response
def update_recipe_only(res, recipe_id: int):
    """
    Update recipe.

    :param recipe_id:
    :param res:
    :return:
    """
    try:
        recipe = Recipe.select().where(Recipe.id == recipe_id).get()
        return_data = model_to_dict(recipe)
    except Recipe.DoesNotExist:
        raise FailedRequest(404, 'Cannot find recipe.')

    data = validate_input(request.json, update_recipe)

    try:
        Recipe.update(**data).where(Recipe.id == recipe_id).execute()
    except BaseException:
        raise FailedRequest(500, 'Failed to update record in db.')
    return_data.update(data)
    return res.send(return_data)


@json_response
def delete_recipe(res, recipe_id: int):
    """
    Delete recipe.

    :param recipe_id:
    :param res:
    :return:
    """
    try:
        recipe = Recipe.select().where(Recipe.id == recipe_id).get()
    except Recipe.DoesNotExist:
        raise FailedRequest(404, 'Cannot find recipe.')

    try:
        recipe.delete_instance()
    except BaseException:
        raise FailedRequest(500, 'Failed to delete record in db.')

    return res.send({
        'id': recipe_id,
        'deleted': True
    })
