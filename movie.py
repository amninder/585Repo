import recsys.algorithm
from recsys.utils.svdlibc import SVDLIBC
recsys.algorithm.VERBOSE = True
import json
from fabric.colors import *

# from recsys.algorithm.factorize import SVD
# svd = SVD()
# svd.load_data(filename='ratings.dat', sep='::', format={'col':0, 'row':1, 'value':2, 'ids': int})

# k = 100
# svd.compute(k=k, min_values=10, pre_normalize=None, mean_center=True, post_normalize=True)

# k = 100
# svd.compute(k=k, min_values=10, pre_normalize=None, mean_center=True, post_normalize=True, savefile='/tmp/movielens')

# from recsys.algorithm.factorize import SVD
# svd2 = SVD(filename='/tmp/movielens')

ITEMID1 = 1
ITEMID2 = 2355
svd 	= None
svdlibc = None
tree 	= []

ratings = 'ratings.dat'
movieNames = 'movies.dat'
movie_dict = {}
movie_name_dict = {}
movie_similarity = {}
similar_title = []

def readDat():
	print(white("READING RATING FILE"))
	global svd
	global svdlibc
	global tree
	global similar_title
	svdlibc = SVDLIBC(ratings)
	svdlibc.to_sparse_matrix(sep='::', \
		format={'col':0, 'row':1, 'value':2, 'ids': int})
	svdlibc.compute(k=100)
	svd = svdlibc.export()
	tree.append(svd.similar(ITEMID1))
	for name in tree:
		for n in name[1:]:
			similar_title.append(n[0])
			if svd.similar(n[0]) not in tree:
				tree.append(svd.similar(n[0]))
		movie_similarity[name[0][0]] = similar_title
		similar_title = []

def generateResult(dict):
	print(white("GENERATING SIMILARITY MATRIX"))
	for key, value in dict.iteritems():
		# str = retMovieName(key)
		str = "%d"%key
		for v in value:
			# str += "::%s"%retMovieName(v)
			str += "::%d"%v
		# print str
		with open("result.dat", "a") as resultFile:
			resultFile.write(str+"\n")
		str = ''
	print(white("GEENRATING JSON FILE"))
	# with open("result.json", 'a') as js:
	# 	js.write(json.dumps(dict))
def dat_to_json(dict):
	l = []
	for key, value in dict.iteritems():
		# print retMovieName(key)
		for v in value:
			# print white(retMovieName(v))
			l.append(retMovieName(v))
		movie_name_dict[retMovieName(key)] = l
		l = []
	# print movie_name_dict
	with open("result.json", 'a') as js:
		js.write(json.dumps(movie_name_dict,  ensure_ascii=False))

def makeJSON(itemid):
	for x in tree:
		for i in x[1:]:
			print i
			item = svd.similar(i[0])
			if item not in tree:
				print "Added"
				tree.append(item)
			else:
				print "Not added"
	print tree

def retMovieName(id):
	return movie_dict[str(id)]

def readMovieNames():
	print(white("READING MOVIE NAMES"))
	global movieNames
	movies = open(movieNames, "r")
	lines = movies.readlines()
	for line in lines:
		# print line
		x = line.split("::")
		# print "Id: %s, Name: %s"%(x[0], x[1])
		movie_dict[x[0]] = x[1]
	# print movie_dict


readMovieNames()
readDat()
generateResult(movie_similarity)
dat_to_json(movie_similarity)
# makeJSON(tree[0])
"""
Down to you (2000)
Toy Story (1995)
IMDB doesnot suggest for The Mystic Masseur
"""
