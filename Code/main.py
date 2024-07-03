"""Program dedicated to generate a random exam in LaTeX from an initial list of questions.
  __author__ = "Sebastien Ollquist"
  __copyright__ = "Sebastien Ollquist © 2024"
  __credits__ = ["Sebastien Ollquist"]
  __license__ = "MIT"
  __version__ = "2.0"
  __maintainer__ = "Sebastien Ollquist"
  __email__ = "sebastien.ollquist@hesge.ch"
  __status__ = "Functional, but yet in progress..."
"""

#!/usr/bin/python
from sys import argv

from Code.exam_creation import generate_random_exam


NB_Q_MIN_MT, NB_Q_MIN_F = (
    3,
    4,
)  # minimum number of questions on a midterm and final exams


def main():
    """Main function to be called.

    Usage
    ----------
    arg count = 3
    argv[1]            => midterm or final
    argv[2]            => # of questions
    argv[3] (optional) => # of mid questions for final exam
    """
    if len(argv) < 3:
        print("Not enough arguments, exiting...")
        raise SystemExit
    nb_q = int(argv[2])
    match argv[1]:
        case "midterm":
            if nb_q < NB_Q_MIN_MT:
                print("Not enough questions for a midterm exam, exiting...")
                raise SystemExit
            generate_random_exam(True, nb_q)
        case "final":
            if nb_q < NB_Q_MIN_F:
                print("Not enough questions for a final exam, exiting...")
                raise SystemExit
            nb_qm = int(argv[3])
            generate_random_exam(False, nb_q, nb_qm)
        case _:
            print("Invalid argument, exiting...")
            raise SystemExit


if __name__ == "__main__":
    main()
