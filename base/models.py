from django.db import models

class userdata(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20)
    worksite = models.CharField(max_length=30,null=True,blank=True)
    passwd = models.CharField(max_length=30)

    def newuseradd(name,worksite,passwd):
        userdata.objects.create(name=name,worklist=worksite,passwd=passwd)


    def updateworksite(id,worksite):
        user =userdata.objects.get(id=id)

        user.worksite = worksite
        user.save()

    def updatepasswd(id,oldpasswd, newpasswd):
        user = userdata.objects.get(id=id)

        if user.passwd == oldpasswd:
            user.passwd = newpasswd
            user.save()


    def selectuser(name,passwd):
        user = userdata.objects.filter(name=name)

        if len(user) == 1:
            result = userdata.checkpasswd(user[0].id,passwd)
        else:
            result = []
            for i in range(len(user)):
                result.append(user[i].name)
        return result

    def checkpasswd(id,passwd):
        user = userdata.objects.get(id=id)
        if user.passwd == passwd:
            result = {
                'check':True,
                'name':user.name,
                'worksite':user.worksite
            }
        else:
            result = {
                'check':False
            }
        return result

class worktiem(models.Model):
    name = models.CharField(models.ForeignKey(userdata, on_delete=models.CASCADE), max_length=20)
    date = models.DateField()
    starth = models.IntegerField()
    startm = models.IntegerField()
    endh = models.IntegerField()
    endm = models.IntegerField()
    overtime = models.FloatField(max_length=8.1, null=True, blank=True)
    flag = models.BooleanField()

    

class Photo(models.Model):
    """写真"""
    file = models.ImageField('ファイル')