import cassiopeia
from db_connector import db
from cassiopeia import Patch, Summoner


def update_champions(db: db):
    db.clear_champions()
    champions = cassiopeia.get_champions(region='EUW')
    for champ in champions:
        db.add_champion(id=champ.id, name=champ.name,
                        icon_path=champ.image.url)


def update_summoner_spells(db: db):
    db.clear_summoner_spells()
    summoner_spells = cassiopeia.get_summoner_spells(region='EUW')
    for spell in summoner_spells:
        db.add_summoner_spell(
            id=spell.id, name=spell.name, icon_path=spell.image.url)


def update_items(db: db):
    db.clear_items()
    items = cassiopeia.get_items(region='EUW')
    for item in items:
        db.add_item(id=item.id, name=item.name, icon_path=item.image.url)


def update_summoner_icons(db: db):
    db.clear_summoner_icons()
    icons = cassiopeia.get_profile_icons(region='EUW')
    for icon in icons:
        db.add_summoner_icon(id=icon.id, icon_path=icon.url)
