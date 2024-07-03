from pathlib import Path
import re


QT_FORMAT_REGEX = r"% QUESTION \d+\n"  # question separator
PT_FORMAT_REGEX = r"\[\d+\]"  # any number in brackets (to recover question points)


def get_question_collection(questions_file: Path) -> dict:
    """Recover the entire list of questions from the LaTeX file.

    Parameters
    ----------
    questions_file: str
        Path to the questions file.

    Returns
    ----------
    dict
        A dictionary of questions.
    """
    questions = {}
    with open(questions_file, "r", encoding="utf-8") as f:
        # Separate each question and store them into an array
        for i, el in enumerate(re.split(QT_FORMAT_REGEX, f.read())[1:]):
            questions[i] = [el]
    return questions


class QuestionBank:
    """Simple class to convert a list of questions into a dictionary."""

    def __init__(self, questions_file: Path):
        self.questions = get_question_collection(questions_file)

    def add_question_points(self) -> list:
        """Get total points for each question.

        Returns
        ----------
        list
            A list of total points for each question.
        """
        total_points = []
        pattern = re.compile(PT_FORMAT_REGEX)
        for question in self.questions.values():
            points = 0
            # Sum up points of all subquestions if any
            if question and isinstance(question, list):
                for re_match in re.finditer(pattern, question[0]):
                    points += int(re_match.group()[1:-1])
                question.append(points)
                total_points.append(points)
        return total_points
