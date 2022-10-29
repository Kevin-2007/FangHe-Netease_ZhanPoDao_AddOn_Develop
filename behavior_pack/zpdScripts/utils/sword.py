# -*- coding=utf-8 -*-
"""
    !  斩魄刀客户端接口类
"""

import mod.client.extraClientApi as clientApi

class SwordRender:
    def __init__(self):
        pass

    def ThirdItem3dRender(self):
        pass

    def FirstItem3DRender(self):
        pass

    def Animation(self):
        pass

    def Particle(self):
        pass
    


class Sword(object):

    def __init__(self, name, type, *args, **kwargs):
        pass

    @SwordRender.FirstItem3DRender()
    @SwordRender.ThirdItem3dRender()
    def BasicRender(self):
        pass
    
    @SwordRender.Animation()
    def Attack(self):
        pass

    @SwordRender.Animation()
    def Show(self):
        pass

