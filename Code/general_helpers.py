import os
from itertools import combinations
from random import choice, shuffle
from string import ascii_letters, digits
from subprocess import call
from time import perf_counter
from pathlib import Path

ROOT_FOLDER = Path(__file__).resolve().parent.parent
ASSETS_FOLDER = ROOT_FOLDER / "Assets/"
EXAMS_FOLDER = ROOT_FOLDER / "Exams/"


def generate_exam_id() -> str:
    """Generates a random exam ID.

    Returns
    ----------
    str
        A random string of 12 characters.
    """
    chars = ascii_letters + digits
    return "".join((choice(chars) for _ in range(12)))


def timer(func):
    """Timer decorator."""

    def f(*args, **kwargs):
        start = perf_counter()
        rv = func(*args, **kwargs)
        end = perf_counter()
        print(f"Elapsed time: {end-start:.3f} seconds")
        return rv

    return f


@timer
def random_subset_sum(points: list, total: int, subset_size: int) -> list:
    """Returns a random possible combination of points that sum to total.

    Parameters
    ----------
    points: list
        List of questions points.
    total: int
        Target number of points.
    subset_size: int
        Number of questions to choose from.

    Returns
    ----------
    list
        A list of questions points that sum to total.
    """
    shuffle(points)
    while subset_size <= 6:
        for subset in combinations(points, subset_size):
            if sum(subset) == total:
                return list(subset)
        subset_size += 1
    raise ValueError("No possible combination found, please try again.")


def get_final_questions(questions: list, points: list) -> list:
    """Get a list of questions the point values of which are in the points array.

    Parameters
    ----------
    questions: dict
        List of questions.
    points: list
        List of points.

    Returns
    ----------
    list
        A list of questions.
    """
    qs = []
    for p in points:
        tentative_qlist = [v[0] for _, v in questions.items() if v[1] == p]
        q = choice(tentative_qlist)
        while q in qs:
            q = choice(tentative_qlist)
        qs.append(q)
    return qs


def compile_and_clean(exam_filename: str, template: str):
    """Copy the desired template and compile the new exam in the appropriate folder;
    additionally remove all useless LaTeX files generated during compilation.

    Parameters
    ----------
    exam_filename: str
        Name of the exam file.
    template: str
        Name of the blank exam template file.
    """
    os.system(f"cp {ASSETS_FOLDER / template} {EXAMS_FOLDER / exam_filename}")
    os.chdir(EXAMS_FOLDER)
    os.system(f"latexmk -pdf {exam_filename}")
    os.chdir("../")
    # Remove all unuseful compiled latex files
    call(["sh", "./remove_unuseful_files.sh"])
