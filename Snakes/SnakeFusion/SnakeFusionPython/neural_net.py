import csv
from pathlib import Path

from matrix import Matrix


class NeuralNet:
    def __init__(self, inputs: int, hidden_no: int, output_no: int) -> None:
        self.i_nodes = inputs
        self.h_nodes = hidden_no
        self.o_nodes = output_no

        self.whi = Matrix(self.h_nodes, self.i_nodes + 1)
        self.whh = Matrix(self.h_nodes, self.h_nodes + 1)
        self.woh = Matrix(self.o_nodes, self.h_nodes + 1)

        self.whi.randomize()
        self.whh.randomize()
        self.woh.randomize()

    def mutate(self, mutation_rate: float) -> None:
        self.whi.mutate(mutation_rate)
        self.whh.mutate(mutation_rate)
        self.woh.mutate(mutation_rate)

    def output(self, inputs_arr: list[float]) -> list[float]:
        inputs = Matrix.single_column_matrix_from_array(inputs_arr)
        inputs_bias = inputs.add_bias()
        hidden_inputs = self.whi.dot(inputs_bias)
        hidden_outputs = hidden_inputs.activate()
        hidden_outputs_bias = hidden_outputs.add_bias()
        hidden_inputs2 = self.whh.dot(hidden_outputs_bias)
        hidden_outputs2 = hidden_inputs2.activate()
        hidden_outputs_bias2 = hidden_outputs2.add_bias()
        output_inputs = self.woh.dot(hidden_outputs_bias2)
        outputs = output_inputs.activate()
        return outputs.to_array()

    def crossover(self, partner: "NeuralNet") -> "NeuralNet":
        child = NeuralNet(self.i_nodes, self.h_nodes, self.o_nodes)
        child.whi = self.whi.crossover(partner.whi)
        child.whh = self.whh.crossover(partner.whh)
        child.woh = self.woh.crossover(partner.woh)
        return child

    def clone(self) -> "NeuralNet":
        clone = NeuralNet(self.i_nodes, self.h_nodes, self.o_nodes)
        clone.whi = self.whi.clone()
        clone.whh = self.whh.clone()
        clone.woh = self.woh.clone()
        return clone

    def save_csv(self, path: Path) -> None:
        rows = [self.whi.to_array(), self.whh.to_array(), self.woh.to_array()]
        width = max(len(r) for r in rows)
        with path.open("w", newline="") as f:
            writer = csv.writer(f)
            for row in rows:
                writer.writerow(row + [""] * (width - len(row)))

    def load_csv(self, path: Path) -> None:
        rows: list[list[float]] = []
        with path.open("r", newline="") as f:
            reader = csv.reader(f)
            for row in reader:
                rows.append([float(x) for x in row if x != ""])

        self.whi.from_array(rows[0][: self.whi.rows * self.whi.cols])
        self.whh.from_array(rows[1][: self.whh.rows * self.whh.cols])
        self.woh.from_array(rows[2][: self.woh.rows * self.woh.cols])
