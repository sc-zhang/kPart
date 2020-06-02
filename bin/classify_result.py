#!/usr/bin/env python
import sys
import time


def time_print(str):
	print("\033[32m%s\033[0m %s"%(time.strftime('[%H:%M:%S]',time.localtime(time.time())), str))


def classify_result(in_csv, out_csv):
	time_print("Starting classify")
	with open(in_csv, 'r') as fin:
		with open(out_csv, 'w') as fout:
			for line in fin:
				data = line.strip().split(',')
				if data[0] == 'ContigName':
					sample_list = []
					for info in data[-2:]:
						sample_list.append(info.split()[-1])
					data.append("Classify")
					fout.write("%s\n"%(','.join(data)))
				else:
					ctg = data[0]
					vals = list(map(int, data[3:]))
					val_db = {}
					for i in range(0, len(vals)):
						if vals[i] == 0:
							vals[i] += 1
						if vals[i] not in val_db:
							val_db[vals[i]] = []
						val_db[vals[i]].append(idx)
					top_idx = []
					for i in sorted(val_db, reverse=True):
						if len(top_idx) == 2:
							break
						for idx in val_db[i]:
							if len(top_idx) == 2:
								break
							top_idx.append(i)
					top_vals = [vals[top_idx[0]], vals[top_idx[1]]]
					if top_vals[0]*1.0/top_vals[1] > 2.0:
						data.append(sample_list[top_idx[0]])
					elif top_vals[1]*1.0/top_vals[0] > 2.0:
						data.append(sample_list[top_idx[1]])
					else:
						data.append('undermine')
					fout.write("%s\n"%(','.join(data)))
	time_print("Finished")


if __name__ == "__main__":
	if len(sys.argv) < 3:
		print("Usage: python %s <in_csv> <out_csv>"%sys.argv[0])
	else:
		in_csv, out_csv = sys.argv[1:]
		classify_result(in_csv, out_csv)

