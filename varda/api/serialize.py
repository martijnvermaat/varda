"""
API model serializers.

.. moduleauthor:: Martijn Vermaat <martijn@vermaat.name>

.. Licensed under the MIT license, see the LICENSE file.
"""


from functools import wraps

from flask import url_for

from ..models import Annotation, DataSource, InvalidDataSource, Sample, User
from ..tasks import TaskError


# Dispatch table for the serialize function below.
_serializers = []


def serializes(model):
    """
    Decorator to specify that a function creates a representation for a
    certain model.
    """
    def serializes_model(serializer):
        _serializers.append( (model, serializer) )
        @wraps(serializer)
        def wrapped_serializer(*args, **kwargs):
            return serializer(*args, **kwargs)
        return wrapped_serializer
    return serializes_model


@serializes(User)
def serialize_user(instance):
    """
    Create a RESTfull representation of a user as dictionary.
    """
    return {'uri':   url_for('.users_get', login=instance.login),
            'name':  instance.name,
            'login': instance.login,
            'roles': list(instance.roles()),
            'added': str(instance.added)}


@serializes(DataSource)
def serialize_data_source(instance):
    """
    Create a RESTfull representation of a data source as dictionary.
    """
    return {'uri':         url_for('.data_sources_get', data_source_id=instance.id),
            'user':        url_for('.users_get', login=instance.user.login),
            'annotations': url_for('.annotations_list', data_source_id=instance.id),
            'name':        instance.name,
            'filetype':    instance.filetype,
            'gzipped':     instance.gzipped,
            'added':       str(instance.added)}


@serializes(Annotation)
def serialize_annotation(instance):
    """
    Create a RESTfull representation of an annotation as dictionary.
    """
    return {'uri':         url_for('.annotations_get', data_source_id=instance.data_source_id, annotation_id=instance.id),
            'data_source': url_for('.data_sources_get', data_source_id=instance.data_source_id),
            'gzipped':     instance.data_source.gzipped,
            'added':       str(instance.added)}


@serializes(Sample)
def serialize_sample(instance):
    """
    Create a RESTfull representation of a sample as dictionary.
    """
    return {'uri':                url_for('.samples_get', sample_id=instance.id),
            'user':               url_for('.users_get', login=instance.user.login),
            'observations':       url_for('.observations_add', sample_id=instance.id),
            'regions':            url_for('.regions_add', sample_id=instance.id),
            'name':               instance.name,
            'coverage_threshold': instance.coverage_threshold,
            'pool_size':          instance.pool_size,
            'added':              str(instance.added)}


@serializes(InvalidDataSource)
@serializes(TaskError)
def serialize_exception(instance):
    """
    Create a RESTfull representation of an exception as dictionary.
    """
    return {'code':    instance.code,
            'message': instance.message}


def serialize(instance):
    """
    Create a RESTfull representation of an object as dictionary.

    This function dispatches to a specific serializer function depending on
    the type of object at hand.

    .. note:: Returns ``None`` if no serializer was found.
    .. note:: I don't think this construction of creating serializations is
        especially elegant, but it gets the job done and I really don't want
        any functionality for representations in the models themselves.
    """
    for model, serializer in _serializers:
        if isinstance(instance, model):
            return serializer(instance)