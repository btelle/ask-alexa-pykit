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
    """ The default handler gets invoked if no handler is set for a request type """
    return alexa.create_response(message="Just ask")


@alexa.intent_handler("StartingEquipmentInGame")
def starting_equipment_handler(request):
	try:
		sentence = db['responses'][request.intent_name()]
		
		game = request.slots[u'Game'].lower().replace(' ', '_')
		type = request.slots[u'Type'].lower().replace(' ', '_')
		
		if u'Followup' not in request.slots or not request.slots[u'Followup']:
			if isinstance(db['games'][game]['starting_equipment'][type], unicode):
				answer = db['games'][game]['starting_equipment'][type]
				ret = alexa.create_response(message=sentence % ({'answer': answer, 'game': request.slots[u'Game'], 'type': request.slots[u'Type']}), end_session=True)
			else:
				question = db['games'][game]['starting_equipment'][type]['follow-up']['question']
				ret = alexa.create_response(question, end_session=False)
		else:
			game = request.session[u'PreviousIntentGame'].lower().replace(' ', '_')
			type = request.session[u'PreviousIntentType'].lower().replace(' ', '_')
			
			answer = db['games'][game]['starting_equipment'][type]['follow-up']['answers'][request.slots[u'Followup']]
			ret = alexa.create_response(message=sentence % ({'answer': answer, 'game': request.session[u'PreviousIntentGame'], 'type': request.session[u'PreviousIntentType']}), end_session=True)
	except KeyError:
		ret = alexa.create_response(message="I'm sorry, I don't know the answer.", end_session=True)
	except AttributeError:
		ret = alexa.create_response(message="I couldn't understand your question, try again.")
	
	request.session = {
		"PreviousIntent": "StartingEquipmentInGame",
		"PreviousIntentGame": request.slots[u'Game'],
		"PreviousIntentType": request.slots[u'Type']
	}
	
	return ret

@alexa.intent_handler('GetRecipeIntent')
def get_recipe_intent_handler(request):
    """
    You can insert arbitrary business logic code here    
    """

    # Get variables like userId, slots, intent name etc from the 'Request' object
    ingredient = request.slots["Ingredient"]  # Gets an Ingredient Slot from the Request object.
    
    if ingredient == None:
        return alexa.create_response("Could not find an ingredient!")

    # All manipulations to the request's session object are automatically reflected in the request returned to Amazon.
    # For e.g. This statement adds a new session attribute (automatically returned with the response) storing the
    # Last seen ingredient value in the 'last_ingredient' key. 

    request.session['last_ingredient'] = ingredient # Automatically returned as a sessionAttribute
    
    # Modifying state like this saves us from explicitly having to return Session objects after every response

    # alexa can also build cards which can be sent as part of the response
    card = alexa.create_card(title="GetRecipeIntent activated", subtitle=None,
                             content="asked alexa to find a recipe using {}".format(ingredient))    

    return alexa.create_response("Finding a recipe with the ingredient {}".format(ingredient),
                                 end_session=False, card_obj=card)



@alexa.intent_handler('NextRecipeIntent')
def next_recipe_intent_handler(request):
    """
    You can insert arbitrary business logic code here
    """
    return alexa.create_response(message="Getting Next Recipe ... 123")
