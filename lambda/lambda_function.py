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

from ask_sdk_model import Response

import utils
import weather_data

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class HelloWorldIntentHandler(AbstractRequestHandler):

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Hello! This is the Skywatcher. You can ask me for the weather!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask(speak_output)
                .response
        )

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
                # .ask(speak_output)
                .response
        )



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
            # .ask("add a reprompt if you want to keep the session open for the user to respond")
            .response
        )


class GetForecastIntentHandler(AbstractRequestHandler):
    '''intent to get a weather forecast'''

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_request_type("LaunchRequest")(handler_input) or
                is_intent_name("GetForecastIntent")(handler_input))


    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In GetForecastIntentHandler")

        # get localization data
        data = handler_input.attributes_manager.request_attributes["_"]

        my_forecast = random.choice(data[prompts.WEATHER])
        speech = data[prompts.GET_WEATHER].format(my_forecast)

        handler_input.response_builder.speak(speech).set_card(
            SimpleCard(data[prompts.SKILL_NAME], my_forecast))
        return handler_input.response_builder.response





sb = SkillBuilder()

# register request / intent handlers

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(HelloWorldIntentHandler())
sb.add_request_handler(GetForecastIntentHandler())


lambda_handler = sb.lambda_handler()