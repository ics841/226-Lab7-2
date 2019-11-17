from django.db import models
from django.core.exceptions import ValidationError
from game import constants

# Create your models here.

def validate_col_range(value):
    if value < 0 or value > constants.MAX_COLS - 1:
        print("Player.objects.all() number: " + str(len(Player.objects.all())))
        raise ValidationError('Out of range',)

def validate_row_range(value):
    if value < 0 or value > constants.MAX_ROWS - 1:
        raise ValidationError('Out of range',)

def validate_unique_tag(value):
    for player in Player.objects.all():
        if player.tag == value:
            raise ValidationError('Tag already taken',)

def validate_max_players(value):
    if len(Player.objects.all()) >= 2:
        raise ValidationError('Max players already made',)

class Player(models.Model):
    tag = models.CharField(max_length=1, validators=[validate_unique_tag, validate_max_players])
    row = models.IntegerField(validators=[validate_row_range])
    col = models.IntegerField(validators=[validate_col_range])

    def __init__(self, *args, **kwargs):
        super(Player, self).__init__(*args, **kwargs)
        self._prev_row = self.row
        self._prev_col = self.col

    def clean(self):
        if self._prev_row != None:
            if abs(self.row - self._prev_row) > 1:
                raise ValidationError('Row too far')
            if abs(self.col - self._prev_col) > 1:
                raise ValidationError('Column too far')


    def __str__(self):
        return self.tag + ' @(' + str(self.row) + ',' + str(self.col) + ')'

class Board(models.Model):
    tag = models.CharField(max_length=1)
    rows = models.IntegerField()
    cols = models.IntegerField()

    def __str__(self):
        return self.tag + ' @(' + str(self.rows) + ',' + str(self.cols) + ')'

