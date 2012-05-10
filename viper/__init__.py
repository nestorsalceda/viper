# -*- coding: utf-8 -*-

import os
from tornado import web
import pymongo

from viper import handlers, commands, mappers


def application():
    database = pymongo.Connection()['viper_package_index']

    packages = mappers.PackageMapper(database)
    files = mappers.FileMapper(database)
    pypi = mappers.PythonPackageIndex()

    submit = commands.SubmitCommand(packages)
    upload = commands.FileUploadCommand(packages, files)

    return web.Application(
        [
            (r'/', handlers.MainHandler),
            web.url(r'/distutils/',
                handlers.DistutilsDownloadHandler, dict(packages=packages)
            ),
            web.url(r'/distutils/(?P<id_>%s)/' % identifier(),
                handlers.DistutilsDownloadHandler, dict(packages=packages),
                name='distutils_package'
            ),
            web.url(r'/distutils',
                handlers.DistutilsHandler, dict(submit=submit, upload=upload)
            ),
            web.url(r'/packages',
                handlers.AllPackagesHandler, dict(packages=packages)
            ),
            web.url(r'/packages/(?P<id_>%s)' % identifier(),
                handlers.PackageHandler, dict(packages=packages, pypi=pypi, files=files),
                name='package'
            ),
            web.url(r'/packages/(?P<id_>%s)/(?P<version>%s)' % (identifier(), identifier()),
                handlers.PackageHandler, dict(packages=packages, pypi=pypi, files=files),
                name='package_with_version'
            ),
            web.url(r'/files/(?P<id_>%s)' % identifier(),
                handlers.FileHandler, dict(files=files),
                name='file'
            )
        ],
        debug=True,
        template_path=os.path.join(os.path.dirname(__file__), 'templates'),
        static_path=os.path.join(os.path.dirname(__file__), 'static'),
        pypi_fallback="http://pypi.python.org/simple/%s/"
    )


def identifier():
    return "[a-zA-Z0-9-_.]+"
