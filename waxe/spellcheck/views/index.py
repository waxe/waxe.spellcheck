from pyramid.view import view_config
import pyramid.httpexceptions as exc
from waxe.core.views.base import BaseView
import pyramid_logging
from enchant.checker import SpellChecker
import enchant

log = pyramid_logging.getLogger(__name__)


class SpellcheckView(BaseView):

    @view_config(route_name='spellcheck_json')
    def spellcheck(self):
        text = self.request.GET.get('text')
        lang = self.request.GET.get('lang')

        if not lang or not text:
            raise exc.HTTPClientError('Missing parameters!')

        chkr = SpellChecker(lang, text)
        lis = []
        for err in chkr:
            lis += [{
                'word': err.word,
                'position': err.wordpos,
                'suggestions': chkr.suggest(err.word),
            }]
        return lis

    @view_config(route_name='suggest_json')
    def suggest(self):
        word = self.request.GET.get('word')
        lang = self.request.GET.get('lang')

        if not lang or not word:
            raise exc.HTTPClientError('Missing parameters!')

        d = enchant.Dict(lang)
        # Perhaps test the word is invalid?
        return d.suggest(word)


def includeme(config):
    config.add_route('spellcheck_json', '/spellcheck.json')
    config.add_route('suggest_json', '/suggest.json')
    config.scan(__name__)
