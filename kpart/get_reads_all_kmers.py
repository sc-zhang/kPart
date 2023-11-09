#!/usr/bin/env python
import sys
import os
import multiprocessing
from utils import time_print, get_kmer


def write_kmers(in_fq, ks, out_kmer):
    kmer_db = {}
    cnt = 0
    time_print("\tGenerating %s" % in_fq)
    with open(in_fq, 'r') as fin:
        with open(out_kmer, 'w') as fout:
            for line in fin:
                if cnt % 4 == 1:
                    seq = line.strip()
                    get_kmer(kmer_db, seq, ks)
                cnt += 1

            for kmer in sorted(kmer_db):
                fout.write("%s\t%d\n" % (kmer, kmer_db[kmer]))


def get_all_kmers(in_fq_dir, ks, out_kmer_dir, ts):
    if not os.path.exists(out_kmer_dir):
        os.makedirs(out_kmer_dir)
    kmer_db = {}
    cnt = 0
    time_print("Loading reads and generating kmers")
    pool = multiprocessing.Pool(processes=ts)
    for fn in os.listdir(in_fq_dir):
        in_fq = os.path.join(in_fq_dir, fn)
        kmer_fn = fn.split('.')
        kmer_fn[-1] = 'kmers'
        kmer_fn = '.'.join(kmer_fn)
        out_kmer = os.path.join(out_kmer_dir, kmer_fn)
        pool.apply_async(write_kmers, (in_fq, ks, out_kmer,))
    pool.close()
    pool.join()

    time_print("Finished")


if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: python " + sys.argv[0] + " <in_fq_dir> <kmer_size> <out_kmer_dir> <threads>")
    else:
        in_fq_dir, kmer_size, out_kmer_dir, ts = sys.argv[1:]
        get_all_kmers(in_fq_dir, int(kmer_size), out_kmer_dir, int(ts))
