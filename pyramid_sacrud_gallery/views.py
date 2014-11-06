# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 Petr Zelenin <po.zelenin@gmail.com>
#
# Distributed under terms of the MIT license.

from pyramid.security import NO_PERMISSION_REQUIRED
from pyramid.view import view_config

from .common import get_model_by_name


@view_config(route_name='sacrud_gallery_view',
             renderer='pyramid_sacrud_gallery/index.jinja2',
             permission=NO_PERMISSION_REQUIRED)
def gallery_view(request):
    dbsession = request.dbsession
    id = request.matchdict['id']
    gallery_table = get_model_by_name(request.registry.settings, 'Gallery')
    gallery_instance = dbsession.query(gallery_table).filter(
        gallery_table.get_col_pk() == id).one()
    return {
        'gallery': gallery_instance,
    }
