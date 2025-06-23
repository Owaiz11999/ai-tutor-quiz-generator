import wikipedia
import random
import nltk
from nltk import sent_tokenize, word_tokenize, pos_tag

nltk.download('punkt', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)

def get_wiki_summary(topic, char_limit=5000):
    try:
        page = wikipedia.page(topic)
        return page.content[:char_limit]
    except Exception as e:
        return "Topic not found or too ambiguous."

def generate_mcqs(text, num_questions=40):
    sentences = sent_tokenize(text)
    questions = []
    used_keywords = set()

    for sentence in sentences:
        words = word_tokenize(sentence)
        tagged = pos_tag(words)
        candidates = [word for word, tag in tagged if tag in ['NN', 'NNS', 'NNP', 'NNPS'] and len(word) > 3 and word.isalpha()]

        if not candidates:
            continue

        keyword = random.choice(candidates)
        if keyword.lower() in used_keywords:
            continue

        blanked = sentence.replace(keyword, "_____")
        if blanked == sentence:
            continue

        questions.append({
            "question": blanked,
            "answer": keyword
        })

        used_keywords.add(keyword.lower())

        if len(questions) >= num_questions:
            break

    return questions

def get_quiz_for_topic(topic, num_questions=40):
    summary = get_wiki_summary(topic)
    questions = generate_mcqs(summary, num_questions=num_questions)
    return {"summary": summary, "questions": questions}
