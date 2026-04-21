from graphviz import Digraph

dot = Digraph("career_path", format="png")
dot.attr(rankdir="LR")

dot.node("A", "IT Auditor / Associate")
dot.node("B", "Senior IT Auditor")
dot.node("C", "IT Audit Lead / Manager")
dot.node("D", "Director / Head of Tech Audit")
dot.node("E", "Enterprise Audit Leadership")
dot.node("F", "Cyber GRC / Risk Mgmt")
dot.node("G", "Security Leadership Path")
dot.node("H", "Privacy / Compliance / Third-Party Risk")
dot.node("I", "Cloud / IAM / SDLC Assurance Specialist")

dot.edge("A", "B")
dot.edge("B", "C")
dot.edge("C", "D")
dot.edge("D", "E")

dot.edge("B", "F")
dot.edge("C", "F")
dot.edge("F", "G")

dot.edge("B", "H")
dot.edge("C", "I")
dot.edge("I", "F")

dot.render("career_path_diagram", view=True)