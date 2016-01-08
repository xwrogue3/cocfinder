import json

from flask import abort, request, render_template
from flask.views import MethodView

from cocfinder import app
from cocfinder.models import Base, TownHallLevel, TrophyLeague


@app.route('/')
def main():
    return render_template('main.html')


class BaseView(MethodView):

    @app.route('/bases/')
    def list():
        bases = []
        for base in Base.query.all():
            if base:
                bases.append(base.to_dict())
        return json.dumps(bases)

# Need CRUD views for the bases


class StatsAPI(object):
    # Class to hold all our stats API views
    @app.route('/stats/avg')
    def averages():
        townhalls = TownHallLevel.query.all()
        averages = []
        entry = {}
        for tl in TrophyLeague.query.all():
            entry = {'league': str(tl),
                     'th': []}
            for th in townhalls:
                bases = Base.objects.by_league(tl, th=th)
                if bases:
                    gold, lix, de = Base.objects.avg_loot(bases)
                    entry['th'].append({
                        'townhall': th.level,
                        'avg_resources': {
                            'gold': gold,
                            'elixir': lix,
                            'de': de
                        }
                    })
            averages.append(entry)
        return json.dumps(averages)




class TrophyLeagueAPI(MethodView):

    def get(self, trophy_league_id):
        if trophy_league_id is None:
            tls = []
            for tl in TrophyLeague.query.all():
                tls.append(tl.to_dict())
            return json.dumps(tls)
        else:
            tl = TrophyLeague.query.get(trophy_league_id)
            if tl:
                return json.dumps(tl.to_dict())
            else:
                abort(404)

    def post(self):
        # create a new TrophyLeague
        return json.dumps(request.json)

    def delete(self, trophy_league_id):
        tl = TrophyLeague.query.get(trophy_league_id)
        TrophyLeague.objects.delete(league=tl.league, level=tl.level)

    def put(self, trophy_league_id):
        # Update a trophy league
        pass


class TownHallLevelAPI(MethodView):

    def get(self, town_hall_level_id):
        if town_hall_level_id is None:
            ths = []
            for th in TownHallLevel.query.all():
                ths.append(th.to_dict())
            return json.dumps(ths)
        else:
            th = TownHallLevel.query.get(town_hall_level_id)
            if th:
                return json.dumps(th.to_dict())
            else:
                abort(404)

    def post(self):
        # create new townhalls
        pass

    def delete(self, town_hall_level_id):
        th = TownHallLevel.query.get(town_hall_level_id)
        TrophyLeague.objects.delete(th.level)

    def put(self, town_hall_level_id):
        # Update a town hall level
        pass


def register_api(view, endpoint, url, pk='id', pk_type='int'):
    view_func = view.as_view(endpoint)
    app.add_url_rule(url, defaults={pk: None},
                     view_func=view_func, methods=['GET',])
    app.add_url_rule(url, view_func=view_func, methods=['POST',])
    app.add_url_rule('%s<%s:%s>' % (url, pk_type, pk), view_func=view_func,
                     methods=['GET', 'PUT', 'DELETE'])

register_api(TownHallLevelAPI, 'town_hall_level_api', '/townhalllevels/', pk='town_hall_level_id')
register_api(TrophyLeagueAPI, 'trophy_league_api', '/trophyleagues/', pk='trophy_league_id')

