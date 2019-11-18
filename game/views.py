from django.shortcuts import render
from django.http import HttpResponse
from game.models import Player, Board
from django.urls import reverse_lazy
from django.template import loader
from django.views.generic.edit import CreateView, UpdateView
import json

# Create your views here.

#def index(request):
#    return HttpResponse("Hello World!")

#def get_board(request):
#    board = Board.objects.filter(tag=0)
#    return HttpResponse("This board has " + str(board[0].rows) + " rows and " + str(board[0].cols) + " cols.")
   # return HttpResponse("This board has %(rows) rows and %(cols) cols." % {'rows':str(board[0].rows), 'cols':str(board[0].cols)})

def get_board_json(request):
    boardQuery = Board.objects.filter(tag=0)
    board = boardQuery[0]
    players = Player.objects.all()
    boardArr = [['_' for x in range(board.cols)] for y in range(board.rows)]
    boardArr[players[0].row][players[0].col] = players[0].tag
    boardArr[players[1].row][players[1].col] = players[1].tag
    s = ""
    for c in range (len(boardArr)):
        for r in range (len(boardArr[0])):
            s += boardArr[c][r] + ' '
        s += "<br />"
    template = loader.get_template('game/game_board.html')
    html = """
        <!DOCTYPE>
        <html lang="en">
        <head>
        <meta charset="utf-8/>
        </head>
            <body>
            """
    htmlEnd = """
            </body>
            </html>
            """
    #return HttpResponse(template.render(s, request))
    return HttpResponse(s)
    #return HttpResponse(json.dumps(boardArr, cls=BoardEncoder))

#class BoardEncoder(json.JSONEncoder):
#    def default(self, obj):
#        s = ""
#        for c in len(obj):
#            for r in len(obj[0]):
#                s += self[c][r]
#            s += '\n'
#        return  { 'board' : s } 

# def get_player(request, id):
#     player = Player.objects.filter(id=id)
#     if (len(player) == 1):
#         return HttpResponse("Player %(id)s is at row %(row)s and col %(col)s" % {'id':player[0].tag, 'row':str(player[0].row), 'col':str(player[0].col)})
#     else:
        # return HttpResponse("No such player")

def get_player_json(request, id):
    player = Player.objects.filter(id=id)
    if (len(player) == 1):
        return HttpResponse(json.dumps(player[0], cls=PlayerEncoder))
    else:
        return HttpResponse("No such player")
    
def get_players(request):
    players = Player.objects.all()
    http =""
    for player in players:
        http += (json.dumps(player, cls=PlayerEncoder)) + "<br />"
    return HttpResponse(http)



class PlayerEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Player):
            return { 'id' : obj.id, 'tag' : obj.tag, 'row' : obj.row, 'col' : obj.col }
        return json.JSONEncoder.default(self, obj)

class PlayerCreate(CreateView):
    model = Player
    fields = '__all__'
    success_url = reverse_lazy('players')

class PlayerUpdate(UpdateView):
    model = Player
    fields = [ 'row', 'col' ]
    success_url = reverse_lazy('players')

