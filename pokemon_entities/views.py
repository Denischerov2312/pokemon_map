import folium

from django.shortcuts import render
from django.utils.timezone import localtime
from django.shortcuts import get_object_or_404

from pokemon_entities.models import Pokemon
from pokemon_entities.models import PokemonEntity


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def check_img_url(url):
    if url:
        return url
    return DEFAULT_IMAGE_URL


def show_all_pokemons(request):
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    local_time = localtime()
    entities = PokemonEntity.objects.filter(disappeared_at__gt=local_time, appeared_at__lt=local_time)
    for entity in entities:
        add_pokemon(
            folium_map, entity.lat,
            entity.lon,
            request.build_absolute_uri(entity.pokemon.image.url)
        )

    pokemons_on_page = []
    pokemons = Pokemon.objects.all()
    for pokemon in pokemons:
        img = pokemon.image
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': request.build_absolute_uri(check_img_url(img.url)),
            'title_ru': pokemon.title_ru,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    requested_pokemon = get_object_or_404(Pokemon, id=pokemon_id)
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in PokemonEntity.objects.filter(pokemon=requested_pokemon):
        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.lon,
            request.build_absolute_uri(requested_pokemon.image.url)
        )

    pokemon = {
        'img_url': check_img_url(requested_pokemon.image.url),
        'description': requested_pokemon.description,
        'title_ru': requested_pokemon.title_ru,
        'title_en': requested_pokemon.title_en,
        'title_jp': requested_pokemon.title_jp,
        'pokemon_id': requested_pokemon.id,
    }
    previous_pokemon = requested_pokemon.previous_evolution
    if previous_pokemon:
        pokemon['previous_evolution'] = {
            'title_ru': previous_pokemon.title_ru,
            'pokemon_id': previous_pokemon.id,
            'img_url': check_img_url(previous_pokemon.image.url),
        }
    next_pokemon = requested_pokemon.next_evolutions.first()
    if next_pokemon:
        pokemon['next_evolutions'] = {
            'title_ru': next_pokemon.title_ru,
            'pokemon_id': next_pokemon.id,
            'img_url': check_img_url(next_pokemon.image.url),
        }

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon
    })
