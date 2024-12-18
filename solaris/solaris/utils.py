from solaris.models import models

def model_to_dict(model:models.Model):
    keys = [f.name for f in model._meta.get_fields()]
    values = [getattr(model, f.name) for f in model._meta.get_fields()]
    return dict(zip(keys, values))

