import unit_test_framework

class APIUnitTestUserPrivilege(unit_test_framework.APIUnitTest):
    url = "/api/v1/user/privilege"
    post_payloads = [
        {
            "username": "admin",
            "priv": ["page-all", "page-system-usermanager"]
        }
    ]
    delete_payloads = [
        {
            "username": "admin",
            "priv": "page-system-usermanager"
        }
    ]

APIUnitTestUserPrivilege()