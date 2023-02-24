import logging
import ask_sdk_core.utils as ask_utils
import json
import prompts
import random

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.dispatch_components import AbstractRequestInterceptor
from ask_sdk_core.dispatch_components import AbstractResponseInterceptor
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_model import Response
from ask_sdk_model.ui import SimpleCard


from ask_sdk_model import Response

import utils
import weather_data

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
location_slot = "location"
location_slot_key = "WEATHER_LOCATION"

class LaunchRequestHandler(AbstractRequestHandler):

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Hello! This is the Skywatcher. You can ask me for the weather!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                #.ask(speak_output)
                .set_should_end_session(False)
                .response
        )


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "The Sky Watcher is designed to help you find the weather in Final Fantasy Fourteen. You can ask for a forecast from any zone in A Realm Reborn for now. For example, try 'What's the weather like in Limsa Lominsa' or any Final Fantasy Fourteen city."

        handler_input.response_builder.speak(speech_text).ask(speech_text).set_card(
            SimpleCard("Hello World", speech_text))
        return handler_input.response_builder.response


class FallbackIntentHandler(AbstractRequestHandler):
    """Handler for Fallback Intent.
    AMAZON.FallbackIntent is only available in en-US locale.
    This handler will not be triggered except in that locale,
    so it is safe to deploy on any locale.
    """

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")

        # get localization data
        data = handler_input.attributes_manager.request_attributes["_"]

        speech = data[prompts.FALLBACK_MESSAGE]
        reprompt = data[prompts.FALLBACK_REPROMPT]
        handler_input.response_builder.speak(speech).ask(reprompt)
        return handler_input.response_builder.response


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Thanks for checking in today! Good-bye and have fun!"
        # Any cleanup logic goes here.

        return handler_input.speak(speak_output).response_builder.set_should_end_session(True).response




class GetForecastIntentHandler(AbstractRequestHandler):
    """Handler for GetForecast"""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_intent_name("GetForecastIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        
        slots = handler_input.request_envelope.request.intent.slots

        loc = slots['location'].value
        
        if loc in slots:
            my_location = slots[location_slot].value
            handler_input.attributes_manager.session_attributes[location_slot_key] = my_location

            speech_text = ("It sounds like you want to get a forecast for the location {}".format(my_location))
        else:
            speech_text = ("I couldn't find the location you specified.")

        handler_input.response_builder.speak(speech_text).ask(speech_text).set_card(
            SimpleCard("Weather Forecast", speech_text))
        return handler_input.response_builder.response


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """

    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Sorry, this is an error message! You're hitting this error because an intent didn't fire correctly."

        return (
            handler_input.response_builder
            .speak(speak_output)
            .ask(speak_output)
            .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or is_intent_name("AMAZON.StopIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "Goodbye!"

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Hello World", speech_text)).set_should_end_session(True)
        return handler_input.response_builder.response


class GetWeatherDataHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return utils.isApiRequest(handler_input, 'GetWeatherInfo')

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        cityNameWithId = utils.getCityNameWithIdFromApiRequestSlots(handler_input)

        if not cityNameWithId:
            # We couldn't match this city value to our slot, we'll return empty and let the response template handle it.
            return {'apiResponse': {}}

        # "Call a service" to get the weather for this location and date.
        weather = weather_data.getWeather(cityNameWithId.id)

        response = {
            'apiResponse': {
                'cityName': cityNameWithId.name,
                'weather': weather
            }
        }

        return response

class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
            .speak(speak_output)
            .set_should_end_session(False)
            # .ask("add a reprompt if you want to keep the session open for the user to respond")
            .response
        )


# *****************************************************************************
# These simple interceptors just log the incoming and outgoing request bodies to assist in debugging.

class LoggingRequestInterceptor(AbstractRequestInterceptor):
    def process(self, handler_input):
        print("Request received: {}".format(handler_input.request_envelope.request))


class LoggingResponseInterceptor(AbstractResponseInterceptor):
    def process(self, handler_input, response):
        print("Response generated: {}".format(response))


sb = SkillBuilder()

# register request / intent handlers

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(GetForecastIntentHandler())
sb.add_request_handler(IntentReflectorHandler())
# register exception handlers
sb.add_exception_handler(CatchAllExceptionHandler())

# register interceptors
sb.add_global_request_interceptor(LoggingRequestInterceptor())
sb.add_global_response_interceptor(LoggingResponseInterceptor())

lambda_handler = sb.lambda_handler()