from flask import g, url_for

from ..models import Group
from ..security import is_user, has_role, true
from .base import ModelResource
from .users import UsersResource

class GroupsResource(ModelResource):
    """
    Group resources model user-specified groups (e.g. disease type)
    """
        
    model = Group
    instance_name = 'group'
    instance_type = 'group'
    
    views = ['list', 'get', 'add', 'edit', 'delete']
    
    embeddable = {'user': UsersResource}
    filterable = {} # empty dict is necessary??
    orderable = ['name']
    
    # only admin should be able to see all groups?
    list_ensure_conditions = [has_role('admin')]
    list_ensure_options = {'satisfy': any}
    
    get_ensure_conditions = [has_role('admin'), owns_group]
    get_ensure_options = {'satisfy': any}
    
    add_ensure_conditions = [has_role('admin'), has_role('importer')]
    add_ensure_options = {'satisfy': any}
    add_schema = {'name': {'type': 'string', 'required' = True, 'maxlength': 200}}
    
    # TODO: add owns_group function to security module
    edit_ensure_conditions = [has_role('admin'), owns_group]
    edit_ensure_options = {'satisfy' : any}
    edit_schema = {'name': {'type': 'string', 'required' = True, 'maxlength': 200}}
    
    # TODO: add owns_group function to security module
    delete_ensure_conditions = [has_role('admin'), owns_group]
    delete_ensure_options = {'satisfy': any}
    
    @classmethod
    def serialize(cls, instance, embed=None):
        """
        A group is representend as an object with the following fields:
        
        **uri** (`uri`)
        URI for this resource
        
        **name** (`string`)
        Human readable name for group
        
        **added** (`string`)
        Date and time this group was added
        
        **user**(`object`)
        :ref:`Link <api-links> to a :ref:user
        """
        
        serialization = super(GroupsResource, cls).serialize(instance, embed=embed)
        serialization.update(name=instance.name,
                             added=str(instance.added.isoformat()))
        
        return serialization
        
    @classmethod
    def list_view(cls, *args, **kwargs):
        """
        Returns a colleciton of groups in the `group_collection` field.
        
        User must have role `admin` to list all groups        
        """
        return super(GroupsResource, cls).list_view(*args, **kwargs)
        
    @classmethod
    def get_view(cls, *args, **kwargs):
        """
        Returns a group 
        User must have role `admin` or own the group
        """
        return super(GroupsResource, cls).get_view(*args, **kwargs)
    
    @classmethod
    def add_view(cls, *args, **kwargs):
        """
        Adds a group to the collection
        
        User must have either role `admin` or `importer`
        """
        kwargs['user'] = g.user
        return super(GroupsResource, cls).add_view(*args, **kwargs)
        
    @classmethod
    def edit_view(cls, *args, **kwargs):
        """
        Edits a group
        
        User must have role `admin` or be the owner of the group
        """
        return super(GroupsResource, cls).edit_view(*args, **kwargs)
        
    @classmethod
    def delete_view(cls, *args, **kwargs):
        """
        Deletes a group
        
        User most have role `admin` or be the owner of the group
        """
        return super(GroupsResource, cls).delete_view(*args, **kwargs)
