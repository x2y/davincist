"""Field validators for AJAX request dictionaries."""

import collections
import re

from django.core.validators import validate_email


def get_errors(data, field_validators):
  errors = []
  for field, validators in field_validators.items():
    if not hasattr(validators, '__iter__'):
      validators = (validators,)
    for validator in validators:
      error = validator.error(data, field)
      if error:
        errors.append(error)
        break
  return errors


class RequiredValidator(object):
  def error(self, data, field):
    return 'Missing field: %s.' % field if field not in data else None


class NonEmptyValidator(object):
  def error(self, data, field):
    if field not in data:
      return 'Missing field: %s.' % field
    return 'Empty field: %s.' % field if not data[field].strip() else None


class StrippedLengthValidator(object):
  def __init__(self, max_length):
    self.max_length_ = max_length

  def error(self, data, field):
    if field not in data:
      return None
    print
    return ('Invalid text field: %s >%d chars' % (field, self.max_length_)
            if len(data[field].strip()) > self.max_length_ else None)


class IntegerValidator(object):
  def error(self, data, field):
    if field not in data:
      return None
    return 'Invalid number field: %s.' % field if not data[field].isdigit() else None


class BooleanValidator(object):
  def error(self, data, field):
    if field not in data:
      return None
    return 'Invalid boolean field: %s.' % field if data[field] not in ('true', 'false') else None


class ModelValidator(object):
  def __init__(self, model):
    self.model_ = model
    self.model_name_ = model._meta.object_name

  def error(self, data, field):
    if field not in data:
      return None

    try:
      pk = int(data[field])
    except:
      return 'Invalid %s model field: %s.' % (self.model_name_, field)

    if self.model_.objects.filter(pk=pk).count() != 1:
      return 'No unique %s model %s for field: %s.' % (self.model_name_, data[field], field)
    return None


class YouTubeIdValidator(object):
  def error(self, data, field):
    if field not in data:
      return None
    print
    return ('Invalid YouTube Id: %s.' % data[field]
            if not re.match(r'|[a-zA-Z_-]{11}', data[field]) else None)


class EmailValidator(object):
  def error(self, data, field):
    if field not in data:
      return None
    try:
      validate_email(data[field].strip())
    except:
      return 'Invalid email: %s.' % data[field] 


class IterableValidator(object):
  def __init__(self, element_type):
    self.element_type_ = element_type

  def error(self, data, field):
    if field not in data:
      return None

    if not isinstance(data[field], collections.Iterable):
      return 'Non-iterable field: %s.' % field

    try:
      self.element_type_(data[field])
    except:
      return 'Invalid %s field element.' % field

    return None
