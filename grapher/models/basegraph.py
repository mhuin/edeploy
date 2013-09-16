#!/usr/bin/env python
#
# Copyright (C) 2013 eNovance SAS <licensing@enovance.com>
#
# Author: Matthieu Huin <mhu@enovance.com>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

"""Graph base class"""

import os
path = os.path.abspath(__file__)
localpath = os.path.dirname(path)


class BaseGraph(object):
    def __init__(self, template, data, keys):
        """@param template: a gnuplot template file used to draw the data.
           @param data: the data 
           @param keys: the keys to look for in the data handed over by eDeploy
           formatted as an "ordered" list (meaning order matters).
           Every entry matching the beginning of the keys will be used for
           generating the graph.
           Example: ('cpu', 'logical', 'bandwidth') will pick every bandwidth
           measurement for every logical cpu.
        """
        self.template = open(template, 'r').read()
        self.name = self.__class__.__name__
        self.data = self.prepare_data(data, keys)
        self.keys = keys
        
    def prepare_data(self, data, keys):
        """Format data to a usable form, if needed."""
        return data
    
    def __call__(self):
        """returns a gnuplot file that can be used to draw the graph."""
        raise NotImplementedError
        
