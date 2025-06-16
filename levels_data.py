class Level:
    def __init__(self, name, bg_file, tile_names, question, options, correct_answer):
        self.name = name
        self.bg_file = bg_file
        self.tile_names = tile_names
        self.question = question
        self.options = options
        self.correct_answer = correct_answer


levels = [
    Level(
        "Amsterdam",
        "Amsterdam.jpg",
        ["cake", "pizza", "pancake", "candy"],
        "Which city is this?",
        ["Amsterdam", "Barcelona", "Skopje", "Helsinki"],
        "Amsterdam"
    ),
    Level(
        "Barcelona",
        "Barcelona.jpg",
        ["hamburger", "pizza", "pancake", "candy", "salad"],
        "Which city is this?",
        ["Paris", "Barcelona", "Rome", "London"],
        "Barcelona"
    ),
    Level(
        "Budapest",
        "Budapest.jpg",
        ["pizza", "french-fries", "salad", "hamburger", "donut", "candy"],
        "Which city is this?",
        ["Rome", "Paris", "Barcelona", "Budapest"],
        "Budapest"
    ),
    Level(
        "Paris",
        "Paris.jpg",
        ["cake", "croissant", "pancake", "candy", "hamburger", "donut", "salad"],
        "Which city is this?",
        ["Paris", "London", "Rome", "Amsterdam"],
        "Paris"
    ),
    Level(
        "Skopje",
        "Skopje.jpg",
        ["cake", "pizza", "pancake", "french-fries", "hamburger", "donut", "lollipop", "croissant"],
        "Which city is this?",
        ["Prague", "Skopje", "Budapest", "Warsaw"],
        "Skopje"
    ),
    Level(
        "Helsinki",
        "Helsinki.jpg",
        ["cake", "pizza", "pancake", "candy", "lollipop", "donut", "hamburger", "salad", "chocolate-bar"],
        "Which city is this?",
        ["Prague", "Helsinki", "Budapest", "Warsaw"],
        "Helsinki"
    ),
    Level(
        "Lisbon",
        "Lisabon.jpg",
        ["cake", "pizza", "pancake", "candy", "salad", "chocolate-bar", "lollipop", "donut", "croissant",
         "french-fries"],
        "Which city is this?",
        ["Prague", "Helsinki", "Budapest", "Lisbon"],
        "Lisbon"
    ),
    Level(
        "Monaco",
        "Monaco.jpg",
        ["cake", "pizza", "pancake", "candy", "lollipop", "donut", "croissant", "french-fries", "salad",
         "chocolate-bar", "hamburger"],
        "Which city is this?",
        ["Prague", "Helsinki", "Monaco", "Warsaw"],
        "Monaco"
    ),
    Level(
        "Nice",
        "Nice.jpeg",
        ["cake", "pizza", "pancake", "candy", "lollipop", "donut", "croissant", "french-fries", "salad",
         "chocolate-bar", "hamburger", "donut", "taco"],
        "Which city is this?",
        ["Nice", "Helsinki", "Budapest", "Warsaw"],
        "Nice"
    ),
    Level(
        "Belgrade",
        "Belgrade.jpg",
        ["cake", "pizza", "pancake", "candy", "lollipop", "donut", "donut", "croissant", "french-fries", "salad",
         "chocolate-bar", "hamburger", "taco", "sandwich"],
        "Which city is this?",
        ["Prague", "Belgrade", "Budapest", "Warsaw"],
        "Belgrade"
    )
]
