from django.test import TestCase
from game.models import Player
import game.constants

# Test cases for player objects

# game.constants contains the integers representing the maximum rows and columns for the game board. 
# They are used for out of bounds (high) tests below
class PlayerTestCase(TestCase):

    # Valid player creation test
    def test_create(self):
        response = self.client.post("/game/player/create/", { 'tag':'T','row':3,'col':7 })
        p = Player.objects.get(tag='T')
        self.assertEqual(p.tag, 'T')
        self.assertEqual(p.row, 3)
        self.assertEqual(p.col, 7)
    
    # Player creation with ne/player/1/ative row test
    def test_out_of_bounds_row_low(self):
        response = self.client.post("/game/player/create/", { 'tag':'U', 'row':-4, 'col':4 })
        self.assertFormError(response, 'form', 'row', 'Out of range')
        try:
            Player.objects.get(tag='U')
            self.fail()
        except Player.DoesNotExist:
            pass

    # Player creation with row out of bounds (high) test
    def test_out_of_bounds_row_high(self):
        response = self.client.post("/game/player/create/", { 'tag':'H', 'row': game.constants.MAX_ROWS, 'col':4 })
        self.assertFormError(response, 'form', 'row', 'Out of range')
        try:
            Player.objects.get(tag='H')
            self.fail()
        except Player.DoesNotExist:
            pass

    # Player creation with negative col test
    def test_out_of_bounds_col_low(self):
        response = self.client.post("/game/player/create/", { 'tag':'C', 'row': 3, 'col':-7 })
        self.assertFormError(response, 'form', 'col', 'Out of range')
        try:
            Player.objects.get(tag='C')
            self.fail()
        except Player.DoesNotExist:
            pass

    # Player creation with col out of bounds (high) test
    def test_out_of_bounds_col_high(self):
        response = self.client.post("/game/player/create/", { 'tag':'D', 'row': 3, 'col':game.constants.MAX_COLS })
        self.assertFormError(response, 'form', 'col', 'Out of range')
        try:
            Player.objects.get(tag='D')
            self.fail()
        except Player.DoesNotExist:
            pass
    
    # Two player creation with duplicate tags test
    def test_duplicate_tags(self):
        self.client.post("/game/player/create/", { 'tag':'G', 'row': 3, 'col':4 })
        response = self.client.post("/game/player/create/", { 'tag':'G', 'row': 5, 'col':7 })
        self.assertFormError(response, 'form', 'tag', 'Tag already taken')
        
        if len(Player.objects.filter(tag='G')) ==1:
            return
        self.fail()
        

    # Max player creation test
    def test_max_players(self):
        self.client.post("/game/player/create/", { 'tag':'A', 'row': 6, 'col':9 })
        self.client.post("/game/player/create/", { 'tag':'B', 'row': 3, 'col':4 })
        response = self.client.post("/game/player/create/", { 'tag':'C', 'row': 4, 'col':8 })
        self.assertFormError(response, 'form', 'tag', 'Max players already made')
        try:
            Player.objects.get(tag='C')
            self.fail()
        except Player.DoesNotExist:
            pass
    
    # Player moving to row that is too far (low)
    def test_moving_to_invalid_row_low(self):
        self.client.post("/game/player/create/", { 'tag':'1', 'row': 5, 'col':5 })
        response = self.client.post("/game/player/1/update/", { 'row': 3, 'col': 5})
        self.assertIn(b'Row too far', response._container[0])
        try:
            Player.objects.get(tag='1', row='3')
            self.fail()
        except Player.DoesNotExist:
            pass

    # Player moving to row that is too far (high)
    def test_moving_to_invalid_row_high(self):
        self.client.post("/game/player/create/", { 'tag':'1', 'row': 5, 'col':5 })
        response = self.client.post("/game/player/1/update/", { 'row': 7, 'col': 5})
        self.assertIn(b'Row too far', response._container[0])
        try:
            Player.objects.get(tag='1', row='7')
            self.fail()
        except Player.DoesNotExist:
            pass

    # Player moving to col that is too far (low)
    def test_moving_to_invalid_col_low(self):
        self.client.post("/game/player/create/", { 'tag':'1', 'row': 5, 'col':5 })
        response = self.client.post("/game/player/1/update/", { 'row': 5, 'col': 3})
        self.assertIn(b'Column too far', response._container[0])
        try:
            Player.objects.get(tag='1', col='3')
            self.fail()
        except Player.DoesNotExist:
            pass

    # Player moving to col that is too far (high)
    def test_moving_to_invalid_col_high(self):
        self.client.post("/game/player/create/", { 'tag':'1', 'row': 5, 'col':5 })
        response = self.client.post("/game/player/1/update/", { 'row': 5, 'col': 7})
        self.assertIn(b'Column too far', response._container[0])
        try:
            Player.objects.get(tag='1', col='7')
            self.fail()
        except Player.DoesNotExist:
            pass