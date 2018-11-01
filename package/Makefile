NAME=report-app
VERSION=1.3.0
PACKAGE_VERSION=1
DESCRIPTION="Simple REST API for himlar"
URL="https://github.com/norcams/report-app"
MAINTAINER="https://github.com/norcams"
RELVERSION=7
INSTALL_DIR=/opt/report-app

.PHONY: default
default: deps build rpm
package: rpm

.PHONY: clean
clean:
	rm -fr /installdir
	rm -f $(NAME)-$(VERSION)-*.rpm
	rm -Rf /vendor/

.PHONY: deps
deps:
	yum install -y gcc ruby-devel rpm-build
	gem install -N fpm
	yum install -y python-devel python-virtualenv git libyaml-devel

.PHONY: build
build:
	mkdir /vendor
	mkdir -p /installdir${INSTALL_DIR}

	cd /vendor; git clone ${URL}
	rsync -avh --exclude '.git' /vendor/${NAME}/ /installdir${INSTALL_DIR}
	cd /installdir${INSTALL_DIR}; virtualenv --clear .
	cd /installdir${INSTALL_DIR}; bin/pip install -U setuptools
	cd /installdir${INSTALL_DIR}; bin/pip install -U pip

	cd /installdir${INSTALL_DIR}; bin/python setup.py install
	cd /installdir${INSTALL_DIR}; bin/pip install -r requirements.txt
	cd /installdir${INSTALL_DIR}; virtualenv --relocatable .
	# Hack
	echo "${INSTALL_DIR}" > /installdir${INSTALL_DIR}/lib/python2.7/site-packages/report_api.egg-link
	sed -i 's/\/installdir\/opt/\/opt/g' /installdir${INSTALL_DIR}/bin/activate
	# version file
	cd  /vendor/${NAME}; echo "commit: `git log --pretty=format:'%h' -n 1`" > /installdir${INSTALL_DIR}/version.yaml
	echo "version: ${VERSION}" >> /installdir${INSTALL_DIR}/version.yaml

.PHONY: rpm
rpm:
	/usr/local/bin/fpm -s dir -t rpm \
		-n $(NAME) \
		-v $(VERSION) \
		--iteration "$(PACKAGE_VERSION).el$(RELVERSION)" \
		--description ${DESCRIPTION} \
		--url ${URL} \
		--maintainer ${MAINTAINER} \
		-C /installdir/ \
		.
