  - move `aws.py` and `aws_cmdline.py` into `providers/`
  - iterate over `providers/*_cmdline.py`
  - move `provider.py` to `providers/__init__.py` (only for use by submodules)
  - sort by file order, name or instance ID
  - Handle `boto_helper.ProfileException`: Missing/incomplete credentials in profile 'xyz'
