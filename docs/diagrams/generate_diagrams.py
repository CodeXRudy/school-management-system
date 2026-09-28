"""Generates the design diagrams (PNG) used in the project report.

Requires Graphviz (`dot`) and matplotlib.  Run from anywhere:
    python docs/diagrams/generate_diagrams.py
"""
import os
import subprocess

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = os.path.dirname(os.path.abspath(__file__))

NODE = 'fontname="Helvetica" fontsize=11'


def dot(name, source):
    path = os.path.join(OUT, name + ".dot")
    with open(path, "w") as f:
        f.write(source)
    subprocess.run(["dot", "-Tpng", "-Gdpi=170", path, "-o", os.path.join(OUT, name + ".png")], check=True)
    os.remove(path)


# 1. System architecture -----------------------------------------------------
dot("architecture", f"""
digraph G {{
  rankdir=TB; nodesep=0.5; ranksep=0.55;
  node [shape=box style="rounded,filled" {NODE} margin="0.25,0.12"];
  edge [fontname="Helvetica" fontsize=9];

  user [label="User (Admin / Teacher)\\nConsole" fillcolor="#FDEBD0"];
  subgraph cluster_pres {{ label="Presentation Layer"; style=dashed; fontname="Helvetica";
    main [label="main.py\\n(entry point)" fillcolor="#D6EAF8"];
    menu [label="menu.py\\nrun_menu()" fillcolor="#D6EAF8"]; }}
  subgraph cluster_logic {{ label="Business Logic Layer"; style=dashed; fontname="Helvetica";
    persons [label="persons.py\\nabstract base + validate_email()" fillcolor="#D5F5E3"];
    student [label="student.py\\nStudent" fillcolor="#D5F5E3"];
    teacher [label="teacher.py\\nTeacher" fillcolor="#D5F5E3"]; }}
  subgraph cluster_data {{ label="Data Layer"; style=dashed; fontname="Helvetica";
    storage [label="storage.py\\nload / save()" fillcolor="#E8DAEF"];
    json [label="School_data.json" shape=cylinder fillcolor="#F9E79F"]; }}

  user -> main [label="keyboard input"];
  main -> menu; menu -> student [label="choice 1,3,4"]; menu -> teacher [label="choice 2,5"];
  student -> persons [arrowhead=empty label="inherits"]; teacher -> persons [arrowhead=empty label="inherits"];
  student -> storage; teacher -> storage; storage -> json [dir=both label="read / write"];
  menu -> user [style=dotted label="console output" constraint=false];
}}
""")

# 2. Workflow -------------------------------------------------------------------
dot("workflow", f"""
digraph G {{
  rankdir=TB; nodesep=0.35; ranksep=0.38;
  node [shape=box style="rounded,filled" fillcolor="#D6EAF8" {NODE}];
  edge [fontname="Helvetica" fontsize=9];
  start [label="Start" shape=oval fillcolor="#D5F5E3"];
  load [label="Load School_data.json\\n(if it exists)"];
  show [label="Display menu (options 1-5)"];
  choice [label="Read choice" shape=diamond fillcolor="#FDEBD0"];
  reg_s [label="Student.register()"]; reg_t [label="Teacher.register()"];
  grade [label="Student.add_grades()"]; sd [label="Student.show_details()"]; td [label="Teacher.show_details()"];
  valid [label="Email valid and\\nID unique?" shape=diamond fillcolor="#FDEBD0"];
  err [label="Print error message\\n(view options: silent)" fillcolor="#F5B7B1"];
  save [label="Append record and save()\\nto JSON file" fillcolor="#E8DAEF"];
  find [label="Record found?" shape=diamond fillcolor="#FDEBD0"];
  out [label="Print result / details"];
  end [label="End" shape=oval fillcolor="#D5F5E3"];
  start -> load -> show -> choice;
  choice -> reg_s [label="1"]; choice -> reg_t [label="2"]; choice -> grade [label="3"];
  choice -> sd [label="4"]; choice -> td [label="5"];
  reg_s -> valid; reg_t -> valid;
  valid -> save [label="yes"]; valid -> err [label="no"];
  grade -> find; sd -> find; td -> find;
  find -> save [label="yes (grade only)"]; find -> out [label="yes (view)"]; find -> err [label="no"];
  save -> out; out -> end; err -> end;
}}
""")

# 3. Use case -------------------------------------------------------------------
dot("usecase", f"""
digraph G {{
  rankdir=LR; nodesep=0.3; ranksep=1.6;
  node [{NODE}];
  admin [label="School Admin /\\nTeacher" shape=box style=filled fillcolor="#FDEBD0"];
  subgraph cluster_sys {{ label="School Management System"; style=rounded; fontname="Helvetica";
    node [shape=ellipse style=filled fillcolor="#D6EAF8"];
    u1 [label="Register Student"]; u2 [label="Register Teacher"]; u3 [label="Add Grades"];
    u4 [label="View Student Details"]; u5 [label="View Teacher Details"];
    v1 [label="Validate Email" fillcolor="#D5F5E3"]; v2 [label="Check Duplicate ID" fillcolor="#D5F5E3"];
    v3 [label="Save Data to JSON" fillcolor="#E8DAEF"]; }}
  admin -> u1; admin -> u2; admin -> u3; admin -> u4; admin -> u5;
  u1 -> v1 [style=dashed label="<<include>>" fontsize=9]; u2 -> v1 [style=dashed label="<<include>>" fontsize=9];
  u1 -> v2 [style=dashed label="<<include>>" fontsize=9]; u2 -> v2 [style=dashed label="<<include>>" fontsize=9];
  u1 -> v3 [style=dashed label="<<include>>" fontsize=9]; u2 -> v3 [style=dashed label="<<include>>" fontsize=9];
  u3 -> v3 [style=dashed label="<<include>>" fontsize=9];
}}
""")

# 4. Class diagram --------------------------------------------------------------
dot("class_diagram", f"""
digraph G {{
  rankdir=BT; nodesep=0.8; ranksep=0.9;
  node [shape=record style=filled fillcolor="#FEF9E7" {NODE}];
  persons [label="{{«abstract»\\npersons|| +get_roles()\\l+register()\\l+show_details()\\l+validate_email(email) (static)\\l}}"];
  Student [label="{{Student||+get_roles() : str\\l+register()\\l+show_details()\\l+add_grades()\\l}}"];
  Teacher [label="{{Teacher||+get_roles() : str\\l+register()\\l+show_details()\\l}}"];
  storage [label="{{storage (module)|+ database : str\\l+ data : dict\\l|+save()\\l}}" fillcolor="#E8DAEF"];
  menu [label="{{menu (module)||+run_menu()\\l}}" fillcolor="#D6EAF8"];
  Student -> persons [arrowhead=empty]; Teacher -> persons [arrowhead=empty];
  Student -> storage [style=dashed arrowhead=open label="uses" fontsize=9];
  Teacher -> storage [style=dashed arrowhead=open label="uses" fontsize=9];
  menu -> Student [arrowhead=open label="creates" fontsize=9]; menu -> Teacher [arrowhead=open label="creates" fontsize=9];
}}
""")

# 5. ER diagram -----------------------------------------------------------------
dot("er_diagram", f"""
digraph G {{
  rankdir=LR; nodesep=0.7; ranksep=1.3;
  node [shape=plaintext {NODE}];
  edge [fontname="Helvetica" fontsize=10];
  Student [label=<<table border="1" cellborder="0" cellspacing="0" cellpadding="4">
    <tr><td bgcolor="#D6EAF8"><b>Student</b></td></tr>
    <tr><td align="left"><u>roll_number</u> (PK)</td></tr>
    <tr><td align="left">name</td></tr><tr><td align="left">age</td></tr>
    <tr><td align="left">email</td></tr></table>>];
  Grade [label=<<table border="1" cellborder="0" cellspacing="0" cellpadding="4">
    <tr><td bgcolor="#D5F5E3"><b>Grade</b> (nested in Student)</td></tr>
    <tr><td align="left">subject</td></tr><tr><td align="left">grade</td></tr></table>>];
  Teacher [label=<<table border="1" cellborder="0" cellspacing="0" cellpadding="4">
    <tr><td bgcolor="#FDEBD0"><b>Teacher</b></td></tr>
    <tr><td align="left"><u>emp_id</u> (PK)</td></tr>
    <tr><td align="left">name</td></tr><tr><td align="left">age</td></tr>
    <tr><td align="left">email</td></tr><tr><td align="left">subject</td></tr></table>>];
  Student -> Grade [label="has 0..*" arrowhead=crow];
}}
""")

# 6. Sequence diagram (drawn manually with matplotlib) ---------------------------
def sequence():
    actors = ["User", "menu.py", "Student", "persons", "storage.py", "JSON file"]
    xs = [1, 3.2, 5.4, 7.6, 9.8, 12]
    msgs = [
        (0, 1, "1. choose option 1"),
        (1, 2, "2. Student().register()"),
        (2, 0, "3. prompt name, age, email, roll no. (input)"),
        (0, 2, "4. enter details"),
        (2, 3, "5. validate_email(email)"),
        (3, 2, "6. True / False"),
        (2, 2, "7. check duplicate roll_number in data"),
        (2, 4, "8. append record, save()"),
        (4, 5, "9. json.dump(data)"),
        (2, 0, "10. 'Student registered successfully.'"),
    ]
    fig, ax = plt.subplots(figsize=(13, 7.4))
    top, gap = 9.2, 0.72
    bottom = top - gap * (len(msgs) + 1)
    for name, x in zip(actors, xs):
        ax.text(x, top + 0.35, name, ha="center", va="center", fontsize=11, fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.4", fc="#D6EAF8", ec="black"))
        ax.plot([x, x], [top, bottom], ls="--", color="grey", lw=1)
    for i, (a, b, text) in enumerate(msgs):
        y = top - gap * (i + 1)
        if a == b:
            x = xs[a]
            ax.annotate("", xy=(x, y - 0.3), xytext=(x, y), arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=-1.6"))
            ax.text(x + 0.55, y - 0.15, text, fontsize=9, va="center")
            continue
        dashed = text.startswith(("3.", "6.", "10."))
        ax.annotate("", xy=(xs[b], y), xytext=(xs[a], y),
                    arrowprops=dict(arrowstyle="->", lw=1.3, ls="--" if dashed else "-"))
        ax.text((xs[a] + xs[b]) / 2, y + 0.13, text, ha="center", fontsize=9)
    ax.set_xlim(0, 13.2); ax.set_ylim(bottom - 0.3, top + 0.9); ax.axis("off")
    ax.set_title("Sequence diagram: registering a student", fontsize=13, fontweight="bold")
    fig.savefig(os.path.join(OUT, "sequence.png"), dpi=170, bbox_inches="tight")
    plt.close(fig)


sequence()
print("Diagrams written to", OUT)
