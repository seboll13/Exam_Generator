""" Program dedicated to generate a random exam in LaTeX from an initial list of questions.
  __author__ = "Sebastien Ollquist"
  __copyright__ = "Sebastien Ollquist © 2022"
  __credits__ = ["Sebastien Ollquist"]
  __license__ = "---"
  __version__ = "1.1"
  __maintainer__ = "Sebastien Ollquist"
  __email__ = "sebastien.ollquist@epfl.ch"
  __status__ = "Functional, but yet in progress..."
"""

#!/usr/bin/python
import re, os, sys
import subprocess
import string, random
from itertools import combinations

ASSETS_FOLDER = 'Assets/'
EXAMS_FOLDER = 'Exams/'

QT_FORMAT_REGEX = '% QUESTION \d+\n' # question separator
PT_FORMAT_REGEX = '\[\d+\]' # any number in brackets (to recover question points)

NB_Q_MIN_MT, NB_Q_MIN_F = 3, 4 # minimum number of questions on a midterm and final exams
TOTAL_EXAM_PTS = 100


def generate_exam_id() -> str:
    # Generate unique exam ID of 12 digits
    chars = string.ascii_letters + string.digits
    return ''.join((random.choice(chars) for _ in range(12)))


def random_subset_sum(points, total, subset_size) -> list:
    """Returns a random possible combination of points that sum to total.
    @param points      => list of questions points
    @param total       => target number of points
    @param subset_size => # of questions to choose from"""
    random.shuffle(points)
    while (subset_size <= 6):
        for subset in combinations(points, subset_size):
            if sum(subset) == total:
                return list(subset)
        subset_size += 1
    return None


def get_question_collection(questions_file) -> dict:
    """Recover the entire list of questions from the LaTeX file.
    @param questions_file => path to the questions file"""
    questions = {}
    with open(questions_file, 'r') as f:
        # Separate each question and store them into an array
        for i, el in enumerate(re.split(QT_FORMAT_REGEX, f.read())[1:]):
            questions[i] = [el]
    return questions


def add_question_points(questions) -> list:
    """Get total points for each question.
    @param questions => list of questions"""
    pattern = re.compile(PT_FORMAT_REGEX)
    # Go through each question
    for i in range(len(questions)):
        points = 0
        # Sum up points of all subquestions if any
        for match in re.finditer(pattern, questions[i][0]):
            points += int(match.group()[1:-1])
        questions[i].append(points)
    # Return the list of total points for each question
    return [list(questions.values())[i][1] for i in range(len(questions))]


def construct_random_exam(filename, questions, exam_id) -> str:
    """Write the selected questions in a LaTeX file.
    @param filename   => name of the file to save the questions into
    @param questions  => list of questions to write to the file
    @param exam_id => exam is either a midterm or a final"""
    #random.shuffle(questions)
    with open(filename, 'w') as f:
        for q in questions:
            f.write(q + '\n')
    return exam_id + '-' + generate_exam_id() + '.tex'


def compile_and_clean(exam_filename, template):
    """Copy the desired template and compile the new exam in the appropriate folder;
    additionally remove all unuseful LaTeX files generated during compilation.
    @param exam_filename => name of the exam file
    @param template      => name of the blank exam template file"""
    os.system('cp %s %s' % (ASSETS_FOLDER + template, EXAMS_FOLDER + exam_filename))
    os.chdir(EXAMS_FOLDER)
    os.system('latexmk -pdf %s' % exam_filename)
    os.chdir('../')
    # Remove all unuseful compiled latex files
    subprocess.call(['sh', './remove_unuseful_files.sh'])


def get_final_questions(questions, points) -> list:
    """Get a list of questions the point values of which are in the points array.
    @param questions => the entire list of questions
    @param points    => the array of corresponding points"""
    qs = []
    for p in points:
        l = [v[0] for k,v in questions.items() if v[1] == p]
        q = random.choice(l)
        while q in qs:
            q = random.choice(l)
        qs.append(q)
    return qs


def generate_random_exam(is_midterm, nb_q, nb_qm=0) -> None:
    """Procedure called to generate an exam. 
    @param is_midterm => boolean to indicate whether or not the exam is a midterm
    @param nb_q       => total number of questions to write
    @param nb_qm      => number of questions from first part in a final exam, default value 0"""
    if is_midterm:
        exam_id = 'midterm'
        exam_points = TOTAL_EXAM_PTS
    else:
        exam_id = 'final'
        nb_qf = nb_q
        nb_q = nb_qm
        exam_points = random.choice([_ for _ in range(nb_q*10, nb_q*20+1)])

    questions = []
    # Normal procedure for midterm exam generation
    if nb_q > 0:
        mid_questions = get_question_collection(ASSETS_FOLDER + 'midterm-questions.tex')
        rand_pts = random_subset_sum(add_question_points(mid_questions), exam_points, nb_q)
        questions += get_final_questions(mid_questions, rand_pts)

    # Supplementary procedure for final exam generation
    if not is_midterm:
        fin_questions = get_question_collection(ASSETS_FOLDER + 'final-questions.tex')
        rand_pts_f = random_subset_sum(add_question_points(fin_questions), TOTAL_EXAM_PTS-exam_points, nb_qf-nb_qm)
        questions += get_final_questions(fin_questions, rand_pts_f)

    exam_filename = construct_random_exam(EXAMS_FOLDER + 'test.tex', questions, exam_id)
    compile_and_clean(exam_filename, exam_id + '-template_' + str(len(questions)) + '.tex')
    return


if __name__ == '__main__':
    """Main program usage
    arg count = 3
    argv[1]            => midterm or final
    argv[2]            => # of questions
    argv[3] (optional) => # of mid questions for final exam
    """
    assert(sys.argv[1] != None and sys.argv[2] != None)
    
    nb_q = int(sys.argv[2])
    try:
        if sys.argv[1] == 'midterm':
            generate_random_exam(True, nb_q)
        else:
            nb_qm = int(sys.argv[3])
            generate_random_exam(False, nb_q, nb_qm)
    except (TypeError, ValueError):
        print('Problem with arguments, exiting...')
        exit()
