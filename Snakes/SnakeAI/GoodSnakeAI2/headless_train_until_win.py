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


def run_until_win(
    max_generations,
    max_steps,
    population_size,
    log_every,
    save_every,
    model_path,
    resume,
    quiet,
    save_at,
    plateau_stop,
):
    install_pygame_stub()

    root = os.path.dirname(os.path.abspath(__file__))
    if root not in sys.path:
        sys.path.insert(0, root)

    import config
    from Population import Population
    from SnakeAI import load_model, save_model, seed_population_from_weights, default_model_path

    config.humanPlaying = False
    config.modelLoaded = False
    config.mutationRate = config.defaultmutation

    if model_path is None:
        model_path = default_model_path()

    evolution = []
    pop = Population(population_size, evolution)

    if resume and os.path.exists(model_path):
        weights, evo, metadata = load_model(model_path)
        if weights:
            evolution[:] = evo
            if "mutation_rate" in metadata:
                config.mutationRate = metadata["mutation_rate"]
                config.defaultmutation = metadata["mutation_rate"]
            pop = Population(population_size, evolution)
            seed_population_from_weights(pop, weights)
            if "generation" in metadata:
                pop.gen = metadata["generation"]
            else:
                pop.gen = len(evolution)
            if "best_score" in metadata:
                pop.bestSnakeScore = metadata["best_score"]
            elif evolution:
                pop.bestSnakeScore = evolution[-1]
    target_len = config.GRID_W * config.GRID_H
    last_best = pop.bestSnakeScore
    last_improve_gen = pop.gen

    generation_limit = max_generations if max_generations and max_generations > 0 else None
    gens_run = 0
    while True:
        steps = 0
        while not pop.done() and steps < max_steps:
            pop.update()
            steps += 1

        hit_cap = steps >= max_steps
        if hit_cap and not quiet:
            print(
                f"gen={pop.gen:05d} steps={steps:05d} "
                f"best_score={pop.bestSnakeScore} samebest={pop.samebest} "
                f"mutation={config.mutationRate:.4f} (step cap)"
            )

        pop.calculateFitness()
        avg_score = sum(s.score for s in pop.snakes) / float(len(pop.snakes))
        pop.naturalSelection()

        best_len = pop.bestSnakeScore
        if best_len > last_best:
            last_best = best_len
            last_improve_gen = pop.gen
        if not quiet and log_every and ((pop.gen % log_every) == 0 or best_len >= target_len):
            print(
                f"gen={pop.gen:05d} steps={steps:05d} "
                f"best_score={pop.bestSnakeScore} best_len={best_len}/{target_len} "
                f"avg_score={avg_score:.2f} "
                f"samebest={pop.samebest} mutation={config.mutationRate:.4f}"
            )

        if save_every and (pop.gen % save_every) == 0:
            save_model(model_path, pop, evolution)
        if save_at and pop.gen == save_at:
            save_model(model_path, pop, evolution)

        if best_len >= target_len:
            if save_every:
                save_model(model_path, pop, evolution)
            print(f"WIN: filled board at gen {pop.gen} with length {best_len}.")
            return True

        if plateau_stop and (pop.gen - last_improve_gen) >= plateau_stop:
            print(f"PLATEAU: no best_score improvement for {plateau_stop} generations (gen {pop.gen}).")
            return False

        gens_run += 1
        if generation_limit is not None and gens_run >= generation_limit:
            break

    print(f"STOP: reached max generations ({max_generations}) without a full board.")
    return False


def main():
    parser = argparse.ArgumentParser(description="Train SnakeAI headless until it fills the board")
    parser.add_argument("--max-gens", type=int, default=0, help="Maximum generations to run (0 = no limit)")
    parser.add_argument("--max-steps", type=int, default=12000, help="Step cap per generation")
    parser.add_argument("--pop-size", type=int, default=300, help="Population size")
    parser.add_argument("--log-every", type=int, default=1, help="Log every N generations")
    parser.add_argument("--save-every", type=int, default=50, help="Save model every N generations (0 disables)")
    parser.add_argument("--save-at", type=int, default=0, help="Save model at a specific generation (0 disables)")
    parser.add_argument("--model-path", type=str, default=None, help="Path to save model CSV")
    parser.add_argument("--resume", action="store_true", help="Resume from existing model path")
    parser.add_argument("--quiet", action="store_true", help="Suppress progress logs")
    parser.add_argument("--plateau-stop", type=int, default=0, help="Stop if best_score stalls for N generations")
    args = parser.parse_args()

    run_until_win(
        args.max_gens,
        args.max_steps,
        args.pop_size,
        args.log_every,
        args.save_every,
        args.model_path,
        args.resume,
        args.quiet,
        args.save_at,
        args.plateau_stop,
    )


if __name__ == "__main__":
    main()
