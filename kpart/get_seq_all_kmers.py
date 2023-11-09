#!/usr/bin/env python
import sys
import os
import multiprocessing
from utils import time_print, get_kmer


def write_kmers(seq, ks, fn):
    kmer_db = {}
    time_print("\tGenerating %s" % fn)
    with open(fn, 'w') as fout:
        get_kmer(kmer_db, seq, ks)

        for kmer in sorted(kmer_db):
            fout.write("%s\t%d\n" % (kmer, kmer_db[kmer]))


def get_all_kmers(in_fa, ks, out_dir, ts):
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    fa_db = {}
    time_print("Loading fasta and generating kmers")
    with open(in_fa, 'r') as fin:
        for line in fin:
            if line[0] == '>':
                gid = line.strip().split()[0][1:]
                fa_db[gid] = []
            else:
                fa_db[gid].append(line.strip())

    time_print("Generating kmers")
    pool = multiprocessing.Pool(processes=ts)
    for gid in fa_db:
        seq = ''.join(fa_db[gid])
        fn = os.path.join(out_dir, gid + ".kmers")
        pool.apply_async(write_kmers, (seq, ks, fn,))
    pool.close()
    pool.join()
    time_print("Finished")


if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: python " + sys.argv[0] + " <in_fa> <kmer_size> <out_dir> <threads>")
    else:
        in_fa, kmer_size, out_dir, ts = sys.argv[1:]
        get_all_kmers(in_fa, int(kmer_size), out_dir, int(ts))
