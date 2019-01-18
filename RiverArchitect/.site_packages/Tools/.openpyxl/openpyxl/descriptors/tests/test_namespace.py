from __future__ import absolute_import
# copyright openpyxl 2010-2015

from ..namespace import namespaced


def test_no_namespace():
    obj = object()

    tag = namespaced(obj, "root")
    assert tag == "root"


def test_object_namespace():

    class Object:

        namespace = "main"

    obj = Object()

    tag = namespaced(obj, "root")
    assert tag == "{main}root"


def test_overwrite_namespace():

    obj = object()

    tag = namespaced(obj, "root", "main")
    assert tag == "{main}root"
