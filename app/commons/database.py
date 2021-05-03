"""
DB functions.

Include model declaration and other db functions
"""
import datetime
from peewee import *
from app.config import FlaskConfig


def get_db_driver(db_choice: str = 'postgres') -> Database:
    """
    Returns proper db driver.

    This is good for testing in pipeline since
    we can use sqlite if no db instance is available.

    :param db_choice:
    :return:
    """
    if db_choice == 'sqlite':
        return SqliteDatabase('FlaskConfig.DB_NAME', pragmas={
            'journal_mode': 'wal',
            'cache_size': -1024 * 64})
    elif db_choice == 'mysql':
        return MySQLDatabase(
            FlaskConfig.DB_NAME,
            user=FlaskConfig.DB_USER,
            password=FlaskConfig.DB_PASS,
            host=FlaskConfig.DB_HOST,
            port=FlaskConfig.DB_PORT)

    elif db_choice == 'postgres':
        return PostgresqlDatabase(
            FlaskConfig.DB_NAME,
            user=FlaskConfig.DB_USER,
            password=FlaskConfig.DB_PASS,
            host=FlaskConfig.DB_HOST,
            port=FlaskConfig.DB_PORT)


db = get_db_driver(FlaskConfig.DB_DRIVER)


class Base(Model):
    """Base."""

    class Meta:
        database = db


class WeeklyMenu(Base):
    """WeeklyMenu model."""
    for_week = DateTimeField(null=False)
    created_date = DateTimeField(default=datetime.datetime.now)

    class Meta:
        db_table = 'weekly_menu'


class Recipe(Base):
    """Recipe model."""

    name = CharField(max_length=128, null=False)
    sub_header = CharField(max_length=128, null=False)
    description = TextField(null=False)
    tags = TextField(default='')
    category = TextField(default='')
    allergens = TextField(default='')
    prep_time = FloatField(null=False)
    prep_time_unit = CharField(max_length=64, null=False, default='minutes')
    difficulty = CharField(max_length=64, null=False, default='easy')
    updated_date = DateTimeField(default=datetime.datetime.now)
    created_date = DateTimeField(default=datetime.datetime.now)

    class Meta:
        db_table = 'recipes'

    def save(self, *args, **kwargs):
        self.updated_date = datetime.datetime.now()
        return super(Recipe, self).save(*args, **kwargs)


class WeeklyMenuRecipe(Base):
    """Instruction model."""
    weekly_menu = ForeignKeyField(WeeklyMenu, backref='recipes', on_delete='CASCADE')
    recipe = ForeignKeyField(Recipe, backref='weekly_menus', on_delete='CASCADE')
    created_date = DateTimeField(default=datetime.datetime.now)

    class Meta:
        db_table = 'weekly_menu_recipe'
        indexes = (
            (('weekly_menu', 'recipe'), True),
        )


class Ingredient(Base):
    """Ingredient model."""
    name = CharField(max_length=64, null=False)
    measure_unit = CharField(max_length=64, null=True, default='')
    updated_date = DateTimeField(default=datetime.datetime.now)
    created_date = DateTimeField(default=datetime.datetime.now)

    class Meta:
        db_table = 'ingredients'

    def save(self, *args, **kwargs):
        self.updated_date = datetime.datetime.now()
        return super(Ingredient, self).save(*args, **kwargs)


class RecipeInstruction(Base):
    """Instruction model."""
    recipe = ForeignKeyField(Recipe, backref='instruction_list', on_delete='CASCADE')
    sequence = IntegerField(null=False)
    details = TextField(null=False)
    updated_date = DateTimeField(default=datetime.datetime.now)
    created_date = DateTimeField(default=datetime.datetime.now)

    class Meta:
        db_table = 'recipe_instructions'

    def save(self, *args, **kwargs):
        self.updated_date = datetime.datetime.now()
        return super(RecipeInstruction, self).save(*args, **kwargs)


class RecipeNutrition(Base):
    """RecipeNutrition model."""
    recipe = ForeignKeyField(Recipe, backref='nutrition_list', on_delete='CASCADE')
    label = CharField(max_length=64, null=False)
    value = FloatField(null=False)
    measure_unit = CharField(max_length=64, null=False, default='g')
    updated_date = DateTimeField(default=datetime.datetime.now)
    created_date = DateTimeField(default=datetime.datetime.now)

    class Meta:
        db_table = 'recipe_nutrition'

    def save(self, *args, **kwargs):
        self.updated_date = datetime.datetime.now()
        return super(RecipeNutrition, self).save(*args, **kwargs)


class RecipeIngredient(Base):
    """RecipeIngredient model."""
    recipe = ForeignKeyField(Recipe, backref='ingredient_list', on_delete='CASCADE')
    ingredient = ForeignKeyField(Ingredient, backref='ingredient_details', on_delete='CASCADE')
    amount_for_two = FloatField(null=False)
    amount_for_four = FloatField()
    included_in_delivery = BooleanField(default=True)
    updated_date = DateTimeField(default=datetime.datetime.now)
    created_date = DateTimeField(default=datetime.datetime.now)

    class Meta:
        db_table = 'recipe_ingredients'

    def save(self, *args, **kwargs):
        self.updated_date = datetime.datetime.now()
        return super(RecipeIngredient, self).save(*args, **kwargs)


def create_tables():
    """Creates all table."""
    with db:
        db.create_tables([
            Ingredient, RecipeIngredient, Recipe,
            RecipeNutrition, RecipeInstruction,
            WeeklyMenuRecipe, WeeklyMenu
        ])
