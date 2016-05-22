import datetime
from django.db import models

from game_app.utils import remove_tags


class Platform(models.Model):
    platform_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    api_detail_url = models.URLField(blank=True, null=True)
    giant_bomb_site_detail_url = models.URLField(blank=True, null=True)
    abbr = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name \
            if self.name \
            else 'Missing name, platform_id: {}'.format(self.platform_id)


class Game(models.Model):
    game_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    aliases = models.CharField(max_length=255, blank=True, null=True)
    api_detail_url = models.URLField(blank=True, null=True)
    giant_bomb_site_detail_url = models.URLField(blank=True, null=True)
    summary = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    number_of_user_reviews = models.IntegerField(default=0)
    original_release_date = models.DateTimeField(blank=True, null=True)
    date_added = models.DateTimeField(blank=True, null=True)
    date_last_updated = models.DateTimeField(blank=True, null=True)
    resource_type = models.CharField(max_length=255, blank=True, null=True)
    platforms = models.ManyToManyField(
        Platform, blank=True, related_name='game_platforms')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name \
            if self.name else 'Missing name, game_id: {}'.format(self.game_id)

    def update_game(self, dict_data):
        self.name = dict_data.get('name')
        self.aliases = dict_data.get('aliases')
        self.api_detail_url = dict_data.get('api_detail_url')
        self.giant_bomb_site_detail_url = dict_data.get('site_detail_url')
        self.summary = dict_data.get('deck')
        self.description = remove_tags(dict_data.get('description'))

        if dict_data.get('number_of_user_reviews'):
            self.number_of_user_reviews = dict_data.get(
                'number_of_user_reviews')

        if dict_data.get('original_release_date'):
            self.original_release_date = datetime.datetime.strptime(
                dict_data.get('original_release_date'), '%Y-%m-%d %H:%M:%S')
        if dict_data.get('date_added'):
            self.date_added = datetime.datetime.strptime(
                dict_data.get('date_added'), '%Y-%m-%d %H:%M:%S')
        if dict_data.get('date_last_updated'):
            self.date_last_updated = datetime.datetime.strptime(
                dict_data.get('date_last_updated'), '%Y-%m-%d %H:%M:%S')
        self.resource_type = dict_data.get('resource_type')
        self.save()

        # if there is image info
        if dict_data.get('image'):
            for k, v in dict_data.get('image').items():
                Image.objects.get_or_create(game=self, title=k, url=v)

        # if there are platforms info
        if dict_data.get('platforms'):
            for p in dict_data.get('platforms'):
                p_obj, created = Platform.objects.get_or_create(
                    platform_id=p.get('id'))
                p_obj.name = p.get('name')
                p_obj.api_detail_url = p.get('api_detail_url')
                p_obj.abbr = p.get('abbreviation')
                p_obj.giant_bomb_site_detail_url = p.get('site_detail_url')
                p_obj.save()
                self.platforms.add(p_obj)
                self.save()

        self.save()


class Image(models.Model):
    game = models.ForeignKey(Game, related_name='image_game')
    url = models.URLField()
    title = models.CharField(max_length=255)

    class Meta:
        unique_together = ['game', 'url', 'title']

    def __str__(self):
        return '{} - {}: {}'.format(self.game, self.title, self.url)





