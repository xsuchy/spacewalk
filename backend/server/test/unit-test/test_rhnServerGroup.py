#!/usr/bin/python
#
# Copyright (c) 2008 Red Hat, Inc.
#
# This software is licensed to you under the GNU General Public License,
# version 2 (GPLv2). There is NO WARRANTY for this software, express or
# implied, including the implied warranties of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. You should have received a copy of GPLv2
# along with this software; if not, see
# http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt.
# 
# Red Hat trademarks are not licensed under GPLv2. No permission is
# granted to use or replicate Red Hat trademarks that are incorporated
# in this software or its documentation. 
#
#
#
#
# $Id$

import sys
import unittest
from server import rhnSQL, rhnServerGroup

import misc_functions

DB = 'rhnuser/rhnuser@webdev'
    

class Tests(unittest.TestCase):

    def setUp(self):
        rhnSQL.initDB(DB)

    def tearDown(self):
        # Roll back any unsaved data
        rhnSQL.rollback()

    def test_new_org_1(self):
        org_id = misc_functions.create_new_org()
        # PGPORT_1:NO Change #
        h = rhnSQL.prepare("select id from web_customer where id = :id")
        h.execute(id=org_id)
        row = h.fetchone_dict()
        self.assertNotEqual(row, None)
        self.assertEqual(row['id'], org_id)

    def test_new_server_group_new_org_1(self):
        org_id = misc_functions.create_new_org()
        params = misc_functions.build_server_group_params(org_id=org_id)

        misc_functions.create_server_group(params)
        
        s = misc_functions.fetch_server_group(params['org_id'], params['name'])
        self.assertEqual(s.get_name(), params['name'])
        self.assertEqual(s.get_description(), params['description'])
        self.assertEqual(s.get_max_members(), params['max_members'])

    def test_exception_user_missing_1(self):
        params = misc_functions.build_server_group_params(org_id="no such user")
        self.assertRaises(rhnServerGroup.InvalidUserError,
            misc_functions.create_server_group, params)

    def test_exception_org_missing_1(self):
        params = misc_functions.build_server_group_params(org_id=-1)
        self.assertRaises(rhnServerGroup.InvalidOrgError,
            misc_functions.create_server_group, params)


if __name__ == '__main__':
    sys.exit(unittest.main() or 0)
