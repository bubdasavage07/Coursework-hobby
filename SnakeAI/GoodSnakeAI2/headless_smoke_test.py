import argparse
import os
import sys
import types


def install_pygame_stub():
    pygame_stub = types.SimpleNamespace(
        draw=types.SimpleNamespace(
            rect=lambda *args, **kwargs: None,
            line=lambda *args, **kwargs: None,
            ellipse=lambda *args, **kwargs: None,
        )
    )
    sys.modules["pygame"] = pygame_stub


def run_smoke(generations, max_steps, population_size):
    install_pygame_stub()

    root = os.path.dirname(os.path.abspath(__file__))
    if root not in sys.path:
        sys.path.insert(0, root)

    import config
    from Population import Population

    config.humanPlaying = False
    config.modelLoaded = False
    config.mutationRate = config.defaultmutation

    pop = Population(population_size, [])
    best_scores = []

    for _ in range(generations):
        steps = 0
        while not pop.done() and steps < max_steps:
            pop.update()
            steps += 1

        if steps >= max_steps:
            raise RuntimeError(
                f"Generation {pop.gen} hit step cap {max_steps}. Possible loop stall."
            )

        pop.calculateFitness()
        pop.naturalSelection()
        best_scores.append(pop.bestSnakeScore)
        print(
            f"gen={pop.gen:03d} steps={steps:05d} best_score={pop.bestSnakeScore} "
            f"samebest={pop.samebest} mutation={config.mutationRate:.4f}"
        )

    non_decreasing = all(
        best_scores[i] >= best_scores[i - 1] for i in range(1, len(best_scores))
    )
    if not non_decreasing:
        raise RuntimeError("Best score regressed across generations.")

    print("PASS: no loop stall detected and best score stayed non-decreasing.")


def main():
    parser = argparse.ArgumentParser(description="Headless SnakeAI smoke test")
    parser.add_argument("--gens", type=int, default=20, help="Number of generations")
    parser.add_argument("--max-steps", type=int, default=7000, help="Step cap per generation")
    parser.add_argument("--pop-size", type=int, default=120, help="Population size")
    args = parser.parse_args()

    run_smoke(args.gens, args.max_steps, args.pop_size)


if __name__ == "__main__":
    main()
