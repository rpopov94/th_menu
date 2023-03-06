from django.db import models

class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='children')
    display_name = models.CharField(max_length=100)
    url = models.CharField(max_length=100, blank=True)
    order = models.IntegerField(default=0)

    def get_descendants(self):
        descendants = list(self.children.all())
        for child in descendants:
            descendants.extend(child.get_descendants())
        return descendants

    def __str__(self):
        return self.name

