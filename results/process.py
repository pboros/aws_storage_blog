import os
import re
import sys

SYSBENCH_RES_LINE = r'\[ (?P<time>[0-9]+)s \] reads: (?P<reads>[0-9\.]+) MiB/s writes: (?P<writes>[0-9\.]+) MiB/s fsyncs: 0.00/s latency \(ms,95%\): (?P<latency>[0-9\.]+)'
sysbench_re = re.compile(SYSBENCH_RES_LINE)

def cleanup():
    for benchmark_type in ['rndrd', 'rndwr', 'rndrw']:
        for meas_type in ['tp', 'lat']:
            with open(f"../{benchmark_type}_{meas_type}.df", 'w') as f:
                f.write('')

def main():
    cleanup()
    for disk_type in os.listdir('.'):
        if disk_type == "process.py":
            continue
        benchmark_dir = "./{disk_type}".format(disk_type=disk_type)
        for result_file in os.listdir(benchmark_dir):
            print(f"Processing {result_file}")
            sys.stdout.flush()
            sysbench_results = []
            result_file_fullpath = "{benchmark_dir}/{result_file}".format(benchmark_dir=benchmark_dir, result_file=result_file)
            result_name = result_file.split('.')[0]
            benchmark_type, threads = result_name.split('_')
            with open(result_file_fullpath, 'r') as f:
                result_lines = f.readlines()
            for result_line in result_lines:
                match = sysbench_re.match(result_line)
                if match:
                    sysbench_results.append(match.groupdict())

            for sysbench_result in sysbench_results:
                with open(f"../{benchmark_type}_lat.df", 'a') as f:
                    f.write("{disk_type},{time},{benchmark_type},{threads},{metric},{value}\n".format(
                        disk_type=disk_type, time=sysbench_result['time'], benchmark_type=benchmark_type, threads=threads,
                        metric='latency', value=sysbench_result['latency']
                    ))
                with open(f"../{benchmark_type}_tp.df", 'a') as f:
                    if benchmark_type == "rndrd":
                            f.write("{disk_type},{time},{benchmark_type},{threads},{metric},{value}\n".format(
                                disk_type=disk_type, time=sysbench_result['time'], benchmark_type=benchmark_type, threads=threads,
                                metric='reads', value=sysbench_result['reads']
                            ))
                    elif benchmark_type == "rndwr":
                            f.write("{disk_type},{time},{benchmark_type},{threads},{metric},{value}\n".format(
                                disk_type=disk_type, time=sysbench_result['time'], benchmark_type=benchmark_type, threads=threads,
                                metric='writes', value=sysbench_result['writes']
                            ))
                    elif benchmark_type == "rndrw":
                        for metric in ['reads', 'writes']:
                            f.write("{disk_type},{time},{benchmark_type},{threads},{metric},{value}\n".format(
                                disk_type=disk_type, time=sysbench_result['time'], benchmark_type=benchmark_type, threads=threads,
                                metric=metric, value=sysbench_result[metric]
                            ))
                    else:
                        raise AssertionError("Unknown benchmark type")

if __name__ == "__main__":
    main()
