from django.db import models

# Create your models here.


class DoctorSpecialty(models.Model):

    id = models.AutoField(primary_key=True, db_column='id_espec')
    type = models.CharField(max_length=50, db_column='tipo_espec')

    class Meta:
        managed = True
        db_table = 'medico_especialidade'


class Doctor(models.Model):

    crm = models.CharField(primary_key=True, db_column='crm', max_length=7)
    name = models.CharField(max_length=50, db_column='nome_med')
    contact = models.CharField(max_length=14, db_column='contato_med')
    doctor_specialty = models.ForeignKey(DoctorSpecialty, db_column='id_espec', on_delete=models.PROTECT)

    class Meta:
        managed = True
        db_table = 'medico'


class Patient(models.Model):

    id = models.AutoField(primary_key=True, db_column='id_paciente')
    name = models.CharField(max_length=50, db_column='nome_pac')
    email = models.CharField(max_length=40, db_column='email_pac')
    birth_date = models.DateField(db_column='data_nasc')
    contact = models.CharField(max_length=14, db_column='contato_pac')
    uid = models.CharField(max_length=50, unique=True, db_column='uid')

    class Meta:
        managed = True
        db_table = 'paciente'


class Appointment(models.Model):

    id = models.AutoField(primary_key=True, db_column='id_consulta')
    title = models.CharField(max_length=50, db_column='titulo')
    date = models.DateField(db_column='data_consulta')
    symptom = models.CharField(max_length=240, db_column='sintoma')
    diagnosis = models.CharField(max_length=240, db_column='diagnostico')
    medication = models.CharField(max_length=240, db_column='medicacao')
    patient = models.ForeignKey(Patient, db_column='id_paciente', on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, db_column='crm', on_delete=models.PROTECT)

    class Meta:
        managed = True
        db_table = 'consulta'


class MedicalExam(models.Model):

    id = models.AutoField(primary_key=True, db_column='id_exame')
    file_path = models.CharField(max_length=250, db_column='path_file')
    creation_date = models.DateField(db_column='data_criacao')
    name = models.CharField(max_length=50, db_column='nome_exame')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, db_column='id_paciente')
    appointment = models.ForeignKey(Appointment, on_delete=models.DO_NOTHING, db_column='id_consulta', null=True)

    class Meta:
        managed = True
        db_table = 'exame'
