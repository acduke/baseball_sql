import concurrent.futures
import time
import pandas as pd
import typer
import random

import season_simulator as sim


def sim_seasons(num_seasons: int, id: int):
    sim.main(id = str(id), show_summary=False, num_seasons=num_seasons)
    return id

def get_job_size_distribution():
    num_seasons_on_avg = 1000
    num_steps = 25
    step_size = int(num_seasons_on_avg/num_steps)
    one_way_range = int((num_steps-1)/2)*step_size
    lo = num_seasons_on_avg-one_way_range
    hi = num_seasons_on_avg+one_way_range
    print(range(lo, hi))
    num_seasons_distribution = list(range(lo, hi+step_size, step_size))
    random.shuffle(num_seasons_distribution)
    return num_seasons_distribution

def summarize_data(num_jobs: int):
    sim_results = sim.gather_results()
    summary = sim.summarize_sim_results(sim_results)
    print(summary.sort_values('champ_shares', ascending=False).to_string())


def main(num_jobs: int = 100):
    start = time.perf_counter()

    num_seasons_distribution = get_job_size_distribution()
    with concurrent.futures.ProcessPoolExecutor() as executor:
        def submit_job(id):
            num_seasons = num_seasons_distribution[id%len(num_seasons_distribution)]
            return executor.submit(sim_seasons, num_seasons, id)

        futures = [submit_job(id) for id in range(num_jobs)]

        for f in concurrent.futures.as_completed(futures):
            print(f'Job {f.result()} completed')

    end = time.perf_counter()
    print(f'Finished simulation in {round(end-start, 2)} second(s)')

    start = time.perf_counter()
    summarize_data(num_jobs)
    end = time.perf_counter()
    print(f'Finished summarization in {round(end-start, 2)} second(s)')

if __name__ == '__main__':
    typer.run(main)
