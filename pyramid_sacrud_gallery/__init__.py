# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 Petr Zelenin <po.zelenin@gmail.com>
#
# Distributed under terms of the MIT license.

from pyramid.config import Configurator
# from sqlalchemy import engine_from_config

# from .models import Base, DBSession


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    # engine = engine_from_config(settings, 'sqlalchemy.')
    # DBSession.configure(bind=engine)
    # Base.metadata.bind = engine
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.scan()
    return config.make_wsgi_app()
