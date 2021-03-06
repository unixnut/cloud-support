#! /usr/bin/python

from __future__ import print_function

import botocore.session
import boto
# this is just used to get the environment variables that aws-cli uses
import awscli


class Credentials(object):
    """Loads credentials and the name of the default region from .aws/config.
    Stuffs the credentials into the boto module's in-memory credentials store.  
    Doesn't need to provide the ability to return credentials.
    
    Use default_region() to get the default region that was specified in .aws/config."""
    def __init__(self, profile=None):
        # Make a session and try to set the profile
        try:
            boto_session = botocore.session.Session(session_vars=awscli.EnvironmentVariables,
                                                    profile=profile)
        except TypeError as e:
            # "__init__() got an unexpected keyword argument 'profile'"
            # This argument was unsupported prior to botocore v1.1, so use the old
            # behaviour of munging the profile prior to loading the credentials
            boto_session = botocore.session.Session(session_vars=awscli.EnvironmentVariables)
            if profile:
                boto_session.profile = profile

        creds = boto_session.get_credentials()
        self._default_region = boto_session.get_config_variable('region')

        try:
            # Now create an in-memory copy of the [Credentials] section,
            # as if it came from .boto
            boto.config.add_section('Credentials')
            # ...and populate it with whichever creds were fetched from .aws/config
            boto.config.set('Credentials', 'aws_access_key_id', creds.access_key)
            boto.config.set('Credentials', 'aws_secret_access_key', creds.secret_key)
            # TO-DO: 
            ## boto.config.set('Credentials', 'security_token', creds.token)
        except AttributeError as e:
            p = boto_session.get_config_variable("profile")
            if p:
                raise ProfileException("Missing/incomplete credentials in profile '%s'" % (p,))
            else:
                raise ProfileException("Missing/incomplete credentials in default profile (maybe set $AWS_DEFAULT_PROFILE)")


    ## TO-DO: make @property
    def default_region(self):
        return self._default_region



# == Utility classes ==
class ProfileException(Exception):
    pass



# *** MAINLINE ***
if __name__ == "__main__":
    print("hi from " + __file__)
    c = Credentials()
    print(c.default_region())

