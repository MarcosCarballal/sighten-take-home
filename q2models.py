# apps/project/models.py
from django.db import models

class Project(models.Model):
   name = models.CharField(max_length=64)
   # This is a one - to one relationship.
   generation_project = models.OneToOneField(
       'project.GenerationProject',
       related_name='project',
       null=True,
       blank=True,
   )

# Has 1-1 rel with Project
class GenerationProject(models.Model):
   capacity = models.FloatField(default=0)
   input_mode = models.CharField(
       max_length=10,
       choices=(
           ('RSD', 'Remote System Design'),
           ('OFFSET', 'Usage Offset'),
       ),
       default='RSD',
   )

class Quote(models.Model):
   project = models.ForeignKey(
       'project.Project',
       # Does this related name field allow me to use project.quotes to perform the reverse lookup?
       related_name='quotes',
   )
   install_cost = models.FloatField()

if __name__ == '__main__':
    print("hi")
    # qs = Quote.objects.all()