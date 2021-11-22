# Generated by Django 3.2.8 on 2021-11-22 15:27

import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('user_type', models.PositiveSmallIntegerField(choices=[(1, 'student'), (2, 'placementOfficer'), (3, 'Company'), (4, 'Mentor'), (5, 'admin')], default=2)),
                ('verified', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Branch_Name', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='BranchDS',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Start_year', models.PositiveSmallIntegerField()),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='placementapp.branch')),
            ],
        ),
        migrations.CreateModel(
            name='Degree',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Degree_Name', models.CharField(max_length=40)),
                ('Degree_Duration', models.DecimalField(decimal_places=1, max_digits=2)),
                ('Total_Sem', models.PositiveIntegerField(blank=True, null=True)),
                ('Min_credit', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PlacementCell',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('University', models.CharField(default='MediCaps University', max_length=40)),
                ('phone_no', models.PositiveBigIntegerField(blank=True, null=True)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=60)),
                ('Location_Name', models.CharField(max_length=40)),
                ('Board', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='placementapp.user')),
                ('Name', models.CharField(max_length=60)),
                ('Description', models.TextField(blank=True, null=True)),
                ('MCA', models.CharField(blank=True, max_length=50, null=True, verbose_name='MCA ID')),
                ('Type', models.CharField(blank=True, max_length=70, null=True, verbose_name='Company Type')),
                ('Revenue', models.BigIntegerField(blank=True, null=True, verbose_name='Latest 1 year Revenue In Crore')),
            ],
        ),
        migrations.CreateModel(
            name='Mentor',
            fields=[
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('gender', models.CharField(choices=[('MALE', 'MALE'), ('FEMALE', 'FEMALE'), ('OTHERS', 'OTHERS')], max_length=10, null=True)),
                ('Email', models.EmailField(max_length=254)),
                ('Mobile_No', models.PositiveBigIntegerField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='placementapp.user')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=100)),
                ('minCTC', models.SmallIntegerField(verbose_name='Minimum CTC in Lakhs')),
                ('maxCTC', models.SmallIntegerField(verbose_name='Maximum CTC in Lakhs')),
                ('Description', models.TextField(verbose_name='Roles and Responsibility')),
                ('minScore10', models.DecimalField(decimal_places=2, default=0.0, max_digits=4)),
                ('minScore12', models.DecimalField(decimal_places=2, default=0.0, max_digits=4)),
                ('minJeePercentile', models.DecimalField(decimal_places=2, default=0.0, max_digits=4)),
                ('Time', models.DateTimeField(blank=True, null=True, verbose_name='Apply By')),
                ('visible', models.BooleanField(default=False, verbose_name='Visible to Student')),
                ('branch', models.ManyToManyField(to='placementapp.BranchDS')),
                ('Company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='placementapp.company')),
            ],
        ),
        migrations.CreateModel(
            name='Offers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Description', models.TextField(verbose_name='Extra Info About offer')),
                ('FinalCTC', models.SmallIntegerField()),
                ('Position', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='placementapp.position')),
            ],
        ),
        migrations.AddField(
            model_name='branchds',
            name='degree',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='placementapp.degree'),
        ),
        migrations.AddField(
            model_name='branch',
            name='Degree',
            field=models.ManyToManyField(through='placementapp.BranchDS', to='placementapp.Degree'),
        ),
        migrations.CreateModel(
            name='Applied',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Status', models.CharField(choices=[('Selected', 'Selected'), ('EligibleForNextRound', 'EligibleForNextRound'), ('Rejected', 'Not Eligible For Next Round'), ('Under Evaluation', 'Under Evaluation')], default='UnderEvaluation', max_length=30)),
                ('Time', models.DateTimeField(auto_now_add=True, verbose_name='applied at')),
                ('Description', models.TextField(blank=True, null=True, verbose_name='Info About Next Roumd')),
                ('FinalOffer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='placementapp.offers')),
                ('Position', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='placementapp.position')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='placementapp.user')),
                ('enrollment_no', models.CharField(max_length=12)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('gender', models.CharField(choices=[('MALE', 'MALE'), ('FEMALE', 'FEMALE'), ('OTHERS', 'OTHERS')], max_length=10, null=True)),
                ('Email', models.EmailField(max_length=254)),
                ('Mobile_No', models.PositiveBigIntegerField()),
                ('Score10', models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True, verbose_name='Grade 10 percentage')),
                ('Score12', models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True, verbose_name='Grade 12 Percentage')),
                ('JeePercentile', models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True)),
                ('Aim', models.TextField(blank=True, null=True)),
                ('Objective', models.TextField(blank=True, null=True)),
                ('Mission', models.TextField(blank=True, null=True)),
                ('Vision', models.TextField(blank=True, null=True)),
                ('maxCTC', models.SmallIntegerField(default=0, null=True)),
                ('Resume', models.FileField(blank=True, upload_to='Resume')),
                ('ResumeURL', models.TextField(blank=True, null=True)),
                ('AppliedPositions', models.ManyToManyField(through='placementapp.Applied', to='placementapp.Position')),
                ('Branch', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='placementapp.branchds')),
                ('PlacementCell', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='placementapp.placementcell')),
                ('School10', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='SchoolX', to='placementapp.school')),
                ('School12', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='SchoolXII', to='placementapp.school')),
                ('mentor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='placementapp.mentor')),
            ],
        ),
        migrations.CreateModel(
            name='PlacementOfficer',
            fields=[
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('gender', models.CharField(choices=[('MALE', 'MALE'), ('FEMALE', 'FEMALE'), ('OTHERS', 'OTHERS')], max_length=10, null=True)),
                ('Email', models.EmailField(max_length=254)),
                ('Mobile_No', models.PositiveBigIntegerField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='placementapp.user')),
                ('placementCell', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='placementapp.placementcell')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MessageP2S',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('TimeStamps', models.DateTimeField()),
                ('Body', models.TextField()),
                ('type', models.CharField(blank=True, max_length=40, null=True)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='placementapp.placementcell')),
                ('receivers', models.ManyToManyField(to='placementapp.Student')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MessageP2C',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('TimeStamps', models.DateTimeField()),
                ('Body', models.TextField()),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='placementapp.placementcell')),
                ('receivers', models.ManyToManyField(to='placementapp.Company')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MessageC2P',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('TimeStamps', models.DateTimeField()),
                ('Body', models.TextField()),
                ('receivers', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='placementapp.placementcell')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='placementapp.company')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='applied',
            name='Student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='placementapp.student'),
        ),
    ]
