# Generated manually

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webAMG', '0002_rename_beneficiari_created_2bc39f_idx_beneficiari_created_266432_idx_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PhaseEvidence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(blank=True, db_column='created_by', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('phase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='evidences', to='webAMG.projectphase')),
            ],
            options={
                'verbose_name': 'Evidencia de Fase',
                'verbose_name_plural': 'Evidencias de Fases',
                'db_table': 'phase_evidences',
                'indexes': [
                    models.Index(fields=['phase'], name='phase_evide_phase_i_0762af_idx'),
                    models.Index(fields=['start_date', 'end_date'], name='phase_evide_start_d_ddba2a_idx'),
                    models.Index(fields=['created_by'], name='phase_evide_created_62360a_idx'),
                ],
            },
        ),
        migrations.CreateModel(
            name='PhaseEvidencePhoto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo_url', models.TextField()),
                ('caption', models.TextField(blank=True, null=True)),
                ('photo_order', models.IntegerField(default=1)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('phase_evidence', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='webAMG.phaseevidence')),
                ('uploaded_by', models.ForeignKey(blank=True, db_column='uploaded_by', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Foto de Evidencia de Fase',
                'verbose_name_plural': 'Fotos de Evidencias de Fases',
                'db_table': 'phase_evidence_photos',
                'indexes': [
                    models.Index(fields=['phase_evidence'], name='phase_evide_phase_e_47e8c2_idx'),
                    models.Index(fields=['uploaded_by'], name='phase_evide_uploade_e14f4b_idx'),
                    models.Index(fields=['uploaded_at'], name='phase_evide_uploade_d8db20_idx'),
                ],
            },
        ),
        migrations.CreateModel(
            name='PhaseEvidenceBeneficiary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assigned_at', models.DateTimeField(auto_now_add=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('beneficiary', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='phase_evidence_participations', to='webAMG.beneficiary')),
                ('phase_evidence', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='beneficiaries', to='webAMG.phaseevidence')),
            ],
            options={
                'verbose_name': 'Beneficiario de Evidencia de Fase',
                'verbose_name_plural': 'Beneficiarios de Evidencias de Fases',
                'db_table': 'phase_evidence_beneficiaries',
                'indexes': [
                    models.Index(fields=['phase_evidence'], name='phase_evide_phase_e_a63674_idx'),
                    models.Index(fields=['beneficiary'], name='phase_evide_benefic_2e1a96_idx'),
                    models.Index(fields=['assigned_at'], name='phase_evide_assigne_8ca03a_idx'),
                ],
                'unique_together': {('phase_evidence', 'beneficiary')},
            },
        ),
    ]
