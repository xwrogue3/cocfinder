from cocfinder import db


class TownHallLevel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    level = db.Column(db.Integer)

    def __init__(self, level):
        self.level = level

    def __repr__(self):
        return 'TH%d' % self.level


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

    def __init__(self, league, level, upper, lower, fallout):
        self.league = league
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
                               backref=db.backref('finders', lazy='dynamic'))
    th_id = db.Column(db.Integer, db.ForeignKey('town_hall_level.id'))
    th = db.relationship('TownHallLevel',
                         backref=db.backref('bases', lazy='dynamic'))

    def __init__(self, th, gold, elixir, de, found_league, found_th):
        self.th = th
        self.gold = gold
        self.elixir = elixir
        self.de = de
        self.found_league = found_league
        self.found_th = found_th

    def __repr__(self):
        return '%s (gold: %d, elixir: %d, de: %d)' % (self.th,
                                                      self.gold,
                                                      self.elixir,
                                                      self.de)

