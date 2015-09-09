from phabricator import Phabricator

phab = Phabricator()

class User(object):
  def __init__(self, **fields):
    self.__dict__.update(fields)

  @classmethod
  def all(cls, limit=500):
    return [cls(**user) for user in phab.user.query(limit=limit).response]

  @classmethod
  def map(cls, limit=500):
    return {user.phid: user.realName for user in cls.all(limit=limit)}


class Diff(object):
  def __init__(self, **fields):
    self.__dict__.update(fields)

  def enrich(self):
    msg = phab.differential.getcommitmessage(revision_id=self.id).response
    self.__dict__.update(phab.differential.parsecommitmessage(corpus=msg).fields)
    return self

  @classmethod
  def all(cls, limit=1000):
    # Warning: This method will take long time.
    diffs = [cls(**diff) for diff in phab.differential.query(limit=limit,
                                                             order='order-created',
                                                             status='status-closed')]
    [diff.enrich() for diff in diffs]
    return diffs


class Task(object):
  def __init__(self, **fields):
    self.__dict__.update(fields)

  @classmethod
  def all(cls, limit=1000):
    return [cls(**task) for task in phab.maniphest.query(status='status-resolved', order='order-created', limit=limit).response.values()]

class Project(object):
  def __init__(self, **fields):
    self.__dict__.update(fields)
