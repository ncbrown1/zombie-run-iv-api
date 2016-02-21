from .. import ma
from ..models.score import Score


class ScoreSchema(ma.ModelSchema):

    class Meta:
        model = Score


score_schema = ScoreSchema()
scores_schema = ScoreSchema(many=True)
