from concurrent.futures import ThreadPoolExecutor
import threading 
import time


def pipe(fastq):
    print("this thread start ", threading.current_thread())
    time.sleep(20)
    print("this thread done ", threading.current_thread())


def pipe_main(fastq_list, k=2):
    with ThreadPoolExecutor(max_workers=k) as f:
        f.map(pipe, fastq_list)


def main():
    fastq_list = [(1, 2), (1, 2), (1, 2)]
    pipe_main(fastq_list)


if __name__ == "__main__":
    main()
