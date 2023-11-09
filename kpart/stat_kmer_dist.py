#!/usr/bin/env python
import sys
import multiprocessing
import os
import time


def time_print(str):
	print("\033[32m%s\033[0m %s"%(time.strftime('[%H:%M:%S]',time.localtime(time.time())), str))


def sub_stat(ref_fn, ctg, qry_dbs):
	stat_db = {'common': 0}
	qry_db = {}
	time_print("\tDealing %s"%ctg)
	for qry_n in qry_dbs:
		stat_db[qry_n] = 0
		if ctg in qry_dbs[qry_n]:
			idx, fn = qry_dbs[qry_n][ctg]
			with open(fn, 'r') as fin:
				for line in fin:
					kmer = line.strip().split()[0]
					if kmer not in qry_db:
						qry_db[kmer] = qry_n
					else:
						qry_db[kmer] = 'common'
	
	kmer_cnt = 0
	with open(ref_fn, 'r') as fin:
		for line in fin:
			kmer = line.strip().split()[0]
			kmer_cnt += 1
			if kmer in qry_db:
				qry_n = qry_db[kmer]
				stat_db[qry_n] += 1
	
	return ctg, stat_db, kmer_cnt


def stat_kmer_dist(in_ref_dir, in_qry_dirs, out_stat, ts):
	time_print("Loading query file lists")
	qry_dbs = {}
	for i in range(0, len(in_qry_dirs)):
		in_qry_dir = in_qry_dirs[i]
		qry_n = in_qry_dir.split('/')[-1]
		qry_dbs[qry_n] = {}
		for fn in os.listdir(in_qry_dir):
			ctg = '.'.join(fn.split('.')[:-1])
			qry_dbs[qry_n][ctg] = [i, os.path.join(in_qry_dir, fn)]
	
	time_print("Statistic")
	pool = multiprocessing.Pool(processes=ts)
	res = []
	for fn in os.listdir(in_ref_dir):
		ref_fn = os.path.join(in_ref_dir, fn)
		ctg = '.'.join(fn.split('.')[:-1])
		r = pool.apply_async(sub_stat, (ref_fn, ctg, qry_dbs,))
		res.append(r)
	pool.close()
	pool.join()

	total_db = {}
	qry_ns = {}
	for r in res:
		ctg, stat_db, kmer_cnt = r.get()
		total_db[ctg] = {'cnt': kmer_cnt}
		for qry_n in stat_db:
			if qry_n not in qry_ns:
				qry_ns[qry_n] = 1
			total_db[ctg][qry_n] = stat_db[qry_n]

	qry_list = []
	for qry_n in qry_ns:
		if qry_n == 'common':
			continue
		qry_list.append(qry_n)
	qry_list = sorted(qry_list)
	time_print("Writing result")
	with open(out_stat, 'w') as fout:
		fout.write("ContigName,No. of Kmers,")
		fout.write("\"No. of kmers that are shared by %s\","%(','.join(qry_list)))
		tmp_list = []
		for qry_n in qry_list:
			tmp_list.append("No. of kmers that are present only in %s"%qry_n)
		fout.write(','.join(tmp_list))
		fout.write("\n")
		for ctg in sorted(total_db):
			fout.write("%s,%d,%d,"%(ctg, total_db[ctg]['cnt'], total_db[ctg]['common']))
			tmp_list = []
			for qry_n in qry_list:
				tmp_list.append(str(total_db[ctg][qry_n]))
			fout.write(','.join(tmp_list))
			fout.write("\n")

	time_print("Finished")


if __name__ == "__main__":
	if len(sys.argv) < 5:
		print("Usage: python %s <in_ref_dir> <in_qry_dirs> <out_stat> <threads>"%sys.argv[0])
	else:
		in_ref_dir, in_qry_dirs, out_stat, ts = sys.argv[1:]
		in_qry_dirs = in_qry_dirs.split(',')
		stat_kmer_dist(in_ref_dir, in_qry_dirs, out_stat, int(ts))

