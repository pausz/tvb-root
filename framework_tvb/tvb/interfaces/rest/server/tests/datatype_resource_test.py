# -*- coding: utf-8 -*-
#
#
# TheVirtualBrain-Scientific Package. This package holds all simulators, and
# analysers necessary to run brain-simulations. You can use it stand alone or
# in conjunction with TheVirtualBrain-Framework Package. See content of the
# documentation-folder for more details. See also http://www.thevirtualbrain.org
#
# (c) 2012-2020, Baycrest Centre for Geriatric Care ("Baycrest") and others
#
# This program is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software Foundation,
# either version 3 of the License, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE.  See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this
# program.  If not, see <http://www.gnu.org/licenses/>.
#
#
#   CITATION:
# When using The Virtual Brain for scientific publications, please cite it as follows:
#
#   Paula Sanz Leon, Stuart A. Knock, M. Marmaduke Woodman, Lia Domide,
#   Jochen Mersmann, Anthony R. McIntosh, Viktor Jirsa (2013)
#       The Virtual Brain: a simulator of primate brain network dynamics.
#   Frontiers in Neuroinformatics (7:10. doi: 10.3389/fninf.2013.00010)
#
#

import os
import pytest
import tvb_data
from tvb.adapters.datatypes.db.connectivity import ConnectivityIndex
from tvb.interfaces.rest.server.resources.datatype.datatype_resource import RetrieveDatatypeResource, \
    GetOperationsForDatatypeResource
from tvb.interfaces.rest.server.resources.exceptions import InvalidIdentifierException
from tvb.interfaces.rest.server.resources.project.project_resource import GetDataInProjectResource
from tvb.tests.framework.core.base_testcase import TransactionalTestCase
from tvb.tests.framework.core.factory import TestFactory


class TestDatatypeResource(TransactionalTestCase):

    def transactional_setup_method(self):
        self.retrieve_resource = RetrieveDatatypeResource()
        self.get_operations_resource = GetOperationsForDatatypeResource()
        self.get_data_in_project_resource = GetDataInProjectResource()

    def test_server_retrieve_datatype_inexistent_gid(self):
        datatype_gid = "inexistent-gid"
        with pytest.raises(InvalidIdentifierException): self.retrieve_resource.get(datatype_gid)

    def test_server_retrieve_datatype(self):
        test_user = TestFactory.create_user('Rest_User')
        test_project_with_data = TestFactory.create_project(test_user, 'Rest_Project')
        zip_path = os.path.join(os.path.dirname(tvb_data.__file__), 'connectivity', 'connectivity_96.zip')
        TestFactory.import_zip_connectivity(test_user, test_project_with_data, zip_path)

        datatypes_in_project = self.get_data_in_project_resource.get(test_project_with_data.gid)
        assert type(datatypes_in_project) is list
        assert len(datatypes_in_project) == 1
        assert datatypes_in_project[0].type == ConnectivityIndex().display_type
        # TODO: finalize test and download file

    def test_server_get_operations_for_datatype(self):
        test_user = TestFactory.create_user('Rest_User')
        test_project_with_data = TestFactory.create_project(test_user, 'Rest_Project')
        zip_path = os.path.join(os.path.dirname(tvb_data.__file__), 'connectivity', 'connectivity_96.zip')
        TestFactory.import_zip_connectivity(test_user, test_project_with_data, zip_path)

        datatypes_in_project = self.get_data_in_project_resource.get(test_project_with_data.gid)
        assert type(datatypes_in_project) is list
        assert len(datatypes_in_project) == 1
        assert datatypes_in_project[0].type == ConnectivityIndex().display_type

        result = self.get_operations_resource.get(datatypes_in_project[0].gid)
        assert type(result) is list
        assert len(result) > 3