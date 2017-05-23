MTF - Levels of testing
==========================================

Component level testing
----------------------------
- **WIP**
- **Test Subject** - RPM packages build by koji
- See sections Manual testing - *Rpm* or *Multihost*
- MTF could be used for component level testing, it is **not primar purpose** of this project


Module level testing
----------------------------

- **Test Subject** - Module Build (rpm packages produced by MBS and tagged by koji or Docker container created manually or by OSBS or similar service)
- See sections Manual testing - *Docker* *Nspawn*
- **This is primar purpose of this framework**
    - tagged rpm packages are not final artifacts (Module Compose should be final artifact) - for now it supply Compose level testing
    - Docker image is final build artifacts

Compose level testing
----------------------------
- **WIP**
- **Test Subject:** Module compose (done by Pungi https://pagure.io/pungi-fedora)
- We are waiting for real module composes, what will be able to provide data about modules (modulemd files, repositories)
- It does not exist yet.
- There should be service for module builds on demand, not just composes for all modules together
- MTF is prepared for *Compose testing* somehow
- How to:
    - remove modulemd-url from config use COMPOSE  env variable or compose-url inside config.yaml.
    - it gets all data from compose info
    - Scheduled as: `MODULE=nspawn COMPOSEURL=https://kojipkgs.stg.fedoraproject.org/compose/branched/jkaluza/latest-Fedora-Modular-26/compose/base-runtime/x86_64/os/ avocado run *.py`

