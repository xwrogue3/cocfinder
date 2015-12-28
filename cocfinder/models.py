from sqlalchemy import orm

from cocfinder import db


class ObjectDoesNotExist(Exception):
    pass


class Manager(object):
    '''
    Model manager
    '''
    pass


class TownHallLevelManager(Manager):

    def get(self, level):
        th = TownHallLevel.query.filter_by(level=level).first()
        if not th:
            raise ObjectDoesNotExist()
        return th

    def create(self, level):
        th = TownHallLevel(level)
        db.session.add(th)
        db.session.commit()
        return th

    def get_or_create(self, level):
        try:
            th = self.get(level)
        except:
            th = self.create(level)
            return (th, 1)
        else:
            return (th, 0)

    def delete(self, level):
        try:
            th = self.get(level)
        except ObjectDoesNotExist:
            return
        else:
            db.session.delete(th)
            db.session.commit()

class TownHallLevel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    level = db.Column(db.Integer)

    objects = TownHallLevelManager()

    def __init__(self, level):
        self.level = level

    def __repr__(self):
        return 'TH%d' % self.level

    def to_dict(self):
        return {'level': self.level}


class TrophyLeagueManager(Manager):

    def get_by_trophy(self, trophy):
        leagues = TrophyLeague.query.all()
        for league in leagues:
            if int(trophy) > league.lower and int(trophy) < league.upper:
                return league
        else:
            raise ObjectDoesNotExist()

    def get(self, league, level):
        tl = TrophyLeague.query.filter_by(league=league, level=level).first()
        if not tl:
            raise ObjectDoesNotExist()
        return tl

    def create(self, league, level, upper, lower, fallout):
        tl = TrophyLeague(league, level, upper, lower, fallout)
        db.session.add(tl)
        db.session.commit()
        return tl

    def get_or_create(self, league, level, upper, lower, fallout):
        try:
            tl = self.get(league, level)
        except ObjectDoesNotExist:
            tl = self.create(league, level, upper, lower, fallout)
            return (tl, 1)
        else:
            return (tl, 0)

    def delete(self, league, level):
        try:
            tl = self.get(league, level)
        except:
            return
        else:
            db.session.delete(tl)
            db.session.commit()


class TrophyLeague(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # bronze, silver, gold, crystal, etc.
    league = db.Column(db.String(50))
    # 0, 1, 2, 3
    level = db.Column(db.Integer)
    # Trophy ranges
    upper = db.Column(db.Integer)
    lower = db.Column(db.Integer)
    # Trophy value where a user will fall out of the trophy range
    fallout = db.Column(db.Integer)

    objects = TrophyLeagueManager()

    def __init__(self, league, level, upper, lower, fallout):
        self.league = league.lower()
        self.level = level
        self.upper = upper
        self.lower = lower
        self.fallout = fallout

    def __repr__(self):
        if self.level:
            return '%s%d' % (self.league, self.level)
        else:
            # There is no level, like Legends
            return self.league

    def to_dict(self):
        return {'league': self.league,
                'level': self.level,
                'upper': self.upper,
                'lower': self.lower,
                'fallout': self.fallout}


class BaseManager(Manager):

    def get(self, id):
        base = Base.query.get(id)
        if not base:
            raise ObjectDoesNotExist()
        return base

    def create(self, th, gold, elixir, de, found_league, found_th):
        base = Base(th, gold, elixir, de, found_league, found_th)
        db.session.add(base)
        db.session.commit()
        return base

    def delete(self, id):
        try:
            base = self.get(id)
        except:
            return
        else:
            db.session.delete(base)
            db.session.commit()


class Base(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gold = db.Column(db.Integer)
    elixir = db.Column(db.Integer)
    de = db.Column(db.Integer)

    # Foreign Keys
    found_league_id = db.Column(db.Integer, db.ForeignKey('trophy_league.id'))
    found_league = db.relationship('TrophyLeague',
                                   backref=db.backref('bases', lazy='dynamic'))
    found_th_id = db.Column(db.Integer, db.ForeignKey('town_hall_level.id'))
    found_th = db.relationship('TownHallLevel',
                               foreign_keys='Base.found_th_id',
                               backref=db.backref('finders', lazy='dynamic'))
    th_id = db.Column(db.Integer, db.ForeignKey('town_hall_level.id'))
    th = db.relationship('TownHallLevel',
                         foreign_keys='Base.th_id',
                         backref=db.backref('bases', lazy='dynamic'))

    objects = BaseManager()

    def __init__(self, th, gold, elixir, de, found_league, found_th):
        self.th = th
        self.gold = int(gold)
        self.elixir = int(elixir)
        self.de = int(de)
        self.found_league = found_league
        self.found_th = found_th

    def __repr__(self):
        return '%s (gold: %d, elixir: %d, de: %d)' % (str(self.th),
                                                      self.gold,
                                                      self.elixir,
                                                      self.de)

    def to_dict(self):
        return {'th': self.th.to_dict(),
                'gold': self.gold,
                'elixir': self.elixir,
                'de': self.de,
                'found_league': self.found_league.to_dict(),
                'found_th': self.found_th.to_dict()}
