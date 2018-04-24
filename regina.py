setting = { "search_engine" : "duckduckgo" }

question = {"type" : "research_summary", "word_count" : "3", "results" : "", "voice_question" : ""}

answer = {}

def record_voice():
    question["voice_question"] = str(input("Whats your question? "))
    print("voice_question recorded")

def speech_to_text():
    question["question"] = question["voice_question"]
    print("question.soru saves as text format.")

def analysis_question():
    question["texts"] = question["question"].split()
    question["keyword"] = question["texts"][0]
    print("Words analysis done.\nKeyword: %s \nOther words:" % (question["keyword"]))
    question["duration"] = len(question["keyword"])
    for items in question["texts"]:
        print(items)

def search_keyword_on_web():
    # Get data from wikipedia?
    print("Searched %s in %s." % (setting["search_engine"], question["keyword"]))

def save_results():
    results = "Important info: " + str(question["keyword"])
    print("results: %s" % (results))

def calculate_word_count():
    print("Word count of question: %s" % (question["duration"]))
    question["kelime_sayisi"] = question["duration"]


def save_answer():
    question["answer"] = "answer"
    print("Answer saved as txt.")

def text_to_speach():
    answer["ses_answer"] = question["answer"]
    print("Answer saved as voice.")

def read():
    print("answer.ses_answer")

def research_summary():
    input = record_voice()
    speech_to_text()
    analysis_question()
    search_keyword_on_web()
    save_results()
    calculate_word_count()
    save_answer()
    text_to_speach()
    read()

research_summary()
