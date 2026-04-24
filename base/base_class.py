class Base():
    
    def __init__(self, driver):
        self.driver = driver

    # Проверка того, что искомое слово присутствует на странице
    def assert_word(self, word, result):
        value_word = word.text
        assert value_word == result

    # Проверка совпадения текста среди двух локаторов
    def assert_word_locators(self, word, result):
        value_word = word.text
        result_word = result.text
        assert value_word == result_word

    # Проверка на частичное совпадение строки
    def assert_contains_text(self, actual_text, expected_part):
        actual_text = actual_text.text
        assert expected_part in actual_text