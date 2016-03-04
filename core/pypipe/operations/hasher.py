"""
Text hashing vectoriser module
@starcolon projects
"""

import numpy as np
import os.path
import pickle
import json
from termcolor import colored
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.linear_model import RidgeClassifier
from sklearn.neighbors import NearestCentroid
from sklearn.preprocessing import Normalizer
from sklearn.pipeline import make_pipeline
from sklearn.decomposition import PCA


# Create a text process pipeline (vectorizer)
def new():
	# Prepare vectoriser engines
	hasher = HashingVectorizer(
		n_features=512,
		non_negative=True,
		binary=False)
	idf = TfidfVectorizer()

	# Prepare dimentionality reducer
	pca = PCA(n_components=64)
	# After PCA, it needs normalisation
	normalizer = Normalizer(copy=False)

	# Classifiers
	ncentroid = NearestCentroid(metric='euclidean')

	# Prepare task pipeline
	vectorizer = [hasher,idf]
	preprocess = [pca,normalizer]
	classifier = [ncentroid]
	return (vectorizer,preprocess,classifier)

def save(transformer,path):
	with open(path,'wb+') as f:
		pickle.dump(transformer,f)

def load(path):
	with open(path,'rb') as f:
		return pickle.load(f)

# Load the transformer pipeline object
# from the physical file,
# or initialise a new object if the file doesn't exist
def safe_load(path):
	if os.path.isfile(path): return load(path)
	else: return new()


# @param {Object}
def to_feature_vector(r):
	title = r['title']
	topic = r['topic']
	tags = [tag.strip() for tag in r['tags'] if len(tag)>0]

	feat = []
	# TAOTODO: Make feature vector out of the input set

	return feat


# @param {String}
def to_train_vector(rec):
	_r = json.loads(rec)

	y = (_r['emoti'],_r['vote'])
	x = to_feature_vector(_r)

	return (y,x)


# Train the vectorizer with the collection (iterable) of text data
# @return {Tuple(a,b)} where a:transformer, b: transformation results
def train(transformer,collection):
	
	X = collection

	# TAOTODO:

	return (transformer,X)


# @return {Matrix} Term document matrix with dimension reduction
def vectorize(transformer):
	seq_opr = make_pipeline(transformer)
	def _vectorize_on(collection):
		return seq_opr.transform(collection)
	return _vectorize_on


