"""Field validators for AJAX request dictionaries."""


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


class NumberValidator(object):
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
    if not data[field].isdigit():
      return 'Invalid %s model field: %s.' % (self.model_name_, field)
    try:
      self.model_.objects.get(pk=int(data[field]))
    except:
      return 'No %s model %s for field: %s.' % (self.model_name_, data[field], field)
    return None
