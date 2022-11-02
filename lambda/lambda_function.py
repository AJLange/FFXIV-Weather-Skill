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



class GetDataApiHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return utils.isApiRequest(handler_input, 'GetDataApi')

    def handle(self):
        '''
        Holding this in place for if I need it later.
        '''

        response = {
            'apiResponse': {
                
            }
        }

        return response




sb = SkillBuilder()

# register request / intent handlers
sb.add_request_handler(GetDataApiHandler())
sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(HelloWorldIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(GetServerNameHandler())
sb.add_request_handler(GetForecastIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(IntentReflectorHandler())
sb.add_request_handler(GetWeatherDataHandler())


# register exception handlers
sb.add_exception_handler(CatchAllExceptionHandler())

# register interceptors
sb.add_global_request_interceptor(LoggingRequestInterceptor())
sb.add_global_response_interceptor(LoggingResponseInterceptor())

lambda_handler = sb.lambda_handler()