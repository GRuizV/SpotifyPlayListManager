# from mongoengine import Document, StringField, ListField, FloatField, IntField, BooleanField

# class User(Document):
#     user_id = StringField(required=True, unique=True)
#     refresh_token = StringField(required=True, unique=True)
#     playlist_id = StringField()
#     last_updated = DateTimeField()
#     playlist_options = {
#         'seeds': ListField(StringField(), default=['ST', 'ST', 'MT', 'MT', 'MT']),
#         'acousticness': ListField(FloatField(), default=[10, 90]),
#         'danceability': ListField(FloatField(), default=[10, 90]),
#         'energy': ListField(FloatField(), default=[10, 90]),
#         'instrumentalness': ListField(FloatField(), default=[10, 90]),
#         'popularity': ListField(IntField(), default=[50, 100]),
#         'valence': ListField(FloatField(), default=[10, 90]),
#     }
#     stripe_id = StringField()
#     grandmothered = BooleanField(default=False)

#     meta = {'collection': 'users'}