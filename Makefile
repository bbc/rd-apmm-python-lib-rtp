# James Sandford, copyright BBC 2020
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

PYTHON3=`which python3`

topdir := $(realpath $(dir $(lastword $(MAKEFILE_LIST))))
topbuilddir := $(realpath .)

DESTDIR=/
PROJECT=$(shell python3 $(topdir)/setup.py --name)
VERSION=$(shell python3 $(topdir)/setup.py --version)
MODNAME=$(PROJECT)

TOXDIR?=$(topbuilddir)/.tox/

all:
	@echo "$(PROJECT)-$(VERSION)"
	@echo "make source   - Create source package"
	@echo "make install  - Install on local system (only during development)"
	@echo "make clean    - Get rid of scratch and byte files"
	@echo "make test     - Test using tox"
	@echo "make wheel    - Create whl package"
	@echo "make docs     - Render pydocs as html"

$(topbuilddir)/dist:
	mkdir -p $@

source: $(topbuilddir)/dist
	$(PYTHON3) $(topdir)/setup.py sdist $(COMPILE) --dist-dir=$(topbuilddir)/dist

$(topbuilddir)/dist/$(MODNAME)-$(VERSION).tar.gz: source

install:
	$(PYTHON3) $(topdir)/setup.py install --root $(DESTDIR) $(COMPILE)

clean:
	$(PYTHON3) $(topdir)/setup.py clean || true
	rm -rf $(topbuilddir)/.tox
	rm -rf $(topbuilddir)/build/ MANIFEST
	rm -rf $(topbuilddir)/dist
	find $(topdir) -name '*.pyc' -delete
	find $(topdir) -name '*.py,cover' -delete
	rm -rf $(topbuilddir)/docs

testenv: $(TOXDIR)/py3/bin/activate

$(TOXDIR)/py3/bin/activate: tox.ini
	tox -e py3 --recreate --workdir $(TOXDIR)

test:
	tox --workdir $(TOXDIR)

wheel:
	$(PYTHON3) $(topdir)/setup.py bdist_wheel

docs: $(topbuilddir)/docs/$(MODNAME).html

$(topbuilddir)/docs/$(MODNAME):
	mkdir -p $(topbuilddir)/docs
	ln -s $(topdir)/$(MODNAME) $(topbuilddir)/docs/

$(topbuilddir)/docs/$(MODNAME).html: $(topbuilddir)/docs/$(MODNAME) $(TOXDIR)/py3/bin/activate
	. $(TOXDIR)/py3/bin/activate && cd $(topbuilddir)/docs/ && pydoc -w ./

.PHONY: test testenv clean install source wheel all docs
