# encoding=utf8
import unittest
from crawlers.lib import *

class TestCase(unittest.TestCase):
  def test_movie(self):
    "Movies must be equal even if name got tags or different case"
    title1 = "El pequeño Delfin qUe Hacia Mu (3d) (ESP)"
    title2 = "EL PEQUEÑO delfin que HACIA mu (3d) (esp)"
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
