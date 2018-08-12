import numpy as np
import multiprocessing as multi
import sys

def chunks(n, page_list):
    return np.array_split(page_list, n)

def perform_extraction(page_ranges):
    file_name = multi.current_process().name + '.txt'

cpus = multi.cpu_count()
workers = []
page_list = [
            'https://www.yellowpages.com/search?search_terms=restaurant&geo_location_terms=Boston, MA&page=1',
            'https://www.yellowpages.com/search?search_terms=restaurant&geo_location_terms=Boston, MA&page=2',
            'https://www.yellowpages.com/search?search_terms=restaurant&geo_location_terms=Boston, MA&page=3',
            'https://www.yellowpages.com/search?search_terms=restaurant&geo_location_terms=Boston, MA&page=4'
            ]

page_bins = chunks(cpus, page_list)

for cpu in range(cpus):
    sys.stdout.write('CPU' + str(cpu) + '\n')
    worker = multi.Process(name=str(cpu),
                           target=perform_extraction,
                           args=(page_bins[cpu],))

    worker.start()
    workers.append(worker)

for worker in workers:
    worker.join()

print(workers)