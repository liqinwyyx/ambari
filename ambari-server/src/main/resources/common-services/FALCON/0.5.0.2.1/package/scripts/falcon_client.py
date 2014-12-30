"""
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

"""

from resource_management import *
from falcon import falcon

class FalconClient(Script):
  def install(self, env):
    self.install_packages(env)
    self.configure(env)


  def configure(self, env):
    import params

    env.set_params(params)
    falcon('client', action='config')


  def status(self, env):
    raise ClientComponentHasNoStatus()


  def pre_rolling_restart(self, env):
    import params
    env.set_params(params)

    # this function should not execute if the version can't be determined or
    # is not at least HDP 2.2.0.0
    if not params.version or compare_versions(format_hdp_stack_version(params.version), '2.2.0.0') < 0:
      return

    Logger.info("Executing Falcon Client Rolling Upgrade pre-restart")
    Execute(format("hdp-select set hadoop-client {version}"))


  def security_status(self, env):
    import status_params
    env.set_params(status_params)

    if status_params.security_enabled:
      self.put_structured_out({"securityState": "SECURED_KERBEROS"})
    else:
      self.put_structured_out({"securityState": "UNSECURED"})

if __name__ == "__main__":
  FalconClient().execute()
