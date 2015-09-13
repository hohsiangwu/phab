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
    self._commit_message = None

  @property
  def commit_message(self):
    if not self._commit_message:
      message = phab.differential.getcommitmessage(revision_id=self.id).response
      self._commit_message = phab.differential.parsecommitmessage(corpus=message).fields
    return self._commit_message

  def enrich(self):
    self.__dict__.update(self.commit_message)
    return self

  @classmethod
  def all(cls, limit=1000, enrich=False):
    # Warning: This method will take long time.
    diffs = [cls(**diff) for diff in phab.differential.query(limit=limit,
                                                             order='order-created',
                                                             status='status-closed')]
    if enrich:
      [diff.enrich() for diff in diffs]
    return diffs


class Task(object):
  def __init__(self, **fields):
    self.__dict__.update(fields)
    self._transactions = None

  @classmethod
  def all(cls, limit=1000):
    return [cls(**task) for task in phab.maniphest.query(status='status-resolved', order='order-created', limit=limit).response.values()]

  @property
  def transactions(self):
    if not self._transactions:
      self._transactions = phab.maniphest.gettasktransactions(ids=[int(self.id)]).response[self.id]
    return self._transactions


class Project(object):
  def __init__(self, **fields):
    self.__dict__.update(fields)
