from django.test import TestCase
from accounts.models import User
from django.contrib import auth
from restaurants.models import *
from django.utils import timezone
# from selenium import webdriver

class ModelsTest(TestCase):
    def test_string_accounts_models(self):
        user= User('john','john@email.com', 'johnpass')
        self.assertTrue(isinstance(user, User))
        self.assertEqual(user.__str__(), '@'+user.username)

    def test_category_restaurants_models(self):
        category = Category(name="testkategoria", slug="kategoriaslug")
        self.assertTrue(isinstance(category, Category))
        self.assertEqual(category.__str__(), '@'+category.name)

    def test_restaurant_restaurants_models(self):
        restaurant = Restaurant(name="testrestauracja", address="testadres", updated=timezone.now(), author="testuser", price=1, slug="testrestauracja")
        self.assertTrue(isinstance(restaurant, Restaurant))
        self.assertEqual(restaurant.__str__(), '@'+restaurant.name)

    def test_comment_restaurants_models(self):
        restaurant1 = Restaurant(name="testrestauracja", address="testadres", updated=timezone.now(), author="testuser", price=1, slug="testrestauracja")
        comment = Comment(restaurant=restaurant1, author="testuser", title="comment")
        self.assertTrue(isinstance(comment, Comment))
        self.assertEqual(comment.__str__(), '@'+comment.author+" "+comment.restaurant.name+" "+comment.title)

    def test_favourite_restaurants_models(self):
        restaurant1 = Restaurant(name="testrestauracja", address="testadres", updated=timezone.now(), author="testuser", price=1, slug="testrestauracja")
        fav = FavouriteRestaurants(restaurant=restaurant1, user="testuser")
        self.assertTrue(isinstance(fav,FavouriteRestaurants))
        self.assertEqual(fav.__str__(), '@'+fav.user+" "+fav.restaurant.name)

    def test_rating_restaurants_models(self):
        restaurant1 = Restaurant(name="testrestauracja", address="testadres", updated=timezone.now(), author="testuser", price=1, slug="testrestauracja")
        rating = Rating(restaurant=restaurant1, user="testuser", score=3)
        self.assertTrue(isinstance(rating,Rating))
        self.assertEqual(rating.__str__(), '@'+rating.user+" "+rating.restaurant.name+" "+str(rating.score))

    def test_inforating_restaurants_models(self):
        restaurant1 = Restaurant(name="testrestauracja", address="testadres", updated=timezone.now(), author="testuser", price=1, slug="testrestauracja")
        inforating = InfoRating(restaurant=restaurant1, user="testuser", rate=4)
        self.assertTrue(isinstance(inforating,InfoRating))
        self.assertEqual(inforating.__str__(), '@'+inforating.user+" "+inforating.restaurant.name+" "+str(inforating.rate))

    def test_restaurantscategory_restaurants_models(self):
        restaurant1 = Restaurant(name="testrestauracja", address="testadres", updated=timezone.now(), author="testuser", price=1, slug="testrestauracja")
        category1 = Category(name="testkategoria", slug="kategoriaslug")
        restcategory = RestauratsCategory(restaurant=restaurant1, category=category1)
        self.assertTrue(isinstance(restcategory,RestauratsCategory))
        self.assertEqual(restcategory.__str__(), '@'+restcategory.restaurant.name+" "+str(restcategory.category))

    def test_category_restaurants_models_save(self):
        category = Category(name="testkategoria", slug="kategoriaslug")
        category.save()
        self.assertEqual(category, Category.objects.get(name="testkategoria"))

    def test_restaurant_restaurants_models_save(self):
        restaurant = Restaurant(name="testrestauracja", address="testadres", updated=timezone.now(), author="testuser", price=1, slug="testrestauracja")
        restaurant.save()
        self.assertEqual(restaurant, Restaurant.objects.get(name="testrestauracja"))

    def test_comment_restaurants_models_save(self):
        restaurant1 = Restaurant.objects.create(name="testrestauracja", address="testadres", updated=timezone.now(), author="testuser", price=1, slug="testrestauracja")
        comment = Comment(restaurant=restaurant1, author="testuser", title="comment")
        comment.save()
        self.assertEqual(comment, Comment.objects.get(title="comment"))

    def test_inforating_restaurants_models_save(self):
        restaurant1 = Restaurant.objects.create(name="testrestauracja", address="testadres", updated=timezone.now(), author="testuser", price=1, slug="testrestauracja")
        inforating = InfoRating(restaurant=restaurant1, user="testuser", rate=4)
        inforating.save()
        self.assertEqual(inforating, InfoRating.objects.get(user="testuser"))
