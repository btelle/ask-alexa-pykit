"""
In this file we specify default event handlers which are then populated into the handler map using metaprogramming
Copyright Anjishnu Kumar 2015
Happy Hacking!
"""
import json
from ask import alexa

db = {}
with open('data.json', 'r') as f:
	db = json.loads(f.read())

def lambda_handler(request_obj, context=None):
    '''
    This is the main function to enter to enter into this code.
    If you are hosting this code on AWS Lambda, this should be the entry point.
    Otherwise your server can hit this code as long as you remember that the
    input 'request_obj' is JSON request converted into a nested python object.
    '''

    metadata = {'user_name' : 'SomeRandomDude'} # add your own metadata to the request using key value pairs
    
    ''' inject user relevant metadata into the request if you want to, here.    
    e.g. Something like : 
    ... metadata = {'user_name' : some_database.query_user_name(request.get_user_id())}

    Then in the handler function you can do something like -
    ... return alexa.create_response('Hello there {}!'.format(request.metadata['user_name']))
    '''
    return alexa.route_request(request_obj, metadata)


@alexa.default_handler()
def default_handler(request):
    return alexa.create_response(message=db['responses']['HelpIntent'])

@alexa.intent_handler("AMAZON.HelpIntent")
def help_handler(request):
    return alexa.create_response(message=db['responses']['HelpIntent'])

@alexa.intent_handler("AMAZON.StopIntent")
def stop_handler(request):
	return alexa.create_response(message="Goodbye.", end_session=True)

@alexa.intent_handler("AMAZON.CancelIntent")
def cancel_handler(request):
	return alexa.create_response(message="Goodbye.", end_session=True)

@alexa.intent_handler("SupportedGames")
def supported_games_handler(request):
	return alexa.create_response(message="These are the games I know: "+", ".join(r.replace('_', ' ') for r in db['games'].keys()))

@alexa.intent_handler("StartingEquipmentInGame")
def starting_equipment_handler(request):
	return generic_question_handler(request, 'starting_equipment')

@alexa.intent_handler("NumberOfPlayers")
def num_players_handler(request):
	return generic_question_handler(request, 'num_players')
	
@alexa.intent_handler("MaxAllowedEquipmentInGame")
def num_players_handler(request):
	return generic_question_handler(request, 'max_equipment')
	
@alexa.intent_handler("WhoStartsGame")
def num_players_handler(request):
	return generic_question_handler(request, 'who_starts_game')

@alexa.intent_handler("WhenGameEnds")
def num_players_handler(request):
	return generic_question_handler(request, 'when_game_ends')

def generic_question_handler(request, question_key):
	try:
		sentence = db['responses'][request.intent_name()]
		game = request.slots[u'Game'].lower().replace(' ', '_')
		
		try:
			type = request.slots[u'Type'].lower().replace(' ', '_')
		except KeyError:
			type = None
		
		if u'Followup' not in request.slots or not request.slots[u'Followup']:
			if isinstance(db['games'][game][question_key], unicode):
				answer = db['games'][game][question_key]
				ret = alexa.create_response(message=sentence % ({'answer': answer, 'game': request.slots[u'Game']}), end_session=True)
			elif isinstance(db['games'][game][question_key][type], unicode):
				answer = db['games'][game][question_key][type]
				ret = alexa.create_response(message=sentence % ({'answer': answer, 'game': request.slots[u'Game'], 'type': request.slots[u'Type']}), end_session=True)
			else:
				question = db['games'][game][question_key][type]['follow-up']['question']
				ret = alexa.create_response(question, end_session=False)
		else:
			game = request.session[u'PreviousIntentGame'].lower().replace(' ', '_')
			type = request.session[u'PreviousIntentType'].lower().replace(' ', '_')
			
			answer = db['games'][game][question_key][type]['follow-up']['answers'][request.slots[u'Followup']]
			ret = alexa.create_response(message=sentence % ({'answer': answer, 'game': request.session[u'PreviousIntentGame'], 'type': request.session[u'PreviousIntentType']}), end_session=True)
	except KeyError:
		ret = alexa.create_response(message="I'm sorry, I don't know the answer.", end_session=True)
	except AttributeError:
		ret = alexa.create_response(message="I couldn't understand your question, try again.")
	
	sess = {}
	sess["PreviousIntent"] = request.intent_name()
	sess["PreviousIntentGame"] = request.slots[u'Game']
	try:
		sess["PreviousIntentType"] = request.slots[u'Type']
	except KeyError:
		sess["PreviousIntentType"] = None
	
	request.session = sess
	
	return ret
