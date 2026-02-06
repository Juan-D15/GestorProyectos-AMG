# Generated to sync with database

from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('webAMG', '0004_projectevidence_projectmaterial_and_more'),
    ]

    operations = [
        # Marcar la columna location de daily_activities como ya existente en la base de datos
        migrations.RunSQL(
            sql="-- Columna daily_activities.location ya existe en la base de datos, creada por BasedeDatos.txt"
        ),
        
        # Marcar las columnas created_by de las tablas que ya tienen ese campo
        migrations.RunSQL(
            sql="-- Columna project_beneficiaries.created_by ya existe"
        ),
        migrations.RunSQL(
            sql="-- Columna phase_beneficiaries.created_by ya existe"
        ),
        migrations.RunSQL(
            sql="-- Columna project_evidences.created_by ya existe"
        ),
        migrations.RunSQL(
            sql="-- Columna project_materials.created_by ya existe"
        ),
    ]
