import pickle
import glob

pickles = [open(filename, 'rb') for filename in glob.glob('tmp/*.dump')]
instances = [pickle.load(dump) for dump in pickles]

def myhash(self):
  return hash(self.name.lower().strip()) 

chains = {}
theaters = {}
movies = {}

for chain in instances:
  chainHash = hex(abs(hash(chain)))
  chains[chainHash] = chain.name

  for theater in chain.theaters:
    theater.chain = chainHash
    theaterHash = hex(abs(hash(theater)))
    theaters[theaterHash] = theater.name
    for movie in theater.movies:
      movie.chains = []
      movie.theaters = []
      movie.__hash__ = myhash

      if not movies.get(hash(movie)):
        movies[hash(movie)] = movie
      
      if not chainHash in movies[hash(movie)].chains:
        movies[hash(movie)].chains.append(chainHash)
      if not theaterHash in movies[hash(movie)].theaters:
        movies[hash(movie)].theaters.append(theaterHash)


for k, x in movies.items():
  print("Name: %s\nChains: %s\nTheaters: %s" % (x.name, str(x.chains), str(x.theaters)), "\n")