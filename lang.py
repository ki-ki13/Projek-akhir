LANGUAGES = {
    'af': 'afrikaans',
    'ar': 'arabic',
    'az': 'azerbaijani',
    'be': 'belarusian',
    'bn': 'bengali',
    'bs': 'bosnian',
    'bg': 'bulgarian',
    'ch_sim': 'chinese (simplified)',
    'ch_tra': 'chinese (traditional)',
    'cs': 'czech',
    'da': 'danish',
    'nl': 'dutch',
    'en': 'english',
    'et': 'estonian',
    'tl': 'filipino',
    'fr': 'french',
    'de': 'german',
    'hu': 'hungarian',
    'hi': 'hindi',
    'is': 'icelandic',
    'id': 'indonesian',
    'ga': 'irish',
    'it': 'italian',
    'ja': 'japanese',
    'kn': 'kannada',
    'ko': 'korean',
    'ku': 'kurdish (kurmanji)',
    'la': 'latin',
    'lv': 'latvian',
    'lt': 'lithuanian',
    'ms': 'malay',
    'mt': 'maltese',
    'mi': 'maori',
    'mr': 'marathi',
    'mn': 'mongolian',
    'ne': 'nepali',
    'no': 'norwegian',
    'fa': 'persian',
    'pl': 'polish',
    'pt': 'portuguese',
    'ro': 'romanian',
    'ru': 'russian',
    'sk': 'slovak',
    'sl': 'slovenian',
    'es': 'spanish',
    'sw': 'swahili',
    'sv': 'swedish',
    'ta': 'tamil',
    'te': 'telugu',
    'th': 'thai',
    'tr': 'turkish',
    'uk': 'ukrainian',
    'ur': 'urdu',
    'ug': 'uyghur',
    'uz': 'uzbek',
    'vi': 'vietnamese',
    'cy': 'welsh'
}

bahasa = {key:value for (value, key) in LANGUAGES.items()}

def cek(language):
  if language != "":
    if language in bahasa:
      return bahasa[language]
    else:
      error = 'bahasa tidak ditemukan'
      return error