#!/usr/bin/env python
import sys
from utils import time_print


def classify_result(in_csv, out_csv):
    time_print("Starting classify")
    with open(in_csv, 'r') as fin:
        with open(out_csv, 'w') as fout:
            for line in fin:
                data = line.strip().split(',')
                if data[0] == 'ContigName':
                    sample_list = []
                    for info in data[3:]:
                        sample_list.append(info.split()[-1])
                    data.append("Classification")
                    fout.write("%s\n" % (','.join(data)))
                else:
                    vals = list(map(int, data[3:]))
                    max_smp = ["", 0]
                    sec_max_smp = ["", 0]
                    for _ in range(len(vals)):
                        if vals[_] > max_smp[1]:
                            sec_max_smp[0] = max_smp[0]
                            sec_max_smp[1] = max_smp[1]
                            max_smp[0] = sample_list[_ - 3]
                            max_smp[1] = vals[_]
                        elif vals[_] > sec_max_smp[1]:
                            sec_max_smp[0] = sample_list[_ - 3]
                            sec_max_smp[1] = vals[_]
                    if max_smp[1] > sec_max_smp[1] * 2.:
                        data.append(max_smp[0])
                    else:
                        data.append('Undetermined')
                    fout.write("%s\n" % (','.join(data)))
    time_print("Finished")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python %s <in_csv> <out_csv>" % sys.argv[0])
    else:
        in_csv, out_csv = sys.argv[1:]
        classify_result(in_csv, out_csv)
