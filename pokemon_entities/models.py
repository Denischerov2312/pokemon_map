from django.db import models  # noqa F401


class Pokemon(models.Model):
    title = models.TextField(blank=True, null=True)
    title_en = models.TextField(blank=True, null=True)
    title_jp = models.TextField(blank=True, null=True)
    image = models.ImageField(blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    previous_evolution = models.ForeignKey(
        'self', related_name='next_evolution',
        null=True, blank=True,
        on_delete=models.CASCADE,
        )

    def __str__(self) -> str:
        return self.title


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    lat = models.FloatField()
    lon = models.FloatField()
    appeared_at = models.DateTimeField()
    disappeared_at = models.DateTimeField()
    level = models.IntegerField()
    health = models.IntegerField()
    strenght = models.IntegerField()
    defence = models.IntegerField()
    stamina = models.IntegerField()
