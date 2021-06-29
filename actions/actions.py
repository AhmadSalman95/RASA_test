from typing import Any, Text, Dict, List, Optional
# from rasa.core.events import Event
from rasa_sdk import Action, Tracker, ActionExecutionRejection
from rasa_sdk.executor import CollectingDispatcher
import re
from rasa_sdk.events import SlotSet, EventType, SessionStarted, ActionExecuted, UserUtteranceReverted
from rasa_sdk.forms import FormAction, REQUESTED_SLOT, FormValidationAction
from rasa_sdk.types import DomainDict
from langdetect import detect

# this package helpful to sends emails
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

#this package helpful to connect DB for check email
import sys
sys.path.append("/home/ahmad/Desktop/RASAFULLPROJECTPYTHON/RASA_TEXT_FAQ/actions/")
from connectionDB import *
#this package helpfal to connect to mangeEnginAPI for open ticket
from API import *
from run_model_classification import *
from IDGroupOfProblem import *
import logging

# #############################################
# site take the site variable and return the website or twitter account
def getsite(text):
    if (text == "website") or (text == "موقع") or (text == "الرابط") or (text == "link"):
        site = "psau.edu.sa"
    elif (text == "twitter") or (text == "التويتر") or (text == "تويتر") or (text == "بتويتر"):
        site = "https://twitter.com/@itdl_psau"
    else:
        site = "psau.edu.sa"
    return site


# this class to detect any site the customer need

class ActionSite(Action):
    def name(self) -> Text:
        return "action_site"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # site= getSite(tracker.latest_message['text'])
        site = getsite(tracker.get_slot("site"))
        dispatcher.utter_message(text=site)
        return []


# this class detect the languge(ar or en) from the first massage from the user and put in lang slot
class ActionDetectLang(Action):
    def name(self) -> Text:
        return "action_detect_lang"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        massage = tracker.latest_message.get('text')
        if detect(massage) == "ar":
            lan = "ar"
        else:
            lan = "en"

        return [SlotSet("lang", lan)]


############################################################################################################
# class if you want MappingPolicy is running with add triggers in domain.yml=>intents
# class ActionRoboHistory(Action):
#     def name(self):
#         return "action_robo_history"
#     def run(self, dispatcher,tracker,domain):
#         dispatcher.utter_template("utter_bot_history",tracker)
#         return [UserUtteranceReverted()]
############################################################################################################
###############################################################################################
# def validate(
#         self,
#         dispatcher: "CollectingDispatcher",
#         tracker: "Tracker",
#         domain: Dict[Text, Any],
# ) -> List[Dict]:
#     slot_values = self.extract_other_slots(dispatcher, tracker, domain)
#     slot_to_fill = tracker.get_slot(REQUESTED_SLOT)
#
#     if slot_to_fill:
#         slot_values.update(self.extract_requested_slot(dispatcher, tracker, domain))
#         if not slot_values:
#             lang = tracker.get_slot("lang")
#             if lang == "eng":
#                 dispatcher.utter_message(text="please repeat again")
#             else:
#                 dispatcher.utter_message(text="الرجاء ادخال مرة اخرى")
#             raise ActionExecutionRejection(self.name(),
#                                            "form,failed to validateSlot {0} with action {1}".format(slot_to_fill,
#                                                                                                     self.name()))
#
#     for slot, value in slot_values.items():
#         if slot == 'name':
#             name, massage = name_test(value)
#             if name is None:
#                 slot_values[slot] = None
#                 dispatcher.utter_message(text=massage)
#             else:
#                 slot_values[slot] = value
#                 dispatcher.utter_message(text=massage)
#         elif slot == 'phone':
#             phone, massage = phone_test(value)
#             if phone is None:
#                 slot_values[slot] = None
#                 dispatcher.utter_message(text=massage)
#             else:
#                 slot_values[slot] = phone
#                 dispatcher.utter_message(text=massage)
#         elif slot == "email":
#             email, massage = email_test(value)
#             if email is None:
#                 slot_values[slot] = None
#                 dispatcher.utter_message(text=massage)
#             else:
#                 slot_values[slot] = email
#                 dispatcher.utter_message(text=massage)
#         elif slot == "problem":
#             problem, massage = problem_test(value)
#             if problem is None:
#                 slot_values[slot] = None
#                 dispatcher.utter_message(text=massage)
#             else:
#                 slot_values[slot] = problem
#                 dispatcher.utter_message(text=massage)
#     return [SlotSet(slot, value) for slot, value in slot_values.items()]

#####################################################################################################################################

class ActionSessionmassage(Action):
    def name(self) -> Text:
        return "action_start_massage"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        massage1 = "the session started,please begin the conversation"
        massage2 = "دردشة قد بدءت ,الرجاء ابدء بمناقشة."
        massage = "{}.\n\n{}".format(massage1, massage2)
        dispatcher.utter_message(text=massage1)
        dispatcher.utter_message(text=massage2)
        return []


# class ActionSessionStart(Action):
#     def name(self) -> Text:
#         return "action_session_start"
#
#     @staticmethod
#     def fetch_slots(tracker: Tracker) -> List[EventType]:
#         """Collect slots that contain the user's name and phone number."""

#     slots = []
#
#     for key in ("name", "phone_number"):
#         value = tracker.get_slot(key)
#         if value is not None:
#             slots.append(SlotSet(key=key, value=value))
#
#     return slots

# async def run(self,
#               output_channel: "OutputChannel",
#               nlg: "NaturalLanguageGenerator",
#               tracker: "DialogueStateTracker",
#               domain: "Domain"
#               ) -> List[Event]:

#     the session should begin with a `session_started` event
# events = [SessionStarted(metadata=self.metadata)]
#
# any slots that should be carried over should come after the
# `session_started` event
# events.extend(self.fetch_slots(tracker))
# events.append(ActionExecuted("action_session_massage"))

# an `action_listen` should be added at the end as a user message follows
# events.append(ActionExecuted("action_listen"))
#
# return events


#################################################################################
# start FORM

# ask the slots forms
class AskForNameAction(Action):
    def name(self) -> Text:
        return "action_ask_name"

    def run(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        lang = tracker.get_slot("lang")
        if lang == "ar":
            dispatcher.utter_message(text=" من فضلك اخبرني ماهو اسمك الثلاثي")
        else:
            dispatcher.utter_message(text="please tell me what's your full name")

        return []


class AskForProblemAction(Action):
    def name(self) -> Text:
        return "action_ask_problem"

    def run(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        lang = tracker.get_slot("lang")
        if lang == "ar":
            dispatcher.utter_message(text="من فضلك اخيرني ما هي مشكلتك")
        else:
            dispatcher.utter_message(text="please tell me what's your problem")

        return []


class AskForEmailAction(Action):
    def name(self) -> Text:
        return "action_ask_email"

    def run(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        lang = tracker.get_slot("lang")
        if lang == "ar":
            dispatcher.utter_message(text=" من فضلك اخبرني ماهو ايميلك الجامعي")
        else:
            dispatcher.utter_message(text="please tell me what's your University email...")

        return []


class AskForPhoneAction(Action):
    def name(self) -> Text:
        return "action_ask_phone"

    def run(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        lang = tracker.get_slot("lang")
        if lang == "ar":
            dispatcher.utter_message(text="من فضلك اخبرني ماهو رقم تلفونك")
        else:
            dispatcher.utter_message(text="please tell me what's your phone number")

        return []


# form to collect the all information

# this function to check the name
def name_test(name,lang):
    if lang == 'ar':
        name_regex = "(([^(\'u0600'-\'u06ff'\'u0750'-\'u077f'\'ufb50'-\'ufbc1'\'ufbd3'-\'ufd3f'\'ufd50'-\'ufd8f'\'ufd50'-\'ufd8f'\'ufe70'-\'ufefc'\'uFDF0'-\'uFDFD')(\s)?]{2,25}(\s)?){4,5})"
        nameRegex = re.fullmatch(name_regex,name)
        if nameRegex is None:
            name = None
            massage = "!لم تدخل اسمك الثلاثي بشكل الصحيح"
        else:
            massage ="تم حفظ اسمك: {}".format(name)
    else:
        name_regex = "^((?:\S+\s+){2,4}\S+)"
        nameRegex = re.fullmatch(name_regex,name)
        if nameRegex is None:
            name = None
            massage = " Please enter your full name correctly!"
        else:
            massage ="your name save: {}".format(name)
    return name, massage


# this function to check the email
def email_test(email,lang):
    # emailRegex = re.search('^([a-zA-Z0-9_\\-\\.]+)@([a-zA-Z0-9_\\-\\.]+)\\.([a-zA-Z]{2,5})$', email)
    email_regex = "^([a-zA-Z0-9_\\-\\.]+)@(psau.edu.sa)$"
    emailRegex = re.fullmatch(email_regex,email)
    if emailRegex is None:
        email = None        
        if lang =='ar':
            massage = " !لم تدخل ايميلك الجامعي بشكل الصحيح"
        else:
            massage = " Please enter your university email correctly!"
    else:
        email_check_DB = checkEmail(email)
        if email_check_DB:
            email = emailRegex.string
            if lang == "ar":
                massage = "تم حفظ ايميلك : {}".format(email)
            else:
                massage = "your email save:{}".format(email)
        else:
            email = None        
            if lang =='ar':
                massage = " !لم تدخل ايميلك الجامعي بشكل الصحيح"
            else:
                massage = " Please enter your university email correctly!"
    return email, massage


# this function to check the phone
def phone_test(phone,lang):
    phoneRegex = re.search('^(009665|9665|05|5|\+966)([593076418])([0-9]{7})$', str(phone))
    if phoneRegex is None:
        phone = None
        if lang == "ar":
            massage = "!لم تدخل رقم جوالك بشكل الصحيح"
        else:
            massage = " Please enter your mobile phone correctly!"
    else:
        phone = phoneRegex.string
        if lang == "ar":
            massage = "تم حفظ رقمك : {}".format(phone)
        else:
            massage = "your phone save:{}".format(phone)
    return phone, massage


# this function to check the problem
def problem_test(problem,lang):
    if problem is None:
        if lang == 'ar':
            massage = "!لم تدخل مشكلتك بشكل الصحيح"
        else:
            massage = "Please enter your problem correctly!"
    else:
        if lang == 'ar':
            massage = "تم حفظ مشكلتك :{}".format(problem)
        else:
            massage = "we save your problem:{}".format(problem)
    return problem, massage




def send_email(massage):
    my_address = ''
    password = ''
    user_email = ''
    # this smtp for outlook
    # s=smtplib.SMTP(host='smtp-mail.outlook.com',port=587)
    s = smtplib.SMTP(host='smtp.gmail.com', port=587)
    s.starttls()
    s.login(my_address, password)
    msg = MIMEMultipart()
    msg['From'] = my_address
    msg['To'] = user_email
    msg['Subject'] = "test chatbot"
    msg.attach(MIMEText(massage, 'plain'))
    s.send_message(msg)
    del msg
    s.quit()


# this class to collect the information of user (name,phone,email,problem)
# the response language detect from lang slot
class ValidateInformationForm(FormValidationAction):
    # return the name
    def name(self) -> Text:
        return "validate_information_form"

    # required slots to fill
    async def required_slots(
            self,
            slots_mapped_in_domain: List[Text],
            dispatcher: "CollectingDispatcher",
            tracker: "Tracker",
            domain: "DomainDict",
    ) -> Optional[List[Text]]:
        return slots_mapped_in_domain

    # this function to validate the request slot
    def validate_name(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate name value."""
        lang = tracker.get_slot("lang")
        if not slot_value:
            if lang == "eng":
                dispatcher.utter_message(text="please repeat again")
            else:
                dispatcher.utter_message(text="الرجاء ادخال مرة اخرى")
            raise ActionExecutionRejection(self.name(),
                                           "form,failed to validateSlot {0} with action {1}".format(slot_value,
                                                                                                    self.name()))
        name, massage = name_test(slot_value,lang)
        if name is None:
            dispatcher.utter_message(text=massage)
            return {"name": None}
        else:
            dispatcher.utter_message(text=massage)
            return {"name": slot_value}

    def validate_problem(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate problem value."""
        lang = tracker.get_slot("lang")
        if not slot_value:
            if lang == "eng":
                dispatcher.utter_message(text="please repeat again")
            else:
                dispatcher.utter_message(text="الرجاء ادخال مرة اخرى")
            raise ActionExecutionRejection(self.name(),
                                           "form,failed to validateSlot {0} with action {1}".format(slot_value,
                                                                                                    self.name()))
        name, massage = problem_test(slot_value,lang)
        if name is None:
            dispatcher.utter_message(text=massage)
            return {"problem": None}
        else:
            dispatcher.utter_message(text=massage)
            return {"problem": slot_value}

    def validate_email(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate email value."""
        lang = tracker.get_slot("lang")
        if not slot_value:
            if lang == "eng":
                dispatcher.utter_message(text="please repeat again")
            else:
                dispatcher.utter_message(text="الرجاء ادخال مرة اخرى")
            raise ActionExecutionRejection(self.name(),
                                           "form,failed to validateSlot {0} with action {1}".format(slot_value,
                                                                                                    self.name()))
        name, massage = email_test(slot_value,lang)
        if name is None:
            dispatcher.utter_message(text=massage)
            return {"email": None}
        else:
            dispatcher.utter_message(text=massage)
            return {"email": slot_value}

    def validate_phone(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate phone value."""
        lang = tracker.get_slot("lang")
        if not slot_value:
            if lang == "eng":
                dispatcher.utter_message(text="please repeat again")
            else:
                dispatcher.utter_message(text="الرجاء ادخال مرة اخرى")
            raise ActionExecutionRejection(self.name(),
                                           "form,failed to validateSlot {0} with action {1}".format(slot_value,
                                                                                                    self.name()))
        name, massage = phone_test(slot_value,lang)
        if name is None:
            dispatcher.utter_message(text=massage)
            return {"phone": None}
        else:
            dispatcher.utter_message(text=massage)
            return {"phone": slot_value}
    

class submitForm(Action):
    def name(self) -> Text:
        return "action_finish_form"

    def run(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        lang = tracker.get_slot("lang")
        if lang == "ar":
            name = tracker.get_slot("name")
            problem = tracker.get_slot("problem")
            email = tracker.get_slot("email")
            phone = tracker.get_slot("phone")
            massage = "اسمك : {} \n ايميلك : {} \n رقم تلفونك : {} \n مشكلتك : {} ".format(name, email, phone,
                                                                                           problem)
        else:
            name = tracker.get_slot("name")
            problem = tracker.get_slot("problem")
            email = tracker.get_slot("email")
            phone = tracker.get_slot("phone")
            massage = " your name : {}\n your email : {}\n your phone : {}\n your problem : {}".format(name, email, phone,
                                                                                                   problem)
        
        dispatcher.utter_message(text=massage)
        return []


class ActionExchangeSlots(Action):
    def name(self) -> Text:
        return "ask_exchange_slots"

    def run(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        lang = tracker.get_slot("lang")
        if lang == "ar":
            massage = "هل تريد تعديل طلبك "
            buttons = [{'title': 'نعم',
                        'payload': '/affirm_ask_exchange_slots'},
                       {'title': 'لا',
                        'payload': '/no_ask_exchange_slots'}]
            dispatcher.utter_message(text=massage, buttons=buttons)
        else:
            massage = "do you want change any variables in your ticket "
            buttons = [{'title': 'yes',
                        'payload': '/affirm_ask_exchange_slots'},
                       {'title': 'no',
                        'payload': '/no_ask_exchange_slots'}]
            dispatcher.utter_message(text=massage, buttons=buttons)
        return []


class ActionExchangeSlots_affirm(Action):
    def name(self) -> Text:
        return "response_ask_exchange_slots"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        last_intent_name = tracker.latest_message['intent']['name']

        if last_intent_name == "affirm_ask_exchange_slots":
            lang = tracker.get_slot("lang")
            if lang == "ar":
                massage = "اي متغير تريد ان تغير ؟ "
                buttons = [{'title': 'اسمك',
                            'payload': '/exchange_name'},
                           {'title': 'رقم تلفونك',
                            'payload': '/exchange_phone'},
                           {'title': 'ايميلك',
                            'payload': '/exchange_email'},
                           {'title': 'مشكلتك',
                            'payload': '/exchange_problem'},
                           {'title': 'لا شيء',
                            'payload': '/nothing'}]
                dispatcher.utter_message(text=massage, buttons=buttons)
            else:
                massage = "any variable you want change ? "
                buttons = [{'title': 'your name',
                            'payload': '/exchange_name'},
                           {'title': 'your phone',
                            'payload': '/exchange_phone'},
                           {'title': 'your email',
                            'payload': '/exchange_email'},
                           {'title': 'your problem',
                            'payload': '/exchange_problem'},
                           {'title': 'nothing',
                            'payload': '/nothing'}
                           ]
                dispatcher.utter_message(text=massage, buttons=buttons)
        else:
            lang = tracker.get_slot("lang")
            email = tracker.get_slot("email")
            name = tracker.get_slot("name")
            problem = tracker.get_slot("problem")
            phone = tracker.get_slot("phone")
            if lang == 'ar':
                problem_class = ClassificationOfProblem(problem)
                subject = "{} problem".format(problem_class)
                # ID_group = IDOfgroup(problem_class)
                ID_group = "1850"
                # m = "subject : {}/problem :{} / email : {} / name : {} / phone : {} / idgroup : {}".format(subject,problem,email,name,phone,ID_group)
                # dispatcher.utter_message(text=m)
                ticket_number = AddRequest(subject,problem,email,name,phone,ID_group)
                massage = "تم حفظ طلبك ,رقم طلبك {}".format(ticket_number)
                dispatcher.utter_message(text=massage)
            else:
                massage = "your ticket has been saved,the ticket number will send to your email"
                dispatcher.utter_message(text=massage)
        return [UserUtteranceReverted()]


class ActionResponseFallback_affirm(Action):
    def name(self) -> Text:
        return "response_exchange_slots"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        last_intent_name = tracker.latest_message['intent']['name']
        if last_intent_name == "exchange_problem":
            return [SlotSet("problem", None)]
        elif last_intent_name == "exchange_email":
            return [SlotSet("email", None)]
        elif last_intent_name == "exchange_phone":
            return [SlotSet("phone", None)]
        elif last_intent_name == "exchange_name":
            return [SlotSet("name", None)]
        else:
            return [UserUtteranceReverted()]


#################################################################################

#################################################################################
# start fallback
# class ActionDefaultFallback(Action):
#     """Executes the fallback action and goes back to the previous state
#     of the dialogue"""
#
#     def name(self) -> Text:
#         # return "action_two_stage_fallback"
#         return "action_default_fallback_chat"
#
#     async def run(
#         self,
#         dispatcher: CollectingDispatcher,
#         tracker: Tracker,
#         domain: Dict[Text, Any],
#     ) -> List[Dict[Text, Any]]:
#         lang = tracker.get_slot("lang")
#         if lang == "ar":
#             dispatcher.utter_message(template="utter_default_ar")
#         else:
#             dispatcher.utter_message(template="utter_default_en")
#
#         # Revert user message which led to fallback.
#         return [UserUtteranceReverted()]


# class ActionDefaultFallback(Action):
#     def name(self) -> Text:
#         # return "action_two_stage_fallback"
#         return "action_default_fallback_chat"
#
#     async def run(
#         self,
#         dispatcher: CollectingDispatcher,
#         tracker: Tracker,
#         domain: Dict[Text, Any],
#     ) -> List[Dict[Text, Any]]:
#         last_intent_name = tracker.latest_message['intent']['name']
#         lang = tracker.get_slot("lang")
#         if lang == "ar":
#             massage = "هل تقصد'{}' ؟".format(last_intent_name)
#             buttons = [{'title': 'yes',
#                         'payload': '/{}'.format(last_intent_name)},
#                        {'title': 'no',
#                         'payload': '/out_of_scope'}]
#             dispatcher.utter_button_message(massage, buttons=buttons)
#             # dispatcher.utter_message(template="utter_default_ar")
#         else:
#             massage = "Did you mean '{}'  we ؟".format(last_intent_name)
#             buttons = [{'title': 'yes',
#                         'payload': '/{}'.format(last_intent_name)},
#                        {'title': 'no',
#                         'payload': '/out_of_scope'}]
#             dispatcher.utter_button_message(massage, buttons=buttons)
#             # dispatcher.utter_message(template="utter_default_en")
#
#         # Revert user message which led to fallback.
#         return [UserUtteranceReverted()]
#         # return []
#
# this tow example for fallback

# class ActionTwoDefaultFallback(Action):
#     number = 0
#     last_intent_name = ""
#
#     def name(self) -> Text:
#         # return "action_two_stage_fallback"
#         # return "action_default_ask_affirmation"
#         return "action_default_fallback_chat"
#
#     async def run(
#             self,
#             dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any],
#     ) -> List[Dict[Text, Any]]:
#         last_intent_name = tracker.latest_message['intent']['name']
#         self.last_intent_name = last_intent_name
#         lang = tracker.get_slot("lang")
#         if self.number == 0:
#             print("the number is in first if in arabic{}".format(self.number))
#             if lang == "ar":
#                 massage = "هل تقصد'{}' ؟".format(last_intent_name)
#                 buttons = [{'title': 'yes',
#                             'payload': '/{}'.format(last_intent_name)},
#                            {'title': 'no',
#                             'payload': '/خارج هذا النطاق'}]
#                 dispatcher.utter_message(massage, buttons=buttons)
#                 self.number = 1
#
#             # dispatcher.utter_message(template="utter_default_ar")
#             else:
#                 print("the number is in first if in english {}".format(self.number))
#                 massage = "Did you mean '{}'  we are ?".format(last_intent_name)
#                 buttons = [{'title': 'yes',
#                             'payload': '/{}'.format(last_intent_name)},
#                            {'title': 'no',
#                             'payload': '/out_of_scope'}]
#
#                 dispatcher.utter_message(text=massage, buttons=buttons)
#                 self.number = 1
#             # dispatcher.utter_message(template="utter_default_en")
#         else:
#             massage = "test number in else {} , {}".format(self.number, self.last_intent_name)
#             m = "utter_".format(self.last_intent_name)
#             print(massage)
#             dispatcher.utter_message(template=m)
#         # Revert user message which led to fallback.
#         return []
#         # return [UserUtteranceReverted()]
# #


class ActionResponseFallback(Action):

    def name(self) -> Text:
        return "response_fallback"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        intent_name = tracker.get_intent_of_latest_message()
        lang = tracker.get_slot("lang")
        if lang == 'ar':
            massage = "ربما تريد ان تخبرني ب {}  ".format(intent_name)
            buttons = [{'title': 'yes',
                        'payload': '/affirm'},
                       {'title': 'no',
                        'payload': '/out_of_scope'}]

            dispatcher.utter_message(text=massage, buttons=buttons)
        else:
            massage = "Did you try enter '{}'  ?".format(intent_name)
            buttons = [{'title': 'yes',
                        'payload': '/affirm'},
                       {'title': 'no',
                        'payload': '/out_of_scope'}]
            dispatcher.utter_message(text=massage, buttons=buttons)
        return [SlotSet("fall_intent", intent_name)]


class ActionResponseFallback_affirm(Action):
    def name(self) -> Text:
        return "response_fallback_utters"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        last_intent_name = tracker.latest_message['intent']['name']
        intent_name = tracker.get_slot("fall_intent")

        if last_intent_name == "affirm":
            massage = "utter_{}".format(intent_name)
            dispatcher.utter_message(template=massage)
        else:
            lang = tracker.get_slot("lang")
            if lang == 'ar':
                massage = "ربما تريد ان تخبرني ب {} \n,انا لا استطيع ان افهمك,هل تستطيع ان توضح اكثر من فضلك ؟ ".format(intent_name)
                dispatcher.utter_message(text=massage)
            else:
                massage = " I can't understand, could you rephrase please ?"
                dispatcher.utter_message(text=massage)
        return [UserUtteranceReverted()]

# ###############################################################################################################################
