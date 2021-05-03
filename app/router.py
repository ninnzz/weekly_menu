"""Routes."""
from app.api.ingredients import add_ingredient, get_ingredient, update_recipe_ingredients, add_ingredients
from app.api.recipe import add_recipe, get_recipe, update_recipe_only, delete_recipe
from app.api.weekly_menu import add_weekly_menu, get_weekly_menu, delete_weekly_menu, update_weekly_menu_recipe
from flask import Blueprint

router = Blueprint('routes', __name__)

# Everytime you add a new endpoint
# add router rule here
# router.add_url_rule('/foo', 'foo', function1)
# router.add_url_rule('/foo2', 'foo2', function2)
router.add_url_rule('/ingredient', view_func=add_ingredient, methods=['POST'])
router.add_url_rule('/ingredients', view_func=add_ingredients, methods=['POST'])
router.add_url_rule('/ingredient/<ingredient_id>', view_func=get_ingredient, methods=['GET'])

router.add_url_rule('/recipe', view_func=add_recipe, methods=['POST'])
router.add_url_rule('/recipe/<recipe_id>', view_func=get_recipe, methods=['GET'])
router.add_url_rule('/recipe/<recipe_id>', view_func=update_recipe_only, methods=['PUT'])
router.add_url_rule('/recipe/<recipe_id>', view_func=delete_recipe, methods=['DELETE'])
router.add_url_rule('/recipe/<recipe_id>/ingredients', view_func=update_recipe_ingredients, methods=['PUT'])

router.add_url_rule('/weekly_menu', view_func=add_weekly_menu, methods=['POST'])
router.add_url_rule('/weekly_menu/<weekly_menu_id>', view_func=get_weekly_menu, methods=['GET'])
router.add_url_rule('/weekly_menu/<weekly_menu_id>', view_func=update_weekly_menu_recipe, methods=['PUT'])
router.add_url_rule('/weekly_menu/<weekly_menu_id>', view_func=delete_weekly_menu, methods=['DELETE'])
