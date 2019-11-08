import json
import requests
from app import current_app
from flask_babel import _


def translate(text, source_language, dest_language):
    if 'MS_TRANSLATOR_KEY' not in current_app.load_json or \
            not current_app.load_json['MS_TRANSLATOR_KEY']:
        return _('Error: the translation service is not configured')
    auth = {'Ocp-Apim-Subscription-Key': current_app.load_json['MS_TRANSLATOR_KEY']}
    request = requests.get('https://api.microsofttranslator.com/v2/Ajax.svc''/Translate?text={}&from={}&to={}'.format(text, source_language, dest_language),
                           headers=auth)
    if request.status_code != 200:
        return _('Error: the translation service failed.')
    return json.loads(request.content.decode('utf-8-sig'))
