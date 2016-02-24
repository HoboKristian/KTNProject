import json

class MessageParser():
    def __init__(self):

        self.possible_responses = {
            'error': self.parse_error,
            'info': self.parse_info,
            'message': self.parse_message,
            'history': self.parse_history
        }

    def parse(self, payload):
        payload = json.loads(payload)

        if payload['response'] in self.possible_responses:
            return self.possible_responses[payload['response']](payload)
        else:
            return
            # Response not valid

    def parse_error(self, payload):
        return {'response': payload['response'], 'content': payload['content']}

    def parse_info(self, payload):
        return {'response': payload['response'], 'content': payload['content']}

    def parse_message(self, payload):
        return {'response': payload['response'], 'sender':payload['sender'], 'content': payload['content']}

    def parse_history(self, payload):
        return {'response': payload['response'], 'content': json.loads(payload['content'])}
