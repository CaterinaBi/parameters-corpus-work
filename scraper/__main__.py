from scraper import Scraper

if __name__ == '__main__':
    bot = Scraper()
    bot.create_dictionary()
    bot.extract_text_from_links()
    bot.extract_questions_from_text()
    bot.create_year_lists()
    bot.save_data_to_json()