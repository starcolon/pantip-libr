"""
Report radaring renderer
@starcolon projects
"""

import sys
import pygal
import argparse
from pygal import Config
from itertools import tee
from termcolor import colored
from pprint import pprint

arguments = argparse.ArgumentParser()
arguments.add_argument('--from', type=str, default='data/report.csv') # CSV file input of the report
arguments.add_argument('--to', type=str, default='data/') # Where to save graphical radars
args = vars(arguments.parse_args(sys.argv[1:]))

def read_csv(path):
  with open(path,'r') as csv:
    return csv.readlines()

def gen_csv(lines):
  header_found = False
  for l in lines:
    if not header_found:
      if 'CLUSTER' in l and 'DECOM' in l:
        header_found = True
    else:
      if len(l)>10:
        yield to_hash(l)

def to_hash(rec):
  rec = list(map(lambda n: n.strip(),rec.split(',')))
  return {
    'cluster': rec[0],
    'decom':   rec[1],
    'N':       int(rec[2]),
    'feat':    None if rec[3] == 'None' else int(rec[3]),
    'tag':     int(rec[4]),
    '#total':  float(rec[5]),
    '#0':      float(rec[6]),
    '#1':      float(rec[7]),
    '#-1':     float(rec[8])
  }

def label(rec):
  return rec['cluster'].upper()

def param(rec):
  return rec['decom'] + '-' + str(rec['N'])

def decom(rec):
  return rec['decom'].upper()

if __name__ == '__main__':
  # Read in CSV report, strip the headers, blank lines
  print(colored('Reading CSV report ...','cyan'))
  csv = read_csv(args['from'])
  data_1, data_2, data_3 = tee(gen_csv(csv),3)

  # Make a renderable radar
  # where the `decomposition algorithms` are plotted on X (corners of Radar)
  # and `variations of parameters` are plotted on Y (contour lines)
  print(colored('Preparing radar ...','cyan'))
  cfg       = Config()
  cfg.fill  = True
  radar     = pygal.Radar(cfg, range=(70,85))
  radar.title = 'Clustering/Feature Comparison'
  bar       = {} # Bar charts, indexed by cluster type

  # NOTE: Need to do the loop, not the `set` conversion
  # otherwise the list gets sorted which becomes out of sync
  labels = []
  for n in data_1:
    if label(n) not in labels:
      labels.append(label(n))
      # Create a bar chart for each of the cluster type
      bar[label(n)] = pygal.HorizontalBar(cfg, range=(70,90))
      bar[label(n)].title = 'Cluster with ' + label(n).upper()
  radar.x_labels = labels

  params = []
  for n in data_2:
    if param(n) not in params:
      params.append(param(n))

  # Aggregate input vectors for charting
  radar_input = {par:[] for par in params}
  bar_input = {lbl: {} for lbl in labels}
  prev_label = None
  for d in data_3:
    lbl = label(d)
    par = param(d)
    dec = decom(d)
    radar_input[par].append(d['#total'])
    if dec not in bar_input[lbl]:
      bar_input[lbl][dec] = d['#total']
    else:
      # Alway collect the best performance 
      bar_input[lbl][dec] = bar_input[lbl][dec] if \
        bar_input[lbl][dec] > d['#total'] else \
        d['#total']

  # Render radar chart
  print(colored('Drawing radar...','cyan'))
  for par,vec in radar_input.items():
    radar.add(par, vec)

  radar.render_to_file(args['to'] + '/radar.svg')

  # Render bar charts
  for lbl in labels:
    for dec in bar_input[lbl]:
      bar[lbl].add('Best ' + dec, bar_input[lbl][dec])
    bar[lbl].render_to_file(args['to'] + '/bar-' + lbl +'.svg')

  print(colored('Done!','green'))
