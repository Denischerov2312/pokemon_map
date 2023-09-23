from django.db import models  # noqa F401


class Pokemon(models.Model):
    title_ru = models.CharField(verbose_name='Название(rus)', max_length=20)
    title_en = models.CharField(null=True, verbose_name='Название(eng)', max_length=20)
    title_jp = models.CharField(null=True, verbose_name='Название(japan)', max_length=20)
    image = models.ImageField(verbose_name='Изображение')
    description = models.TextField(verbose_name='Описание')
    previous_evolution = models.ForeignKey(
        'self', related_name='next_evolutions',
        null=True, blank=True,
        on_delete=models.CASCADE,
        verbose_name='Прошлая эволюция'
        )

    def __str__(self) -> str:
        return self.title_ru


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, verbose_name='Покемон')
    lat = models.FloatField(verbose_name='Широта')
    lon = models.FloatField(verbose_name='Долгота')
    appeared_at = models.DateTimeField(verbose_name='Появился в')
    disappeared_at = models.DateTimeField(verbose_name='Исчез в')
    level = models.IntegerField(verbose_name='Уровень')
    health = models.IntegerField(verbose_name='Здоровье')
    strenght = models.IntegerField(verbose_name='Сила')
    defence = models.IntegerField(verbose_name='Защита')
    stamina = models.IntegerField(verbose_name='Выносливость')

    def __str__(self) -> str:
        return self.pokemon.title_ru
