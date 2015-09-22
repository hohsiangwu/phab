from phabricator import Phabricator

from utils import datetime_from_timestamp

phab = Phabricator()

class User(object):
  def __init__(self, **fields):
    self.__dict__.update(fields)

  @classmethod
  def query(cls, limit=500, **kwargs):
    return [cls(**user) for user in phab.user.query(limit=limit, **kwargs).response]

  @classmethod
  def maps(cls, limit=500, **kwargs):
    return {user.phid: user.realName for user in cls.query(limit=limit, **kwargs)}


class Diff(object):
  def __init__(self, diff_id=None, **fields):
    if diff_id is not None:
      fields = phab.differential.query(ids=[diff_id]).response[0]
    self.__dict__.update(fields)
    self._transactions = None

  @property
  def transactions(self):
    if not self._transactions:
      self._transactions = phab.differential.getrevisioncomments(ids=[int(self.id)]).response[self.id]
    return self._transactions

  @property
  def authored_by(self):
    return (
      self.transactions[0]['authorPHID'],
      datetime_from_timestamp(self.transactions[0]['dateCreated'])
    )

  @property
  def commented_by(self):
    return [(t['authorPHID'], datetime_from_timestamp(t['dateCreated']))
            for t in self.transactions if t['action'] == 'comment']

  @property
  def accepted_by(self):
    return [(t['authorPHID'], datetime_from_timestamp(t['dateCreated']))
            for t in self.transactions if t['action'] == 'accept']

  @property
  def committed_by(self):
    return [(t['authorPHID'], datetime_from_timestamp(t['dateCreated']))
            for t in self.transactions if t['action'] == 'commit']

  @classmethod
  def query(cls, limit=1000, order='order-created', status='status-any', **kwargs):
    return [cls(**diff) for diff in phab.differential.query(limit=limit,
                                                            order=order,
                                                            status=status,
                                                            **kwargs).response]


class Task(object):
  def __init__(self, **fields):
    self.__dict__.update(fields)
    self._transactions = None

  @classmethod
  def query(cls, limit=1000, order='order-created', status='status-any', **kwargs):
    return [cls(**task) for task in phab.maniphest.query(limit=limit,
                                                         status=status,
                                                         order=order,
                                                         **kwargs).response.values()]

  @property
  def transactions(self):
    if not self._transactions:
      self._transactions = phab.maniphest.gettasktransactions(ids=[int(self.id)]).response[self.id]
    return self._transactions


class Project(object):
  def __init__(self, **fields):
    self.__dict__.update(fields)
