import bpy
from bpy.types import Node

import numpy as np
import time

from collections import deque

from .node_tree import AudioTreeNode
        


class DelayNode(Node, AudioTreeNode):
    '''Add a delayed echo to sound input'''
    
    def callback(self, socket, timeData, rate, length):

        inputData = self.inputs[0].getData(timeData, rate, length)[0].sum(axis=0)

        print(len(self.data[self.path_from_id()])*length)

        print(self.inputs[1].getData(timeData, rate, length)[0][0][0])

        self.data[self.path_from_id()].append(inputData)
        if int(len(self.data[self.path_from_id()])) > int(self.inputs[1].getData(timeData, rate, length)[0][0][0]/length):

            [self.data[self.path_from_id()].popleft() for _i in range(len(self.data[self.path_from_id()])-int(self.inputs[1].getData(timeData, rate, length)[0][0][0]*rate))]

        if int(len(self.data[self.path_from_id()])) < int(self.inputs[1].getData(timeData, rate, length)[0][0][0]/length):

            self.data[self.path_from_id()].append(inputData)
            return np.array([(inputData * 0.5, self.stamp[self.path_from_id()])])
        else:
            newData = self.data[self.path_from_id()].popleft()
            result = (newData + inputData) * 0.5
            self.data[self.path_from_id()].append(result)
            return np.array([(result * 0.5, self.stamp[self.path_from_id()])])
                    
    
    bl_idname = 'DelayNode'
    # Label for nice name display
    bl_label = 'Delay'
    
    data = {}
    stamp = {}

    def init(self, context):
        self.inputs.new('RawAudioSocketType', "Audio")
        self.inputs.new('RawAudioSocketType', "Delay")
        self.inputs[1].value_prop = 1.0
        self.outputs.new('RawAudioSocketType', "Audio")

        self.data[self.path_from_id()] = deque()
        self.stamp[self.path_from_id()] = time.time()
    
    
    def draw_buttons(self, context, layout):
        pass
    
   



def register():
    bpy.utils.register_module(__name__)


def unregister():
    bpy.utils.unregister_module(__name__)
