"""
Topic classification server as a microservice
@starcolon projects
"""

import os
import sys
import json
import argparse
import subprocess
import numpy as np
from flask import Flask, request
from termcolor import colored
from pprint import pprint
from pypipe import pipe as Pipe
from pypipe import datapipe as DP
from pypipe.operations import rabbit
from pypipe.operations import tapper as T
from pypipe.operations import cluster
from pypipe.operations import taghasher
from pypipe.operations import texthasher
from pypipe.operations import textcluster
from pypipe.operations import preprocess

REPO_DIR = os.getenv('PANTIPLIBR','../..')
TEXT_VECTORIZER_PATH  = '{0}/data/models/vectoriser'.format(REPO_DIR)
TAG_HASHER_PATH       = '{0}/data/models/taghash'.format(REPO_DIR)
CLF_PATH              = '{0}/data/models/clf'.format(REPO_DIR)
STOPWORDS_PATH        = '{0}/data/words/stopwords.txt'.format(REPO_DIR)
CSV_REPORT_PATH       = '{0}/data/report.csv'.format(REPO_DIR)


class Classifier:

  def __init__(self):
    # Load the trained models
    print(colored('Loading CLF models','magenta'))
    self.topicHasher = texthasher.safe_load(TEXT_VECTORIZER_PATH,stop_words=[])
    self.tagHasher   = taghasher.safe_load(TAG_HASHER_PATH,n_feature=256)
    self.clf         = cluster.safe_load(CLF_PATH,method=None,n_features=256)
    print(colored('[DONE] ','green'),'CLF models loaded')

  def classify(self,topic):
    # Prepare processing functions
    hashMe     = texthasher.hash(self.topicHasher,learn=False)
    hashtagMe  = taghasher.hash(self.tagHasher,learn=False)
    classifyMe = cluster.analyze(self.clf)

    v = hashMe(str(topic['title'] + topic['topic']))
    t = ' '.join([tag for tag in topic['tags'] if len(tag)>1])
    w = hashtagMe(t)
    x = [list(a)+list(b) for a,b in zip(list(v),list(w))]

    y = classifyMe(x)
    return y

  def create_topic(self,title,tags,content):
    return {
      'title': title,
      'tags' : tags,
      'topic': content
    }


# Server configuration and setup
app = Flask(__name__)

class ErrorResponse(Exception):
  status_code = 500

  def __init__(self,message,status_code=500):
    Exception.__init__(self)
    self.message     = message
    self.status_code = status_code


# Server lifetime-wide variables
clf         = Classifier()
ALL_ATTRS   = ['title','topic','tags']
workers     = []

def try_parse(req):
  try:
    if len(req)<3:
      print(colored('Unrecognised request format','red'))
      return None
    elif any([(attr not in req) for attr in ALL_ATTRS]):
      print(colored('Missing mandatory attributes','red'))
      return None
    else:
      print(colored('Valid request received.','green'))
      return req
  except e:
    print(colored('[ERROR]','red'))
    print(colored(e,'red'))
    return None

def classify_req(topic):
  global clf
  print(colored('Classifying: ','cyan'))

  # Apply preprocessing
  topic = preprocess.take(topic)
  pprint(topic)
  c = next(clf.classify(topic))
  print(colored('#CLASS : ${}'.format(c),'cyan'))
  return c

# Merge requesting topic along with the 
# classification result
def encap_resp(req,c):
  resp = json.dumps({
    'class': c.item(), # [c] is a numpy.int64, not a primitive py int
    'title': req['title'],
    'topic': req['topic'],
    'tags':  req['tags']
  }, ensure_ascii=False)
  return resp

@app.route('/')
def root():
  return __name__

@app.errorhandler(ErrorResponse)
def handle_http_error(e):
  return json.dumps(e)

@app.route('/classify', methods=['POST'])
def classify():
  # Parse the JSON request data
  req = try_parse(request.json)
  if req is None:
    # Invalid request package
    print(colored('Unparsable request package','red'))
    raise ErrorResponse('Invalid Request',500)
  else:
    return encap_resp(req,classify_req(req))


def run_tokeniser():
  global workers
  script = 'ruby {0}/core/tokenizer/tokenizer.rb'.format(REPO_DIR)
  print(colored('🚀 Executing...','green') + script)
  sp = subprocess.Popen(script, 
    shell=True, stdout=subprocess.PIPE,
    preexec_fn=os.setsid)
  workers.append(sp)

def end_worker(sp):
  print(colored('Ending worker pid#${}'.format(sp.pid),'green'))
  subprocess.Popen('kill {0}'.format(sp.pid),
    shell=True, stdout=subprocess.PIPE)

if __name__ == '__main__':

  global workers

  # Execute text tokeniser service in background
  run_tokeniser()

  print(colored('Classification microservice STARTED...','magenta'))
  app.run(host='0.0.0.0', port=1996)
  print(colored('Classification microservice ENDED...','magenta'))

  # End all workers (tokeniser)
  [end_worker(sp) for sp in workers]

