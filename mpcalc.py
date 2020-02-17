import requests
import pprint
import spreadsheet
from enum import IntFlag

API_KEY = "5954bb11ac6d667229f2bdecea9c2bfd7ff65aad"
PLAYERS = {}
TAB = ''
Tabs = ["'YEET'",
        "'Ted'",
        "'HC2'",
        "'OWC2019'",
        "'LC2'",
        "'DBHT'",
        "'UFRJD'"]
class Mod(IntFlag):
    NoMod = 0
    NF = 1
    EZ = 2
    TD = 4
    HD = 8
    HR = 16
    SD = 32
    DT = 64
    RX = 128
    HT = 256
    NC = 512
    FL = 1024
    Autoplay = 2048
    SO = 4096
    AP = 8192
    PF = 16384
    Key4 = 32768
    Key5 = 65536
    Key6 = 131072
    Key7 = 262144
    Key8 = 524288
    FadeIn = 1048576
    Random = 2097152
    Cinema = 4194304
    Target = 8388608
    Key9 = 16777216
    KeyCoop = 33554432
    Key1 = 67108864
    Key3 = 134217728
    Key2 = 268435456
    ScoreV2 = 536870912
    Mirror = 1073741824
    HDHR = HD|HR
    HDNF = HD|NF
    EZHD = EZ|HD
    EZNF = EZ|NF
    HRNF = HR|NF
    NFHDHR = NF|HD|HR
    NFDT= NF|DT
    HRSD = HR|SD
    HDSD = HD|SD
    HDHRSD = HD|HR|SD
    HDFL = HD|FL
    HRFL = HR|FL
    HDHRFL = HD|HR|FL
    HDRX = HD|RX
    HRRX = HR|RX
    HDHRRX = HD|HR|RX
    HDSO = HD|SO
    EZHDSO = EZ|HD|SO
    HRSO = HR|SO
    HDHRSO = HD|HR|SO
    HDHT = HD|HT
    HRHT = HR|HT
    HDHRHT = HD|HR|HT
    HRDT = HR|DT
    HDPF = HD|PF
    HRPF = HR|PF
    HDHRPF = HD|HR|PF

def get_mp_data(link: str):
    url = 'https://osu.ppy.sh/api/get_match'
    mp = ''
    for character in link:
        if character.isdigit():
            mp += character
    url = url + '?mp=' + mp + '&k=' + API_KEY
    response = requests.get(url)
    return response.json()

def get_username(player_id: str):
    url = 'https://osu.ppy.sh/api/get_user'
    u = player_id
    m = 0
    type = 'id'
    url = url + '?u=' + u + '&m=' + str(m) + '&type=' + type + '&k=' + API_KEY
    response = requests.get(url)
    return response.json()[0]['username']

def get_userid(player: str):
    url = 'https://osu.ppy.sh/api/get_user'
    u = player
    m = 0
    type = 'string'
    url = url + '?u=' + u + '&m=' + str(m) + '&type=' + type + '&k=' + API_KEY
    response = requests.get(url)
    return response.json()[0]['user_id']

def get_beatmaptitle(mapid: str):
    url = "https://osu.ppy.sh/api/get_beatmaps?k=" + API_KEY + "&b=" + mapid
    response = requests.get(url)
    artist = response.json()[0]['artist']
    difficulty = response.json()[0]['version']
    title = artist + ' - ' + response.json()[0]['title'] + ' ['+difficulty+']'

    return title
def get_map_data(mapid: str):
    url = "https://osu.ppy.sh/api/get_beatmaps?k=" + API_KEY + "&b=" + mapid
    response = requests.get(url)

    return response.json()[0]

def get_colon_index(json: dict):
    colon_index = len(json['match']['name'])
    for h in range(len(json['match']['name'])):
        if json['match']['name'][h] == ':':
            colon_index = h
            break
    return colon_index

def get_mappool(json: dict):
    matches = 0
    final_mappool = []
    if ':' in json['match']['name']:
        colon_index = get_colon_index(json)
        tab = "'" + json['match']['name'][:colon_index] + "'"
        TAB = tab
        map_ids = spreadsheet.get_sheet_values(TAB)
        for game in json['games']:
            for pool in map_ids:
                if game['beatmap_id'] in pool:
                    matches += 1
                    if matches == 3:
                        final_mappool = pool
                        break
        map_ids = final_mappool
    else:
        for sheet in Tabs:
            map_ids = spreadsheet.get_sheet_values(sheet)
            for game in json['games']:
                for pool in map_ids:
                    if game['beatmap_id'] in pool:
                        matches += 1
                        if matches == (len(json['games']))-2:
                            final_mappool = pool
                            break
            map_ids = final_mappool
    return map_ids

def get_user_team(json: dict, player_id: str):
    team = ''
    for game in json['games']:
        if game['team_type'] == '2':
            for score in game['scores']:
                if score['user_id'] == player_id:
                    team = (score['team'])
    return team

def get_player_score(json: dict, returning_total: bool, data: bool, searching_map: bool, player_id='', map=''):
    if player_id != '':
        player = get_username(player_id)
    map_scores = {}
    total_score = 0
    mods = None
    map_ids = get_mappool(json)

    for game in json['games']:
        if searching_map:
            if map == game['beatmap_id']:
                for score in game['scores']:
                    if score['user_id'] not in map_scores:
                        if score['enabled_mods'] != None:
                            mods = score['enabled_mods']
                        elif game['mods'] == '0':
                            mods = None
                        else:
                            mods = game['mods']
                        map_scores[score['user_id']] = {'score': score['score'],
                                                        '300': score['count300'],
                                                        '100': score['count100'],
                                                        '50': score['count50'],
                                                        'miss': score['countmiss'],
                                                        'combo': score['maxcombo'],
                                                        'mods': mods,
                                                        'map': map,
                                                        'team': get_user_team(json, score['user_id']),
                                                        'id': score['user_id']
                                                        }
        else:
            for score in game['scores']:
                if player_id == score['user_id']:
                    if game['beatmap_id'] in map_scores and game['beatmap_id'] in map_ids:
                        if returning_total and int(score['score']) > int(map_scores[game['beatmap_id']]):
                            map_scores[game['beatmap_id']] = score['score']
                        elif data and int(score['score']) > int(map_scores[game['beatmap_id']]['score']):
                            if score['enabled_mods'] != None:
                                mods = score['enabled_mods']
                            elif game['mods'] == '0':
                                mods = None
                            else:
                                mods = game['mods']
                            map_scores[game['beatmap_id']] = {'score': score['score'],
                                                              '300': score['count300'],
                                                              '100': score['count100'],
                                                              '50': score['count50'],
                                                              'miss': score['countmiss'],
                                                              'combo': score['maxcombo'],
                                                              'mods': mods,
                                                              }
                            mods = None
                    elif game['beatmap_id'] in map_ids:
                        map_scores[game['beatmap_id']] = score['score']
                        if data:
                            if score['enabled_mods'] != None:
                                mods = score['enabled_mods']
                            elif game['mods'] == '0':
                                mods = None
                            else:
                                mods = game['mods']
                            map_scores[game['beatmap_id']] = {'score': score['score'],
                                                              '300': score['count300'],
                                                              '100': score['count100'],
                                                              '50': score['count50'],
                                                              'miss': score['countmiss'],
                                                              'combo': score['maxcombo'],
                                                              'mods': mods,
                                                              }
                            mods = None
    if returning_total:
        for id in map_ids:
            if id in map_scores:
                total_score += int(map_scores[id])
        return {player: str(total_score)}
    else:
        return map_scores

