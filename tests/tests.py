# encoding=utf8
import unittest
from crawlers.lib import *
from nose.plugins.attrib import attr

class TestCase(unittest.TestCase):
  def test_movie_equal_case(self):
    "Movies must be equal even if name got tags or different case"
    title1 = "El pequeño Delfin qUe Hacia Mu (3d) (ESP)"
    title2 = "EL PEQUEÑO delfin que HACIA mu (3d) (esp)"
    movie1 = schemas.Movie(title1, None, [])
    movie2 = schemas.Movie(title2, None, [])

    self.assertTrue(movie1 == movie2)
    self.assertEqual(hash(movie1), hash(movie2))

  def test_movie_equal_accented(self):
    "Movies must be equal even if name got accented characters tags or different case"
    title1 = "El pequeño Delfín qUe Hacia Mu (3d) (ESP)"
    title2 = "EL PEQUEÑO delfin que HACIA mú (3d) (esp)"
    movie1 = schemas.Movie(title1, None, [])
    movie2 = schemas.Movie(title2, None, [])

    self.assertTrue(movie1 == movie2)
    self.assertEqual(hash(movie1), hash(movie2))

  @attr('important')
  def test_movie_equal_bad_accents(self):
    "Movies must be equal even if name is missing some chars"
    title1 = "FIN DEL SUENO AMERICANO"
    title2 = "El Fin Del Sueño Americano"

    movie1 = schemas.Movie(title1, None, [])
    movie2 = schemas.Movie(title2, None, [])

    self.assertTrue(movie1 == movie2)
    self.assertEqual(hash(movie1), hash(movie2))

  def test_movie_equal_very_likely(self):
    "Movies must be equal if their names are very alike"
    
    title1 = "SING VEN Y CANTA"
    title2 = "SING: VEN Y CANTA"

    movie1 = schemas.Movie(title1, None, [])
    movie2 = schemas.Movie(title2, None, [])

    self.assertTrue(movie1 == movie2)
    self.assertEqual(hash(movie1), hash(movie2))

  def test_tag_cleaner(self):
    "It must clean all tags from a movie title"
    title = "Un Titulazo (3d) (ESP)"
    clean = utils.clean_tags_from_title(title)

    self.assertEqual("Un Titulazo", clean)
  def test_tag_extractor(self):
    "It must extract all tags from a movie title"

    title = "Un Titulazo (3d) (ESP)"
    tags = utils.get_meta_from_title(title)

    self.assertEqual(tags, {
      '3d': True,
      'ESP': True
    })
