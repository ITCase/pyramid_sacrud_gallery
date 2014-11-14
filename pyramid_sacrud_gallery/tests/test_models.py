# -*- coding: utf-8 -*-
#
# Copyright © 2014 Petr Zelenin (po.zelenin@gmail.com)
#
# Distributed under terms of the MIT license.

import unittest

import transaction

from sqlalchemy import create_engine
from sqlalchemy.exc import StatementError
from sqlalchemy.orm import scoped_session, sessionmaker

from zope.sqlalchemy import ZopeTransactionExtension

from . import (
    add_fixture,
    Base,
    Gallery, GalleryItem, GalleryItemM2M,
    TEST_DATABASE_CONNECTION_STRING,
)


DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))


def add_data(session):
    galleries = [
        {'pk': 1, 'name': 'Best gallery'}
    ]
    galleries = add_fixture(Gallery, galleries, session)
    items = []
    for x in xrange(1, 10):
        items.append({
            'pk': x,
            'image': 'images/%s.jpg' % x,
            'description': 'This is image with name "%s"' % x,
            'galleries': galleries
        })
    add_fixture(GalleryItem, items, session)


class TestGallery(unittest.TestCase):

    def setUp(self):
        engine = create_engine(TEST_DATABASE_CONNECTION_STRING)
        DBSession.configure(bind=engine)
        Base.metadata.create_all(engine)
        with transaction.manager:
            add_data(DBSession)

    def tearDown(self):
        DBSession.remove()

    def test_mixins_attrs(self):
        """Check mixins attrs auto apply to classes."""
        self.assertEqual(Gallery.get_pk(), 'pk')
        self.assertEqual(Gallery.get_db_pk(), 'id')
        self.assertEqual(Gallery.__tablename__, 'gallery')

        self.assertEqual(GalleryItem.get_pk(), 'pk')
        self.assertEqual(GalleryItem.get_db_pk(), 'id')
        self.assertEqual(GalleryItem.__tablename__, 'galleryitem')

        self.assertEqual(GalleryItemM2M.__tablename__, 'galleryitemm2m')

    def test_instances_attrs(self):
        """Check attrs and methods available only for instances."""
        gallery = DBSession.query(Gallery).one()
        self.assertEqual(gallery.__repr__(), 'Best gallery')
        self.assertEqual(gallery.get_val_pk(), 1)

    def test_mixins_fks(self):
        """Check GalleryItemM2MMixin has ForeignKeys to GalleryMixin
        and GalleryItemMixin."""
        self.assertTrue(hasattr(GalleryItemM2M, 'gallery_id'))
        self.assertTrue(hasattr(GalleryItemM2M, 'item_id'))

    def test_access_by_relations(self):
        """Check relations between GalleryMixin and GalleryItemMixin."""
        gallery = DBSession.query(Gallery).one()
        self.assertEqual(len(gallery.items), 9)

    def test_unique_image_hash(self):
        """Check of deny to add non-unique image_hash."""
        image = GalleryItem(image='images/1.jpg')
        DBSession.add(image)
        with self.assertRaises(StatementError) as cm:
            DBSession.query(GalleryItem).all()
        self.assertIn('This Connection is closed', str(cm.exception))
