#!/usr/bin/python -dOO

import cjson
import urllib2, urllib

languages = {
    'ARABIC' : 'ar',
    'BULGARIAN' : 'bg',
    'CATALAN' : 'ca',
    'CHINESE' : 'zh',
    'CHINESE_SIMPLIFIED' : 'zh-CN',
    'CHINESE_TRADITIONAL' : 'zh-TW',
    'CROATIAN' : 'hr',
    'CZECH' : 'cs',
    'DANISH' : 'da',
    'DUTCH': 'nl',
    'ENGLISH' : 'en',
    'ESTONIAN' : 'et',
    'FILIPINO' : 'tl',
    'FINNISH' : 'fi',
    'FRENCH' : 'fr',
    'GERMAN' : 'de',
    'GREEK' : 'el',
    'HEBREW' : 'iw',
    'HINDI' : 'hi',
    'HUNGARIAN' : 'hu',
    'INDONESIAN' : 'id',
    'ITALIAN' : 'it',
    'JAPANESE' : 'ja',
    'KOREAN' : 'ko',
    'LATVIAN' : 'lv',
    'LITHUANIAN' : 'lt',
    'NORWEGIAN' : 'no',
    'PERSIAN' : 'fa',
    'POLISH' : 'pl',
    'PORTUGUESE' : 'pt-PT',
    'ROMANIAN' : 'ro',
    'RUSSIAN' : 'ru',
    'SERBIAN' : 'sr',
    'SLOVAK' : 'sk',
    'SLOVENIAN' : 'sl',
    'SPANISH' : 'es',
    'SWEDISH' : 'sv',
    'THAI' : 'th',
    'TURKISH' : 'tr',
    'UKRAINIAN' : 'uk',
    'VIETNAMESE' : 'vi',
    'UNKNOWN' : ''
}

def iso2name(iso):
    for key,value in languages.iteritems():
        if value == iso:
            return key;

def name2iso(name):
    for key, value in languages.iteritems():
        if key == name:
            return value;
    

class LanguageDetection:
    def __init__(self):
        pass
    
    def _buildRequest(self, text):
        param = { 'v':'1.0' , 'q':text }
        url = LanguageDetection.host + urllib.urlencode( param )
        request = urllib2.Request(url, headers = {'Referer':Translator.referer} )
        return request

    def detection(self, text):
        r = self._buildRequest( text )
        handle = urllib2.urlopen( r )
        line = handle.readline()
        handle.close()

        response = cjson.decode( line )

        del line, handle,r;
        
        if response['responseStatus'] != 200:
            raise TranslatorException("HTTP Status was not 200", response)
        
        return response['responseData']

    def __call__(self,text):
        return self.detection(text)['language']

    host = 'http://ajax.googleapis.com/ajax/services/language/detect?' 


class Translator:
    def __init__(self, from_lang='de', to_lang='en'):
        self.from_lang= from_lang;
        self.to_lang  = to_lang;

    def _buildRequest(self, to_translate, from_lang, to_lang):
        p = {'q':to_translate, 'langpair': from_lang + '|' + to_lang };
        url = Translator.host + Translator.path +  urllib.urlencode( p )
        request = urllib2.Request(url, headers = { 'Referer' : Translator.referer } )
        return request;

    def translate(self, to_translate):
        req = self._buildRequest( to_translate, self.from_lang, self.to_lang)
        
        handle = urllib2.urlopen(req)
        response = handle.readline()
        handle.close()        
        response = cjson.decode( response )

        if response['responseStatus'] != 200:
            raise TranslatorException("HTTP Status was not 200", response)

        return response['responseData']['translatedText'];

    def __call__(self, trans):
        return self.translate(trans)
    
    referer='http://google.com'
    host='http://ajax.googleapis.com/'
    path='ajax/services/language/translate?v=1.0&'
          

class TranslatorException(Exception):
    def __init__(self, message, response=None):
        self.message = message;
        self.response = response

    def __str__(self):
        if response == None:
            return self.message;
        else:
            return self.message + "\n"  + "The response was: " + self.response
        

if __name__ == '__main__':    
    import sys

    from optparse import OptionParser
    
    op = OptionParser("""%prog -f en -t de [words]
%prog --list-languages
%prog -g [words]
""",
epilog="""
If words are missing the program is read from stdin
"""
)

    op.add_option('-g', '--guess' ,action='store_true',
                  dest = 'guess', default = False,
                  help = 'guess the language from the input')

    op.add_option('-f', '--from', action='store',
                  type='string', dest='from_lang', default ='',
                  help="the source language")
    op.add_option('-t', '--to', action='store',
                  type='string', dest='to_lang', default='',
                  help='the destination language')

    op.add_option('-l','--list-languages', default=False,
                  action='store_true', help='print all avaible lanugages',
                  dest = 'list_languages' )

    op.add_option('','--file', default=None, help='File to be translated',
                  type="string", dest='file');

    
    
    (options, args) = op.parse_args()    

    if options.list_languages:
        for key in languages.iterkeys():
            print  languages[key], '\t\t', key
        sys.exit(0)
		
    if  options.file:
        handle = open(options.file)
        lines = handle.readlines()
        handle.close()
    else:
        lines = ''.join(args)
        if not lines: 
            lines = sys.stdin.readlines();
        
    try:
        if options.guess:
            d = LanguageDetection()
            print iso2name( d( "".join(lines) ) )
        else:
            t = Translator(options.from_lang , options.to_lang)
            print  t( "".join( lines ) )
    except TranslatorException, e:
        print >> sys.stderr, e.message
        print >> sys.stderr, e.response
        



