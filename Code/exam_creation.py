from random import choice
from Code.general_helpers import (
    compile_and_clean,
    generate_exam_id,
    random_subset_sum,
    get_final_questions,
    ASSETS_FOLDER,
    EXAMS_FOLDER,
)
from Code.questionbank import QuestionBank

TOTAL_EXAM_PTS = 100


def construct_random_exam(filename: str, questions: list, exam_id: str) -> str:
    """Write the selected questions in a LaTeX file.

    Parameters
    ----------
    filename: str
        Path to the file.
    questions: list
        List of questions.
    exam_id: str
        ID of the exam.

    Returns
    ----------
    str
        Name of the exam file.
    """
    # shuffle(questions)
    with open(filename, "w", encoding="utf-8") as f:
        for q in questions:
            f.write(q + "\n")
    return exam_id + "-" + generate_exam_id() + ".tex"


def generate_random_exam(is_midterm: bool, nb_q: int, nb_qm: int = 0) -> None:
    """Procedure called to generate an exam.

    Parameters
    ----------
    is_midterm: bool
        Boolean to indicate whether or not the exam is a midterm.
    nb_q: int
        Total number of questions to write.
    nb_qm: int
        Number of questions from first part in a final exam, default value 0.
    """
    if is_midterm:
        exam_id = "midterm"
        exam_points = TOTAL_EXAM_PTS
    else:
        exam_id = "final"
        nb_qf = nb_q
        nb_q = nb_qm
        exam_points = choice(list(range(nb_q * 10, nb_q * 20 + 1)))

    questions = []
    # Normal procedure for midterm exam generation
    if nb_q > 0:
        mid_questions = QuestionBank(ASSETS_FOLDER / "midterm-questions.tex")
        rand_pts = random_subset_sum(
            mid_questions.add_question_points(), exam_points, nb_q
        )
        questions += get_final_questions(mid_questions.questions, rand_pts)

    # Supplementary procedure for final exam generation
    if not is_midterm:
        fin_questions = QuestionBank(ASSETS_FOLDER / "final-questions.tex")
        rand_pts_f = random_subset_sum(
            fin_questions.add_question_points(),
            TOTAL_EXAM_PTS - exam_points,
            nb_qf - nb_qm,
        )
        questions += get_final_questions(fin_questions.questions, rand_pts_f)

    exam_filename = construct_random_exam(EXAMS_FOLDER / "test.tex", questions, exam_id)
    compile_and_clean(
        exam_filename, exam_id + "-template_" + str(len(questions)) + ".tex"
    )
