import yaml

from cocfinder.models import TrophyLeague

with open('trophyleagues.yaml') as f:
    tls = yaml.load(f.read())
    for tl in tls:
        TrophyLeague.objects.get_or_create(tl['league'],
                                           tl['level'],
                                           tl['upper'],
                                           tl['lower'],
                                           tl['fallout'])
