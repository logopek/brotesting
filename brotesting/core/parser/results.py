import bs4
from ..models import StudentAnswer, Question, Choice


class ResultParser:
    def parse(self, form: str, user) -> list:
        soup = bs4.BeautifulSoup(form, "html.parser")
        d = []
        for i in soup.find_all("textarea"):
            id, val = self.__parseTextArea(i)
            d.append(StudentAnswer(question = Question.objects.filter(id=id).first(), text_answer = val, user=user))
        for field in soup.find_all("fieldset"):
            id, val = self.__parseInput(field.find_all("input"))
            if val == "True" or val == "False":
                val = True if val == "True" else "False"
                d.append(StudentAnswer(question = Question.objects.filter(id=id).first, tf_answer = val, user=user))
            else:
                d.append(StudentAnswer(question = Question.objects.filter(id=id).first(), selected_choice = Choice.objects.filter(id=val).first(), user=user))
        return d

    @staticmethod
    def __parseInput(inputs):
        id = -1
        id = inputs[0].get("id")[12:-2]
        for input in inputs:
            if input.has_attr("checked"):
                h = input.get("value")
                return int(id), h
    @staticmethod
    def __parseTextArea(input):
        id = -1
        id = input.get("id")[12:]
        return int(id), input.text.rstrip("\n").lstrip("\n")
