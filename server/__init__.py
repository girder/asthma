#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
#  Copyright 2015 Kitware Inc.
#
#  Licensed under the Apache License, Version 2.0 ( the "License" );
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
###############################################################################
import json
from girder import constants
from girder.api import access
from girder.api.rest import Resource, loadmodel
from girder.api.describe import Description
from girder.constants import AccessType
from girder.utility.model_importer import ModelImporter


PATIENT_FIELD = 'patient'


class Patient(Resource):

    @access.public
    @loadmodel(model='user', level=AccessType.WRITE)
    def setUserPatient(self, user, params):
        self.requireParams((PATIENT_FIELD, ), params)
        patient = params[PATIENT_FIELD]
        user[PATIENT_FIELD] = json.loads(patient)
        self.model('user').save(user, validate=False)
        return self.model('user').filter(user, self.getCurrentUser())
    setUserPatient.description = (
        Description('Set patient property for the user.')
        .param('id', 'The user ID', paramType='path')
        .param('patient', 'json document holding patient values.',
               required=True, dataType='json')
        .errorResponse('ID was invalid.')
        .errorResponse('Write permission denied on the user.', 403))


def load(info):
    patient = Patient()
    info['apiRoot'].user.route('PUT', (':id', 'patient'),
                               patient.setUserPatient)
    ModelImporter.model('user').exposeFields(
        level=constants.AccessType.READ, fields=[PATIENT_FIELD])
