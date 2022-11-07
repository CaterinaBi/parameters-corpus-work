from scraper import Scraper

if __name__ == '__main__':
    bot = Scraper()
    bot.create_dictionary()
    bot.extract_text_from_links()
    bot.extract_questions_from_text()
    bot.create_year_lists()
    bot.save_data_to_json()
    bot.create_mono_question_dictionaries()
    bot.create_century_lists()
    bot.export_data_to_excel()