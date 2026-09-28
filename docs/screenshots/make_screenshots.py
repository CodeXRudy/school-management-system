"""Runs the real application with scripted input and renders each run as a terminal-style PNG.

Each scenario launches `main.py` in a fresh subprocess (like a real user would), inside a temporary
folder so no real data is touched.  The only trick: input() is wrapped so the typed answer is echoed
(a piped stdin would not show it).  Run:  python docs/screenshots/make_screenshots.py
"""
import os
import subprocess
import sys
import tempfile

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))

RUNNER = r"""
import builtins, sys, runpy
answers = iter(sys.argv[1:])
def echo_input(prompt=""):
    a = next(answers)
    print(prompt + a)
    return a
builtins.input = echo_input
sys.argv = ["main.py"]
runpy.run_path(r"%s", run_name="__main__")
""" % os.path.join(ROOT, "main.py")


def run(workdir, answers):
    env = dict(os.environ, PYTHONPATH=ROOT)
    res = subprocess.run([sys.executable, "-c", RUNNER, *answers], cwd=workdir, env=env,
                         capture_output=True, text=True)
    return (res.stdout + res.stderr).rstrip("\n")


def render(title, text, filename):
    lines = text.split("\n")
    height = 0.32 * len(lines) + 0.9
    fig = plt.figure(figsize=(9, height), facecolor="#1e1e1e")
    fig.text(0.02, 1 - 0.35 / height, "$ " + title, color="#8ae234", family="monospace", fontsize=10.5, va="center")
    for i, line in enumerate(lines):
        y = 1 - (0.85 + 0.32 * i) / height
        fig.text(0.02, y, line, color="#eeeeec", family="monospace", fontsize=10.5, va="center")
    fig.savefig(os.path.join(HERE, filename), dpi=150, facecolor=fig.get_facecolor())
    plt.close(fig)


def main():
    work = tempfile.mkdtemp()
    scenarios = [
        ("01_register_student.png", "python main.py   # option 1", ["1", "Asha Rao", "16", "asha@school.edu", "S101"]),
        ("02_register_teacher.png", "python main.py   # option 2", ["2", "Ravi Kumar", "41", "ravi@school.edu", "Physics", "T201"]),
        ("03_add_grade.png", "python main.py   # option 3", ["3", "S101", "Physics", "A"]),
        ("04_show_student.png", "python main.py   # option 4", ["4", "S101"]),
        ("05_show_teacher.png", "python main.py   # option 5", ["5", "T201"]),
        ("06_duplicate_roll.png", "python main.py   # duplicate roll number", ["1", "Meena", "17", "meena@school.edu", "S101"]),
        ("07_invalid_email.png", "python main.py   # invalid email", ["1", "Meena", "17", "meena-at-school", "S102"]),
        ("08_student_not_found.png", "python main.py   # grade for unknown student", ["3", "S999"]),
    ]
    for filename, title, answers in scenarios:
        render(title, run(work, answers), filename)
        print("wrote", filename)

    with open(os.path.join(work, "School_data.json")) as f:
        render("cat School_data.json", f.read().rstrip("\n"), "09_json_storage.png")

    tests = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"],
                           cwd=ROOT, capture_output=True, text=True)
    out = (tests.stdout + tests.stderr).strip().split("\n")
    # shorten "test_x (module.Class.test_x) ... ok" to "test_x ... ok" so it fits on screen
    short = [l.split(" (")[0] + " ... " + l.rsplit(" ... ", 1)[1] if " ... " in l else l for l in out]
    render("python -m unittest discover -s tests -v", "\n".join(short), "10_unit_tests.png")
    print("wrote 10_unit_tests.png")


if __name__ == "__main__":
    main()
