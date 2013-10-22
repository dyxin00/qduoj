# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'User'
        db.create_table(u'oj_user', (
            ('user_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nick', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
            ('isManager', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('website', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('ac', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('submit', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('rank', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'oj', ['User'])

        # Adding model 'Problem'
        db.create_table(u'oj_problem', (
            ('problem_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('input_data', self.gf('django.db.models.fields.TextField')()),
            ('output_data', self.gf('django.db.models.fields.TextField')()),
            ('sample_input', self.gf('django.db.models.fields.TextField')()),
            ('sameple_output', self.gf('django.db.models.fields.TextField')()),
            ('source', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('hint', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('in_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('time_limit', self.gf('django.db.models.fields.IntegerField')()),
            ('memory_limit', self.gf('django.db.models.fields.IntegerField')()),
            ('hard', self.gf('django.db.models.fields.IntegerField')()),
            ('accepted', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('submit', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('visible', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('oi_mode', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('content_file', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'oj', ['Problem'])

        # Adding model 'Solution'
        db.create_table(u'oj_solution', (
            ('solution_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('problem', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['oj.Problem'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['oj.User'])),
            ('score', self.gf('django.db.models.fields.FloatField')(default=0.0)),
            ('time', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('memory', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('in_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('result', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('language', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('judgetime', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('code_length', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'oj', ['Solution'])

        # Adding model 'Source_code'
        db.create_table(u'oj_source_code', (
            ('solution_id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'oj', ['Source_code'])

        # Adding model 'Compileinfo'
        db.create_table(u'oj_compileinfo', (
            ('solution_id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('error', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'oj', ['Compileinfo'])

        # Adding model 'LoginLog'
        db.create_table(u'oj_loginlog', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['oj.User'])),
            ('ip', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
            ('time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'oj', ['LoginLog'])

        # Adding model 'News'
        db.create_table(u'oj_news', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.TextField')()),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('visible', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'oj', ['News'])

        # Adding model 'Mail'
        db.create_table(u'oj_mail', (
            ('mail_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('mail_to', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('mail_from', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('title', self.gf('django.db.models.fields.TextField')()),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('is_new', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('in_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('reply', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
        ))
        db.send_create_signal(u'oj', ['Mail'])

        # Adding model 'Bbs'
        db.create_table(u'oj_bbs', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('problem', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['oj.Problem'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['oj.User'])),
            ('time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('reply_id', self.gf('django.db.models.fields.IntegerField')()),
            ('stairs', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'oj', ['Bbs'])

        # Adding model 'Runtimeinfo'
        db.create_table(u'oj_runtimeinfo', (
            ('solution_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('error', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'oj', ['Runtimeinfo'])


    def backwards(self, orm):
        # Deleting model 'User'
        db.delete_table(u'oj_user')

        # Deleting model 'Problem'
        db.delete_table(u'oj_problem')

        # Deleting model 'Solution'
        db.delete_table(u'oj_solution')

        # Deleting model 'Source_code'
        db.delete_table(u'oj_source_code')

        # Deleting model 'Compileinfo'
        db.delete_table(u'oj_compileinfo')

        # Deleting model 'LoginLog'
        db.delete_table(u'oj_loginlog')

        # Deleting model 'News'
        db.delete_table(u'oj_news')

        # Deleting model 'Mail'
        db.delete_table(u'oj_mail')

        # Deleting model 'Bbs'
        db.delete_table(u'oj_bbs')

        # Deleting model 'Runtimeinfo'
        db.delete_table(u'oj_runtimeinfo')


    models = {
        u'oj.bbs': {
            'Meta': {'object_name': 'Bbs'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'problem': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['oj.Problem']"}),
            'reply_id': ('django.db.models.fields.IntegerField', [], {}),
            'stairs': ('django.db.models.fields.IntegerField', [], {}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['oj.User']"})
        },
        u'oj.compileinfo': {
            'Meta': {'object_name': 'Compileinfo'},
            'error': ('django.db.models.fields.TextField', [], {}),
            'solution_id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'})
        },
        u'oj.loginlog': {
            'Meta': {'object_name': 'LoginLog'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['oj.User']"})
        },
        u'oj.mail': {
            'Meta': {'object_name': 'Mail'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'in_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'is_new': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'mail_from': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'mail_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mail_to': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'reply': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.TextField', [], {})
        },
        u'oj.news': {
            'Meta': {'object_name': 'News'},
            'content': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.TextField', [], {}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        u'oj.problem': {
            'Meta': {'object_name': 'Problem'},
            'accepted': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'content_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'hard': ('django.db.models.fields.IntegerField', [], {}),
            'hint': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'in_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'input_data': ('django.db.models.fields.TextField', [], {}),
            'memory_limit': ('django.db.models.fields.IntegerField', [], {}),
            'oi_mode': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'output_data': ('django.db.models.fields.TextField', [], {}),
            'problem_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sameple_output': ('django.db.models.fields.TextField', [], {}),
            'sample_input': ('django.db.models.fields.TextField', [], {}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'submit': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'time_limit': ('django.db.models.fields.IntegerField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        u'oj.runtimeinfo': {
            'Meta': {'object_name': 'Runtimeinfo'},
            'error': ('django.db.models.fields.TextField', [], {}),
            'solution_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'oj.solution': {
            'Meta': {'object_name': 'Solution'},
            'code_length': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'in_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'judgetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'language': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'memory': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'problem': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['oj.Problem']"}),
            'result': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'score': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'solution_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'time': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['oj.User']"})
        },
        u'oj.source_code': {
            'Meta': {'object_name': 'Source_code'},
            'code': ('django.db.models.fields.TextField', [], {}),
            'solution_id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'})
        },
        u'oj.user': {
            'Meta': {'object_name': 'User'},
            'ac': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'isManager': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'nick': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'rank': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'submit': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'user_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'website': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['oj']