# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Consultation(models.Model):
    consultation_id = models.AutoField(primary_key=True)
    query = models.CharField(max_length=500)
    line_1 = models.IntegerField()
    chng_1 = models.IntegerField()
    line_2 = models.IntegerField()
    chng_2 = models.IntegerField()
    line_3 = models.IntegerField()
    chng_3 = models.IntegerField()
    line_4 = models.IntegerField()
    chng_4 = models.IntegerField()
    line_5 = models.IntegerField()
    chng_5 = models.IntegerField()
    line_6 = models.IntegerField()
    chng_6 = models.IntegerField()
    notes = models.CharField(max_length=500, blank=True, null=True)
    conclusion = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return "%d" % self.consultation_id + ":  " + self.query

    class Meta:
        managed = False
        db_table = 'consultation'


class HLinePosition(models.Model):
    h_line_position_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=45)
    meaning = models.CharField(max_length=500)

    class Meta:
        managed = False
        db_table = 'h_line_position'


class Trigram(models.Model):
    trigram_id = models.CharField(primary_key=True, max_length=45)
    description = models.CharField(max_length=500)

    class Meta:
        managed = False
        db_table = 'trigram'


class Hexagram(models.Model):
    hexagram_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=45)
    description = models.CharField(max_length=10000)
    upper_trigram = models.ForeignKey('Trigram', models.DO_NOTHING, db_column='upper_trigram', related_name='ut')
    lower_trigram = models.ForeignKey('Trigram', models.DO_NOTHING, db_column='lower_trigram', related_name='lt')

    class Meta:
        managed = False
        db_table = 'hexagram'


class Line(models.Model):
    line_id = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=500)

    class Meta:
        managed = False
        db_table = 'line'


class HexagramLine(models.Model):
    hexagram_line_id = models.IntegerField(primary_key=True)
    hexagram = models.ForeignKey(Hexagram, models.DO_NOTHING, db_column='hexagram', related_name='h')
    h_line_position = models.ForeignKey(HLinePosition, models.DO_NOTHING, db_column='h_line_position')
    line = models.ForeignKey('Line', models.DO_NOTHING, db_column='line')
    translation = models.CharField(max_length=500)
    commentary = models.CharField(max_length=1000)
    related_hexagram = models.ForeignKey(Hexagram, models.DO_NOTHING, db_column='related_hexagram', related_name='rh')

    class Meta:
        managed = False
        db_table = 'hexagram_line'
        unique_together = (('hexagram', 'h_line_position'),)


class LineChanges(models.Model):
    line_changes_id = models.IntegerField(primary_key=True)
    line_1 = models.IntegerField()
    line_2 = models.IntegerField()
    line_3 = models.IntegerField()
    line_4 = models.IntegerField()
    line_5 = models.IntegerField()
    line_6 = models.IntegerField()
    chng_1 = models.IntegerField()
    chng_2 = models.IntegerField()
    chng_3 = models.IntegerField()
    chng_4 = models.IntegerField()
    chng_5 = models.IntegerField()
    chng_6 = models.IntegerField()
    hexagram = models.ForeignKey(Hexagram, models.DO_NOTHING, db_column='hexagram')

    class Meta:
        managed = False
        db_table = 'line_changes'
        unique_together = (('line_1', 'line_2', 'line_3', 'line_4', 'line_5', 'line_6', 'chng_1', 'chng_2', 'chng_3', 'chng_4', 'chng_5', 'chng_6'),)


class Pair(models.Model):
    hexagram1_id = models.ForeignKey(Hexagram, models.DO_NOTHING, primary_key=True, related_name='h1')
    hexagram2 = models.ForeignKey(Hexagram, models.DO_NOTHING, db_column='hexagram2', related_name='h2')

    class Meta:
        managed = False
        db_table = 'pair'
        unique_together = (('hexagram1_id', 'hexagram2'),)


class TrigramLine(models.Model):
    trigram_line_id = models.IntegerField(primary_key=True)
    trigram = models.ForeignKey(Trigram, models.DO_NOTHING, db_column='trigram')
    t_line_position = models.IntegerField()
    line = models.ForeignKey(Line, models.DO_NOTHING, db_column='line')

    class Meta:
        managed = False
        db_table = 'trigram_line'
        unique_together = (('trigram', 't_line_position'),)
