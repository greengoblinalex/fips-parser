from pprint import pprint

from src.parsers import FipsParser, text_parser


def main():
    with FipsParser() as fips_parser:
        url_text_map = fips_parser.parse_by_query('Искусственный интеллект в нефтегазе')

    phrases = [
        'искусственный интеллект',
        'Original Equipment Manufacture',
        'диагностика LMDS',
        'sql'
    ]

    for url, text in url_text_map.items():
        print(f'Ссылка на патент: {url}\nНайденные алгоритмы:')
        phrases_found = text_parser.search_phrases_in_text(phrases, text)
        if phrases_found:
            pprint(phrases_found)
        else:
            print('Нет найденных алгоритмов')
        print()


if __name__ == '__main__':
    main()
