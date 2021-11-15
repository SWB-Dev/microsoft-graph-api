import unittest

from msgraph import SharepointListItemBatchAction, SharepointGraphClient

class TestSharepointListItemBatchActions(unittest.TestCase):

    def setUp(self):
        self.client = SharepointGraphClient(None)
        self.base_uri = self.client.sites("ParentSite/ChildSite").lists("MyList").build_url()
        self.data = {
            "id":"",
            "body":{},
        }
        self.batch = SharepointListItemBatchAction(self.data.copy(), self.base_uri, self.client)

    def test_frontload_payload_adds_keys(self):
        control_dict = {"id":"","body":"","url":"","headers":"","method":""}
        data = self.data.copy()

        batch_keys = self.batch._build_payload(data).keys()
        control_keys = control_dict.keys()

        self.assertEqual(batch_keys, control_keys)
    
    def test_build_payload_raises_keyerror_with_body_id_key(self):
        data = self.data.copy()
        data['body']['id'] = 4

        with self.assertRaises(KeyError):
            self.batch._build_payload(data)
    
    def test_build_payload_raises_typeerror_with_non_dict_body_key(self):
        data = self.data.copy()
        data['body'] = ""

        with self.assertRaises(TypeError):
            self.batch._build_payload(data)   

class TestSharepointListItemBatchActionsPost(unittest.TestCase):

    def setUp(self):
        self.client = SharepointGraphClient(None)
        self.base_uri = self.client.sites("ParentSite/ChildSite").lists("MyList").build_url()
        self.post_data = {
            "id": 1,
            "body": {
                "fields": {
                    "field1":"value1"
                }
            }
        }
        self.batch = SharepointListItemBatchAction(self.post_data.copy(), self.base_uri, self.client)
        self.batch.method = "POST"
    
    def test_post_build_payload_raises_keyerror_without_fields_key(self):
        data = self.post_data.copy()
        data["body"] = {}

        with self.assertRaises(KeyError):
            self.batch._build_payload(data)
    
    def test_post_build_payload_succeeds(self):
        data = self.post_data.copy()
        control_dict = self.batch._frontload_payload(data.copy())

        payload = self.batch._build_payload(data)

        self.assertEqual(payload, control_dict)
    
    def test_post_uri_equals_base_uri(self):
        data = self.post_data.copy()

        payload = self.batch._build_payload(data)
        
        self.assertEqual(payload['url'], self.base_uri)
    
    def test_post_build_payload_raises_keyerror_with_fields_id_key(self):
        data = self.post_data.copy()
        data['body']['fields']['id'] = 1

        with self.assertRaises(KeyError):
            self.batch._build_payload(data)
    
    def test_post_build_payload_raises_typeerror_with_non_dict_fields_key(self):
        data = self.post_data.copy()

        data['body']['fields'] = ""

        with self.assertRaises(TypeError):
            self.batch._build_payload(data)


class TestSharepointListItemBatchActionsPatch(unittest.TestCase):

    def setUp(self):
        self.client = SharepointGraphClient(None)
        self.base_uri = self.client.sites("ParentSite/ChildSite").lists("MyList").items().build_url()
        self.patch_data = {
            "id": 1,
            "body": {
                "field1":"value1"
            }
        }
        self.batch = SharepointListItemBatchAction(self.patch_data.copy(), self.base_uri, self.client)
        self.batch.method = "PATCH"
    
    def test_patch_uri_includes_id(self):
        data = self.patch_data.copy()

        control_uri = f"{self.base_uri}/{data['id']}/fields"

        payload = self.batch._build_payload(data)

        self.assertEqual(payload['url'], control_uri)
    
    def test_patch_build_payload_raises_keyerror_with_fields_key(self):
        data = self.patch_data.copy()

        data['body']['fields'] = {}

        with self.assertRaises(KeyError):
            self.batch._build_payload(data)
    
def run():
    unittest.main()

if __name__ == "__main__":
    unittest.main()