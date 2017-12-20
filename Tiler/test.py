from deiis.model import Question

if __name__ == '__main__':
    question = Question({'body':'Why are we using Python?', 'ranked': ['1', '2', '3']})
    print question.body
    print question.ranked
