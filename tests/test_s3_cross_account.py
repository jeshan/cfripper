"""
Copyright 2019 Skyscanner Ltd

Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""


import os
import pytest
import pycfmodel

from cfripper.rules.S3CrossAccountTrustRule import S3CrossAccountTrustRule
from cfripper.model.result import Result
from cfripper.s3_adapter import S3Adapter


class TestS3CrossAccountTrustRule:
    @pytest.fixture(scope="class")
    def template(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        cf_script = open(
            "{}/test_templates/s3_bucket_cross_account.json".format(dir_path)
        )
        cf_template = S3Adapter().convert_json_or_yaml_to_dict(cf_script.read())
        return pycfmodel.parse(cf_template)

    def test_with_cross_account_in_bucket_policy(self, template):
        result = Result()
        rule = S3CrossAccountTrustRule(None, result)

        rule.invoke(template.resources)

        assert result.valid
        assert len(result.failed_rules) == 0
        assert len(result.failed_monitored_rules) == 1
        assert (
            result.failed_monitored_rules[0]["reason"]
            == "S3BucketPolicyAccountAccess has forbidden cross-account policy allow with arn:aws:iam::987654321:root for an S3 bucket."
        )


class TestS3CrossAccountTrustRuleWithNormalAccess:
    @pytest.fixture(scope="class")
    def template(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        cf_script = open(
            "{}/test_templates/s3_bucket_cross_account_and_normal.json".format(dir_path)
        )
        cf_template = S3Adapter().convert_json_or_yaml_to_dict(cf_script.read())
        return pycfmodel.parse(cf_template)

    def test_with_cross_account_in_bucket_policy(self, template):
        result = Result()
        rule = S3CrossAccountTrustRule(None, result)

        rule.invoke(template.resources)

        assert result.valid
        assert len(result.failed_rules) == 0
        assert len(result.failed_monitored_rules) == 1
        assert (
            result.failed_monitored_rules[0]["reason"]
            == "S3BucketPolicyAccountAccess has forbidden cross-account policy allow with arn:aws:iam::666555444:root for an S3 bucket."
        )
