from models.db_models import db


def get_all(model):
    data = model.query.all()
    return data


def get_instance(model, **kwargs):
    instance = model.query.filter_by(**kwargs).first()
    return instance


def add_instance(model, **kwargs):
    instance = model(**kwargs)
    db.session.add(instance)
    commit_changes()


def delete_instance(model, id):
    model.query.filter_by(id=id).delete()
    commit_changes()


def edit_instance(model, id, **kwargs):
    instance = model.query.filter_by(**kwargs).all()[0]
    for attr, new_value in kwargs.items():
        setattr(instance, attr, new_value)
    commit_changes()


def commit_changes():
    db.session.commit()
